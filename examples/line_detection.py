import cv2
import numpy as np

def detect_and_draw_lines(frame):
    # 1. グレースケール変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2. ノイズ除去（ガウシアンブラー）
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
    # 3. エッジ検出（Canny）
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    # 4. ハフ変換（確率的Hough）
    lines = cv2.HoughLinesP(
        edges,
        rho=1,               # 距離解像度：1ピクセル
        theta=np.pi / 180,   # 角度解像度：1度
        threshold=80,        # 線と認定するための最小投票数
        minLineLength=50,    # 最小線分長
        maxLineGap=10        # 線分をつなぐ最大ギャップ
    )
    # 5. 検出線を元のフレームに描画
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    # 必要ならポーリング待機を挿入…

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 線検出＆描画
        output = detect_and_draw_lines(frame)

        cv2.imshow("Line Detection", output)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
