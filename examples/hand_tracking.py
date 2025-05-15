import time
import cv2
import mediapipe as mp

# === Mediapipe 初期化 ===
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7
)

# === AVFoundationバックエンドでカメラオープン ===
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# === カメラ準備待機（最大5秒） ===
timeout, interval, elapsed = 5.0, 0.2, 0.0
while not cap.isOpened() and elapsed < timeout:
    time.sleep(interval)
    elapsed += interval

if not cap.isOpened():
    raise RuntimeError(f"カメラ初期化失敗（{timeout}秒経過）")

print("[INFO] CamMotion 起動完了！終了するには 'q' を押してください。")

# === メインループ ===
while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] フレーム取得に失敗しました…")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("CamMotion - Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] 終了します。")
        break

cap.release()
cv2.destroyAllWindows()
