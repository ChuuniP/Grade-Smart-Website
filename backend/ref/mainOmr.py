import sys
import os
import json
import random
import datetime
import cv2
import numpy as np
from PIL import Image
import support as sp
import solveImg as si
import OmrMDD as omr_mdd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

WIDTH_IMG = 500
HEIGHT_IMG = 700
QUESTIONS = 40
CHOICES = 4
FINAL_ANS = [1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2,
             1, 2, 2, 2, 3, 3, 2, 1, 3, 0, 0, 0, 1, 2, 2, 2, 3, 1, 0, 2]

# Ngưỡng pixel để xác định ô có được tô hay không.
BLANK_PIXEL_THRESHOLD = 15


def load_image(image_path):
    try:
        pil_img = Image.open(image_path)
        image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    except Exception as exc:
        raise RuntimeError(f'Unable to load image: {exc}')

    if image is None:
        raise FileNotFoundError(f'Image not found or unsupported format: {image_path}')

    return cv2.resize(image, (WIDTH_IMG, HEIGHT_IMG))


def extract_student_info(image, image_path):
    try:
        _, student_digits, paper_digits = omr_mdd.ReadMDD(image)
        student_id = ''.join(str(int(d)) for d in student_digits)
        paper_code = ''.join(str(int(d)) for d in paper_digits)

        if len(student_id) != 6:
            student_id = None
        if len(paper_code) != 3:
            paper_code = None
    except Exception:
        student_id = None
        paper_code = None

    if paper_code is None:
        paper_code = os.path.splitext(os.path.basename(image_path))[0].upper()[:3]
    if student_id is None:
        student_id = f'{random.randint(0, 999999):06d}'

    return student_id, paper_code


def extract_answers(image):
    img = image.copy()
    imgAns = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 150)
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # 1. Lọc contour bằng sp.rectContour giống tham_khao_omr.py để warp chính xác
    contours = sp.rectContour(contours)

    if len(contours) == 0:
        raise RuntimeError('Không tìm thấy contour của phiếu trả lời')

    # Dùng float64 giống file tham khảo
    pointContour = np.zeros((4, 2))
    img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

    perX1, perX2, perY1, perY2 = 20, 490, 35, 685
    imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
    imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)

    # 2. Dùng nhị phân hóa toàn cục với ngưỡng 140 cho form MDD 120-câu để chuyển đổi chính xác hơn
    imgThresh = cv2.threshold(imgCvt, 140, 255, cv2.THRESH_BINARY_INV)[1]

    boxes = sp.splitImg120(imgThresh)

    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
    row_height = boxes[0].shape[0] // 15
    col_width = boxes[0].shape[1] // CHOICES

    for question_index in range(QUESTIONS):
        box_index = question_index // 15
        row_index = question_index % 15
        box = boxes[box_index]
        for choice_index in range(CHOICES):
            start_x = choice_index * col_width
            end_x = start_x + col_width
            start_y = row_index * row_height
            end_y = start_y + row_height
            cell = box[start_y:end_y, start_x:end_x]
            pixel_vals[question_index][choice_index] = cv2.countNonZero(cell)

    student_answers = []
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > BLANK_PIXEL_THRESHOLD:
            myIndexVal = np.where(arr == max_value)
            student_answers.append(int(myIndexVal[0][0]))
        else:
            student_answers.append(-1)

    return student_answers, imgWarpColored, pt1, pt2, perX1, perX2, perY1, perY2


def grade_answers(student_answers, student_id, paper_code):
    correct = 0
    wrong = 0
    blank = 0
    details = []
    choice_labels = ['A', 'B', 'C', 'D']

    for index, student in enumerate(student_answers):
        expected = FINAL_ANS[index]
        if student == -1:
            status = 'bỏ trống'
            blank += 1
        elif student == expected:
            status = 'đúng'
            correct += 1
        else:
            status = 'sai'
            wrong += 1

        details.append({
            'question': index + 1,
            'studentAnswer': 'Bỏ trống' if student == -1 else choice_labels[student],
            'correctAnswer': choice_labels[expected],
            'status': status,
            'isCorrect': student == expected
        })

    score = round((correct / QUESTIONS) * 10, 1)
    return {
        'paperCode': paper_code,
        'studentId': student_id,
        'studentCode': f'HS-{datetime.datetime.now().year}-{random.randint(0, 9999):04d}',
        'score': score,
        'totalScore': 10,
        'totalQuestions': QUESTIONS,
        'correct': correct,
        'wrong': wrong,
        'blank': blank,
        'details': details,
        'timestamp': datetime.datetime.now().isoformat()
    }


def main(image_path, custom_answers=None):
    global QUESTIONS, FINAL_ANS
    if custom_answers is not None:
        FINAL_ANS = custom_answers
        QUESTIONS = len(custom_answers)

    image = load_image(image_path)
    student_id, paper_code = extract_student_info(image, image_path)
    student_answers, imgWarpColored, pt1, pt2, perX1, perX2, perY1, perY2 = extract_answers(image)
    
    result = grade_answers(student_answers, student_id, paper_code)

    # Khắc phục lỗi hiển thị ảnh sau khi chấm: vẽ đáp án, SBD, mã đề và điểm lên ảnh gốc và lưu lại
    try:
        # Danh sách chấm đúng/sai
        grading = []
        for index, student in enumerate(student_answers):
            expected = FINAL_ANS[index]
            if student == expected:
                grading.append(1)
            else:
                grading.append(0)

        # Vẽ đáp án Đúng/Sai trên vùng ảnh đáp án
        imgRevert = imgWarpColored[perY1:perY2, perX1:perX2].copy()
        imgRawRevert = np.zeros_like(imgRevert)
        rawBoxes = sp.splitImg(imgRawRevert)
        stack = min(QUESTIONS // 5, len(rawBoxes))
        
        for x in range(stack):
            stackAns = FINAL_ANS[x*5:x*5+5]
            stackIndex = student_answers[x*5:x*5+5]
            stackGrading = grading[x*5:x*5+5]

            oriWidth = rawBoxes[x].shape[1]
            oriHeight = rawBoxes[x].shape[0]
            rawBoxes[x] = sp.ResizeImg(rawBoxes[x], 500, 500)
            rawBoxes[x] = sp.showAnswer(rawBoxes[x], stackIndex, stackGrading, stackAns, 5, 4)
            rawBoxes[x] = sp.ResizeImg(rawBoxes[x], oriWidth, oriHeight)
            
        reRawImg = sp.restoreImg(imgRawRevert, rawBoxes, stack)
        
        imgRawRevert1 = np.zeros_like(imgWarpColored)
        imgRawRevert1[perY1:perY2, perX1:perX2] = reRawImg

        invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
        imgInvWarp = cv2.warpPerspective(imgRawRevert1, invMatrix, (WIDTH_IMG, HEIGHT_IMG))
        
        # Đè các vòng tròn đáp án lên bản sao của ảnh gốc
        imgFinal = image.copy()
        imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
        
        # Nhận diện SBD và Mã đề để vẽ vòng tròn xanh
        imgFinal, MDD, MD = omr_mdd.ReadMDD(imgFinal)
        
        # Vẽ Điểm số và thông tin điểm
        import OmrScore as omr_score
        imgFinal = omr_score.ReadScore(imgFinal, sum(grading), QUESTIONS)
        
        # Cắt và biến đổi phối cảnh ảnh kết quả cuối cùng (giống OmrFinalImg.py nhưng không dùng cv2.imshow)
        widthImg = 500
        heightImg = 700
        imgAns_copy = imgFinal.copy()
        imgGray_f = cv2.cvtColor(imgFinal, cv2.COLOR_BGR2GRAY)
        imgCanny_f = cv2.Canny(imgGray_f, 50, 150)
        contours_f, _ = cv2.findContours(imgCanny_f, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_f = sp.rectContour(contours_f)
        pointContour_f = np.zeros((4, 2))
        imgFinal, pointContour_f = si.TakeImgFinal(imgFinal, pointContour_f, contours_f)
        pt1_f = np.float32([pointContour_f[0], pointContour_f[1], pointContour_f[2], pointContour_f[3]])
        pt2_f = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix_f = cv2.getPerspectiveTransform(pt1_f, pt2_f)
        warpImg_f = cv2.warpPerspective(imgAns_copy, matrix_f, (widthImg, heightImg))
        finalImg = warpImg_f[25:690, 15:495]
        finalImg = cv2.resize(finalImg, (widthImg, heightImg))
        cv2.putText(finalImg, str(int(MDD[0])) + str(int(MDD[1])) + str(int(MDD[2])) + str(int(MDD[3])) + str(int(MDD[4])) + str(int(MDD[5])), (375, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
        cv2.putText(finalImg, str(int(MD[0])) + str(int(MD[1])) + str(int(MD[2])), (455, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
        
        # Lưu ảnh kết quả vào thư mục uploads
        dir_name = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        graded_image_name = f"graded_{base_name}.jpg"
        graded_image_path = os.path.join(dir_name, graded_image_name)
        cv2.imwrite(graded_image_path, finalImg)
        
        result['gradedImagePath'] = graded_image_name
    except Exception as e:
        # Phương án dự phòng (fallback) nếu quá trình vẽ có lỗi: lưu luôn ảnh imgWarpColored
        try:
            dir_name = os.path.dirname(image_path)
            base_name = os.path.basename(image_path)
            graded_image_name = f"graded_{base_name}.jpg"
            graded_image_path = os.path.join(dir_name, graded_image_name)
            cv2.imwrite(graded_image_path, imgWarpColored)
            result['gradedImagePath'] = graded_image_name
        except Exception:
            pass

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Missing image path'}), file=sys.stderr)
        sys.exit(1)

    custom_answers = None
    if len(sys.argv) > 2:
        try:
            raw_answers = json.loads(sys.argv[2])
            choice_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            custom_answers = [choice_map.get(ans.upper(), -1) for ans in raw_answers]
        except Exception:
            pass

    try:
        outcome = main(sys.argv[1], custom_answers)
        print(json.dumps(outcome, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        sys.exit(1)
