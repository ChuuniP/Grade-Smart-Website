import sys
import os
import json
import random
import datetime
import cv2
import numpy as np
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


def load_image(image_path):
    try:
        data = np.fromfile(image_path, dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
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
    contours = sp.rectContour(contours)

    if len(contours) == 0:
        raise RuntimeError('Không tìm thấy contour của phiếu trả lời')

    pointContour = np.zeros((4, 2), dtype=np.float32)
    img, pointContour = si.TakeImgAnswer(img, pointContour, contours)

    pt1 = np.float32([pointContour[0], pointContour[1], pointContour[2], pointContour[3]])
    pt2 = np.float32([[0, 0], [WIDTH_IMG, 0], [0, HEIGHT_IMG], [WIDTH_IMG, HEIGHT_IMG]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(imgAns, matrix, (WIDTH_IMG, HEIGHT_IMG))

    perX1, perX2, perY1, perY2 = 20, 490, 35, 685
    imgPer = imgWarpColored[perY1:perY2, perX1:perX2]
    imgCvt = cv2.cvtColor(imgPer, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgCvt, 135, 255, cv2.THRESH_BINARY_INV)[1]

    boxes = sp.splitImg(imgThresh)
    ans_images = sp.splitAns(boxes)

    pixel_vals = np.zeros((QUESTIONS, CHOICES), dtype=np.int32)
    max_cells = QUESTIONS * CHOICES
    for index, image_piece in enumerate(ans_images[:max_cells]):
        total_pixels = cv2.countNonZero(image_piece)
        row = index // CHOICES
        col = index % CHOICES
        pixel_vals[row][col] = total_pixels

    student_answers = []
    for idx in range(QUESTIONS):
        arr = pixel_vals[idx]
        max_value = np.amax(arr)
        if max_value > 50:
            selected = int(np.argmax(arr))
            student_answers.append(selected)
        else:
            student_answers.append(-1)

    return student_answers


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


def main(image_path):
    image = load_image(image_path)
    student_id, paper_code = extract_student_info(image, image_path)
    student_answers = extract_answers(image)
    return grade_answers(student_answers, student_id, paper_code)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Missing image path'}), file=sys.stderr)
        sys.exit(1)

    try:
        outcome = main(sys.argv[1])
        print(json.dumps(outcome, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        sys.exit(1)
