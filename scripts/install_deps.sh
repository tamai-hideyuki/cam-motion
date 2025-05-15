#!/usr/bin/env bash
set -eup pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="$PROJECT_ROOT/venv"

# 仮想環境作成
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] 仮想環境できたよ！ -> $VENV_DIR ..."
    # Python 3.11 を優先して venv 作成
    PYTHON_BIN=$(which python3.11 || which python3)
    echo "[INFO] Using Python: $($PYTHON_BIN --version)"
    $PYTHON_BIN -m venv "$VENV_DIR"
else
  echo "[INFO] 仮想環境既にあるよ。。。"
fi

# 仮想環境をアクティベート
source "$VENV_DIR/bin/activate"

# pip更新と依存インストール
pip install --upgrade pip
pip install -r requirements.txt

echo "[INFO] 設定完了！ 実行中！？ -> ./scripts/run.sh"
