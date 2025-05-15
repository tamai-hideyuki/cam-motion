#!/usr/bin/env bash
set -euo pipefail

# == 定義 ==
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
HAND_SCRIPT="$PROJECT_ROOT/examples/hand_tracking.py"
LINE_SCRIPT="$PROJECT_ROOT/examples/line_detection.py"
TRACE_SCRIPT="$PROJECT_ROOT/examples/spatial_trace.py"
CURB_SCRIPT="$PROJECT_ROOT/examples/curb_detection.py"
OBST_SCRIPT="$PROJECT_ROOT/examples/obstacle_detection.py"

# === 引数パース ===
MODE="hand"
if [[ "${1-}" == "--mode" && -n "${2-}" ]]; then
  MODE="$2"
fi

# === 仮想環境作成・アクティベート ===
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO]: 仮想環境を作成中…"
  python3 -m venv "$VENV_DIR"
fi
source "${VENV_DIR}/bin/activate"

# === 依存インストール ===
if ! pip show opencv-python &>/dev/null || ! pip show mediapipe &>/dev/null; then
  echo "[INFO]: パッケージをインストール中…"
  pip install --upgrade pip
  pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# === 実行スクリプト選択 ===
case "$MODE" in
  hand)
    SELECTED="$HAND_SCRIPT"
    echo "[INFO]: 手追跡モード"
    ;;
  line)
    SELECTED="$LINE_SCRIPT"
    echo "[INFO]: 線検出モード"
    ;;
  trace)
    SELECTED="$TRACE_SCRIPT"
    echo "[INFO]: 空間トレースモード"
    ;;
  curb)
    SELECTED="$CURB_SCRIPT"
    echo "[INFO]: 歩道縁取り検出モード"
    ;;
  detect)
    SELECTED="$OBST_SCRIPT"
    echo "[INFO]: 障害物検出モード"
    ;;
  *)
    echo "[ERROR]: 未知のモード \"$MODE\"。--mode hand|line|trace|curb|detect を指定してください。"
    exit 1
    ;;
esac

# === 実行 ===
python "$SELECTED"
