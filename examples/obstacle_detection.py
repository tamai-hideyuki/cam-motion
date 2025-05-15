# examples/obstacle_detection.py

import cv2
import numpy as np
import time
import subprocess   # say コマンドで通知

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    time.sleep(1)

    print("[INFO] 障害物検出モード（Contour） 起動。'q' で終了。")
    while True:
        ret, frame = cap.read()
        if not ret: break

        gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edges   = cv2.Canny(blurred, 50, 150)

        # 輪郭検出
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 500 < area < 5000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                subprocess.Popen(['say', '障害物注意'])

        cv2.imshow("Obstacle Detection (Contour)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
