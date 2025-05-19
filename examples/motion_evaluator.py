# motion_evaluator.py

import time
import cv2
import mediapipe as mp
import numpy as np

# --- 関数定義 ---

def compute_angle(point_a, point_b, point_c):
    """
    点 A–B–C の関節角度を計算する。
    B を頂点とし、BA ベクトルと BC ベクトルのなす角を度で返す。
    """
    v_ab = np.array(point_a) - np.array(point_b)
    v_cb = np.array(point_c) - np.array(point_b)
    cos_theta = np.dot(v_ab, v_cb) / (np.linalg.norm(v_ab) * np.linalg.norm(v_cb))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

def extract_2d_coordinates(landmark, image_width, image_height):
    """
    Mediapipe の正規化座標 landmark を画像ピクセル座標に変換して返す。
    """
    return (int(landmark.x * image_width), int(landmark.y * image_height))

# --- Mediapipe 手検出器の初期化 ---
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hand_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,               # 片手のみ追跡
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- データ格納用 ---
elbow_angles       = []  # 肘関節角度時系列
timestamps         = []

# --- カメラオープン ---
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
if not cap.isOpened():
    raise RuntimeError("カメラの初期化に失敗しました")

print("[INFO] MotionEvaluator 起動。'q' で終了し、結果を表示します。")

# --- メインループ ---
while True:
    success, frame = cap.read()
    if not success:
        print("[ERROR] フレーム取得に失敗しました")
        break

    t_now = time.time()
    h, w = frame.shape[:2]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand_detector.process(frame_rgb)

    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark

        # 肘関節角度：肩(wrist相当), 肘(index_mcp相当), 手首(index_pip相当) を仮定
        shoulder_pt = extract_2d_coordinates(lm[mp_hands.HandLandmark.WRIST], w, h)
        elbow_pt    = extract_2d_coordinates(lm[mp_hands.HandLandmark.INDEX_FINGER_MCP], w, h)
        wrist_pt    = extract_2d_coordinates(lm[mp_hands.HandLandmark.INDEX_FINGER_PIP], w, h)

        angle_elbow = compute_angle(shoulder_pt, elbow_pt, wrist_pt)

        elbow_angles.append(angle_elbow)
        timestamps.append(t_now)

        # 手のランドマークを描画
        mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    # 映像表示
    cv2.imshow("MotionEvaluator - 評価モード", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] 計測終了。結果を算出中…")
        break

# --- 後処理と結果算出 ---
cap.release()
cv2.destroyAllWindows()

# フレーム間時間差
delta_times = np.diff(timestamps)

# 可動域 (Range of Motion)
if elbow_angles:
    rom_elbow = max(elbow_angles) - min(elbow_angles)

    # 角度変化速度 (deg/s)
    angular_speeds = np.diff(elbow_angles) / delta_times
    peak_speed_elbow = np.max(np.abs(angular_speeds))

    # 滑らかさ指標 (ジャークの標準偏差)
    jerks = np.diff(angular_speeds) / delta_times[1:]
    smoothness_elbow = np.std(jerks)

    # 結果表示
    print(f"肘の可動域 (ROM): {rom_elbow:.1f} °")
    print(f"肘のピーク速度:     {peak_speed_elbow:.1f} °/s")
    print(f"肘の滑らかさ指標:   {smoothness_elbow:.4f}")
else:
    print("手が検出されなかったため、結果を算出できませんでした。")
