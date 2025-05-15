#!/usr/bin/env bash
set -euo pipefail

# == 定義 ==
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
MAIN_SCRIPT="$PROJECT_ROOT/examples/hand_tracking.py"


# == 仮想環境がなければ作成 ==
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO]:仮想環境作ってるんでちょっと待ってね。。。"
  python3 -m venv "$VENV_DIR"
fi

# == 仮想環境のアクティベート ==
source "${VENV_DIR}/bin/activate"

# == 依存パッケージを確認・インストール ==
if ! pip show opencv-python &>/dev/null || ! pip show mediapipe &>/dev/null; then
  echo "[INFO]:必要なパッケージ入れてます！？"
  pip install --upgrade pip
  pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# == スクリプトの実行 ==
echo "[INFO]:cam-motion 行きます！！: hand_tracking.py"
python "$MAIN_SCRIPT"
