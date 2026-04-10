import cv2
import numpy as np

class LaneDetector:
    def __init__(self):
        pass

    def process_frame(self, frame):
        # 1. Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. Gaussian Blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 3. Canny Edge Detection
        canny = cv2.Canny(blur, 50, 150)
        
        # 4. ROI Masking (Simulator track ke liye specialized area)
        height, width = canny.shape
        mask = np.zeros_like(canny)
        # Trapezoid shape for simulator track
        polygon = np.array([[
            (0, height * 0.9),
            (width * 0.45, height * 0.6),
            (width * 0.55, height * 0.6),
            (width, height * 0.9),
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_edges = cv2.bitwise_and(canny, mask)
        
        # 5. Hough Transform
        lines = cv2.HoughLinesP(masked_edges, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
        
        # 6. Draw Lanes Overlay
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        
        # Combine Result
        combined = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return combined, lines

    def get_steering_offset(self, lines, width):
        # Logically calculate center offset
        # Simplified: average of bottom point of lines
        if lines is None:
            return 0
        
        mid = width / 2
        offsets = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                offsets.append(x1)
                offsets.append(x2)
        
        if not offsets:
            return 0
            
        lane_center = np.mean(offsets)
        return (lane_center - mid) / mid # Normalized offset
