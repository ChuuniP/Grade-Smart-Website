import cv2
import numpy as np

def order_points(pts):
    """Sắp xếp 4 tọa độ góc theo thứ tự: trên-trái, trên-phải, dưới-phải, dưới-trái [4]"""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    """Thực hiện biến biến đổi phối cảnh để đưa tờ giấy về dạng phẳng [4]"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Tính toán chiều rộng tối đa (khoảng cách Euclidean giữa các góc đối diện)
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    # Tính toán chiều cao tối đa (khoảng cách Euclidean giữa các góc đối diện)
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Tạo các điểm đích phẳng cho Perspective Transform
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))

def solve_omr(image_path, questions=5, choices=5):
    # 1. Tiền xử lý: Sử dụng Blur và Canny để tìm biên giấy
    image = cv2.imread(image_path)
    if image is None:
        return "Không thể tải ảnh."
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # Tìm đường bao lớn nhất (giả định là tờ giấy)
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    doc_cnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                doc_cnt = approx
                break

    if doc_cnt is None:
        return "Không tìm thấy khung giấy."

    # 2. Biến đổi phối cảnh phẳng tờ giấy
    paper = four_point_transform(gray, doc_cnt.reshape(4, 2))
    
    # 3. Nhị phân hóa thích nghi (Adaptive Thresholding) để xử lý ánh sáng không đều
    thresh = cv2.adaptiveThreshold(paper, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # 4. Tìm các ô tròn (bubbles) dựa trên diện tích và tỷ lệ khung hình
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    question_cnts = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # Bộ lọc thông minh: diện tích lớn hơn nhiễu nhỏ và tỉ lệ cạnh xấp xỉ tròn
        if w >= 20 and h >= 20 and 0.8 <= ar <= 1.2:
            question_cnts.append(c)

    # 5. Phân nhóm phân cấp 2 bước (Hierarchical Sorting)
    # Bước 1: Sắp xếp theo trục Y (từ trên xuống dưới)
    sorted_by_y = sorted(question_cnts, key=lambda c: cv2.boundingRect(c)[1])
    
    # Bước 2: Gom nhóm các bubble thuộc cùng một hàng dựa trên khoảng cách Y gần nhau
    rows = []
    for c in sorted_by_y:
        (x, y, w, h) = cv2.boundingRect(c)
        added = False
        for r in rows:
            # So sánh tọa độ Y hiện tại với Y của phần tử đại diện hàng đó
            ref_y = r[0][1]
            if abs(y - ref_y) < h * 0.5:  # Ngưỡng đè lấp dọc
                r.append((x, y, w, h, c))
                added = True
                break
        if not added:
            rows.append([(x, y, w, h, c)])
            
    # Sắp xếp các hàng từ trên xuống dưới theo tọa độ Y trung bình
    rows = sorted(rows, key=lambda r: r[0][1])
    
    # Sắp xếp mỗi hàng từ trái sang phải theo tọa độ X
    sorted_rows = []
    for r in rows:
        r_sorted = sorted(r, key=lambda item: item[0])
        sorted_rows.append(r_sorted)

    results = []
    choice_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Hỗ trợ động nhiều phương án lựa chọn

    # Duyệt qua từng hàng câu hỏi
    for q_idx, row in enumerate(sorted_rows):
        # Đảm bảo hàng có đủ số ô tròn theo số phương án choices yêu cầu
        if len(row) < choices:
            # Nếu phát hiện thiếu ô tròn do lỗi đứt nét, điền kết quả trống
            results.append((q_idx + 1, "Không xác định (Thiếu bubble)"))
            continue
            
        # Chỉ xét đúng số lượng choices đầu tiên trong hàng câu hỏi
        row_choices = row[:choices]
        row_densities = []
        
        for idx, (x, y, w, h, c) in enumerate(row_choices):
            # Tạo mask chính xác cho ô tròn hiện tại
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            
            # Tính toán lượng pixel trắng bên trong vùng mask
            masked_img = cv2.bitwise_and(thresh, thresh, mask=mask)
            total_pixels = cv2.countNonZero(masked_img)
            contour_area = cv2.contourArea(c)
            
            row_densities.append((total_pixels, contour_area, idx))
            
        # Tìm ô tròn có mật độ tô màu đậm nhất
        max_pixels, best_area, best_choice_idx = max(row_densities, key=lambda item: item[0])
        
        # Ngưỡng tự tin (Confidence Threshold): Ít nhất 35% diện tích contour phải được tô sáng
        confidence_thresh = 0.35 * best_area
        if max_pixels >= confidence_thresh:
            selected_ans = choice_labels[best_choice_idx]
        else:
            selected_ans = "Bỏ trống"  # Không đủ độ tin cậy -> học sinh bỏ trống hoặc tẩy xóa sạch
            
        results.append((q_idx + 1, selected_ans))
        
    return results
