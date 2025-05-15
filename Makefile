# Makefile for cam-motion

# デフォルトターゲット
.DEFAULT_GOAL := run

# 仮想環境のディレクトリ
VENV           := venv
INSTALL_SCRIPT := scripts/install_deps.sh
RUN_SCRIPT     := scripts/run.sh

.PHONY: install run run-line run-trace run-curb run-obstacle clean

# install: 仮想環境作成＋依存インストール
install:
	@echo "[MAKE] install: setting up virtual environment and dependencies..."
	@chmod +x $(INSTALL_SCRIPT)
	@$(INSTALL_SCRIPT)

# run: 手追跡モード（デフォルト）
run: install
	@echo "[MAKE] run: launching cam-motion (hand mode)..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT) --mode hand

# run-line: 線検出モード
run-line: install
	@echo "[MAKE] run-line: launching cam-motion (line mode)..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT) --mode line

# run-trace: 空間トレースモード
run-trace: install
	@echo "[MAKE] run-trace: launching cam-motion (trace mode)..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT) --mode trace

# run-curb: 歩道縁取り検出モード
run-curb: install
	@echo "[MAKE] run-curb: launching cam-motion (curb detection mode)..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT) --mode curb

# run-obstacle: 障害物検出モード
run-obstacle: install
	@echo "[MAKE] run-obstacle: launching cam-motion (obstacle detection mode)..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT) --mode detect

# clean: 仮想環境を削除
clean:
	@echo "[MAKE] clean: removing virtual environment..."
	@rm -rf $(VENV)
