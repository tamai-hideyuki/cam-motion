#!/usr/bin/env bash
set -euo pipefail

# == 定義 ==
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
HAND_SCRIPT="$PROJECT_ROOT/examples/hand_tracking.py"
LINE_SCRIPT="$PROJECT_ROOT/examples/line_detection.py"
TRACE_SCRIPT="$PROJECT_ROOT/examples/spatial_trace.py"

# === 引数パース ===
MODE="hand"
if [[ "${1-}" == "--mode" && -n "${2-}" ]]; then
  MODE="$2"
fi

# === 仮想環境作成 ===
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO]: 仮想環境を作成中…"
  python3 -m venv "$VENV_DIR"
fi

# === 仮想環境アクティベート ===
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
    echo "[INFO]: cam-motion モード=手追跡 → hand_tracking.py を実行"
    ;;
  line)
    SELECTED="$LINE_SCRIPT"
    echo "[INFO]: cam-motion モード=線検出 → line_detection.py を実行"
    ;;
  trace)
    SELECTED="$TRACE_SCRIPT"
    echo "[INFO]: cam-motion モード=空間トレース → spatial_trace.py を実行"
    ;;
  *)
    echo "[ERROR]: 未知のモード \"$MODE\"。--mode hand|line|trace を指定してください。"
    exit 1
    ;;
esac

# === 実行 ===
python "$SELECTED"
