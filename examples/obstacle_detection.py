import cv2
import numpy as np
import time
import subprocess   # say コマンドで通知

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    time.sleep(1)  # カメラ安定待機

    if not cap.isOpened():
        raise RuntimeError("カメラ初期化失敗")

    print("[INFO] 障害物検出モード（Contour） 起動。'q' で終了。")

    last_notify = 0.0
    notify_interval = 2.0  # 通知は2秒に1回まで

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ── 解像度ダウン ──
        small = cv2.resize(frame, (320, 240))

        # ── 前処理 ──
        gray    = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edges   = cv2.Canny(blurred, 50, 150)

        # ── モルフォロジーでノイズ除去 ──
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # ── 輪郭検出 ──
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        now = time.time()
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if not (500 < area < 5000):
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / float(h)

            # 面積＋アスペクト比＋ROI（下部40％）に限定
            if not (0.2 < aspect < 5.0):
                continue
            if y < small.shape[0] * 0.6:
                continue

            # 検出ボックスを描画
            cv2.rectangle(small, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # 通知抑制（2秒インターバル）
            if now - last_notify > notify_interval:
                subprocess.call(['say', '障害物注意'])
                last_notify = now

        # ── 表示＆終了判定 ──
        cv2.imshow("Obstacle Detection (Contour)", small)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] 終了します。")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
