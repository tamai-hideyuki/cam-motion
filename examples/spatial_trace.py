import time
import cv2
import mediapipe as mp
from collections import deque

# --- 設定 ---
MAX_TRAIL = 64        # 軌跡として残すフレーム数
POINT_IDX = 8         # 人差し指先のランドマーク index (0=手首, 8=人差し指先)
TRAIL_COLOR = (0,255,0)
TRAIL_THICKNESS = 2

# --- Mediapipe 初期化 ---
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,                # 軌跡は片手に限定
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- カメラオープン ＋ ポーリング待機 ---
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
timeout, interval, elapsed = 5.0, 0.2, 0.0
while not cap.isOpened() and elapsed < timeout:
    time.sleep(interval)
    elapsed += interval
if not cap.isOpened():
    raise RuntimeError("カメラ初期化に失敗しました")

# --- 軌跡データ構造 ---
trail = deque(maxlen=MAX_TRAIL)

print("[INFO] CamMotion 空間トレースモード 起動。'q'で終了")

# --- メインループ ---
while True:
    success, img = cap.read()
    if not success:
        break

    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # ランドマーク取得
    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark[POINT_IDX]
        # 画面座標に変換して trail に追加
        px, py = int(lm.x * w), int(lm.y * h)
        trail.append((px, py))
        # 手全体のランドマークも描画
        mp_draw.draw_landmarks(img, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    # 軌跡を描画（deque 内の点を順につなぐ）
    for i in range(1, len(trail)):
        cv2.line(img, trail[i-1], trail[i], TRAIL_COLOR, TRAIL_THICKNESS)

    cv2.imshow("CamMotion - Spatial Trace", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
