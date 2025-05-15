import cv2
import numpy as np
import time
import subprocess   # playsound から say 呼び出しへ変更

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    time.sleep(1)  # カメラが安定するまで少し待機

    if not cap.isOpened():
        raise RuntimeError("カメラ初期化失敗")

    print("[INFO] 歩道縁取り検出モード 起動。'q' で終了。")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edges   = cv2.Canny(blurred, 50, 150)

        # HoughLinesP で直線検出
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=w // 4,
            maxLineGap=20
        )

        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                # 地面とほぼ平行（水平線）を白線で描画
                if abs(y2 - y1) < 10:
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    # 段差判定：画面下端からの高さが 10% 以上なら音声通知
                    if h - y1 > h * 0.1:
                        subprocess.Popen(['say', '段差注意'])

        cv2.imshow("Curb Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] 終了します。")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
