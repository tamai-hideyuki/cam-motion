## 名称：cam-motion


## 🚀 目的:
- OpenCV + Mediapipe を利用し、内蔵カメラから手や足などの動きを高精度にキャプチャし、リアルタイムにトラッキングする。

### 🛠️ 使い方

- **Makefile を使って環境構築から実行まで一括実行**

```bash
# 初回／依存インストール
make install

# 手の追跡
make run

# 実世界の線検出
make run-line

# 動きの軌跡トレース
make run-trace

# 歩道の縁取り検出
make run-curb

# 障害物検出
make run-obstacle

# 仮想環境リセット
make clean

---
````
## 📋 大まかなディレクトリ構成：
```
.
├── assets
│   └── logo.png
├── cam_motion
│   ├── __init__.py
│   ├── config.py
│   ├── draw_utils.py
│   └── tracker.py
├── examples
│   ├── hand_tracking.py
│   └── line_detection.py
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── scripts
│   ├── install_deps.sh
│   └── run.sh
└── tests
    └── test_tracker.py
```
---
## 📦 インストール方法
#### リポジトリをクローン
```
https://github.com/tamai-hideyuki/cam-motion.git
cd cam-motion
```
#### 仮想環境 & 依存構築
```
ochmod +x scripts/install_deps.sh
./scripts/install_deps.sh
```
#### 実行
```
chmod +x scripts/run.sh
./scripts/run.sh
```
上記の方法ではなく、仮想環境なしで実行する場合は
- グローバルインストールになるため、他プロジェクトとバージョン競合に注意してください。
- 必要に応じて pip install --user オプションでユーザーレベルにインストール可能です。

---

## 🕰️ 開発フロー（時系列）
1.プロジェクト雛形作成
- 拡張性を考慮し、cam_motion/ モジュール、scripts/、examples/、tests/、assets/ フォルダを作成。
- requirements.txt, pyproject.toml, .gitignore, README.md を配置。

2.エントリースクリプトの実装
- scripts/install_deps.sh で仮想環境作成と依存インストールを自動化。
- scripts/run.sh で仮想環境のアクティベート、依存確認、サンプルスクリプト実行を実装。

3.サンプルコード作成
- examples/hand_tracking.py に Mediapipe + OpenCV を組み合わせた手の検出・描画処理を記述。

4.スクリプトと環境整備のデバッグ
- run.sh で仮想環境の bin/activate パスや変数展開の誤りを修正。
- install_deps.sh の set -euo pipefail のタイプミス修正。
- macOS 権限周りでカメラが開かれない問題に対処（システム設定でターミナルにカメラアクセス許可）。

5.Python バージョン調整
- Homebrew Python 3.13 環境で mediapipe が未対応のため、Python 3.11 で仮想環境を再作成。
- venv のリセット、再生成、pip install -r requirements.txt で依存導入。

6.macOS 用バックエンド指定＆ポーリング実装
- cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION) とすることで AVFoundation バックエンドを明示。
- カメラオープン時に最大 5 秒間のポーリング待機を実装し、起動安定性向上。

7.動作確認
- ./scripts/run.sh 実行後、ターミナルにログが表示され、カメラ映像ウィンドウが立ち上がる。
- 'q' キー押下で正常終了を確認。

8.Makefile作成
- make cam-motion で起動するようにした。

## ⚙️ Troubleshooting
- venv/bin/activate: No such file or directory→ rm -rf venv && ./scripts/install_deps.sh で仮想環境を再生成。
- Could not find a version that satisfies the requirement mediapipe→ Python 3.11 で仮想環境を作成する。
- OpenCV: not authorized to capture video→ システム設定 > プライバシーとセキュリティ > カメラ からターミナルに権限付与。


## ✨ 今後の拡張案
- 足や顔、姿勢検出などのトラッカー実装を cam_motion/tracker.py に追加
- CLI 引数対応（例：cam-motion --mode=face）
- GPU 加速 / TensorRT 対応
- 単体テスト・CI/CD パイプライン整備


