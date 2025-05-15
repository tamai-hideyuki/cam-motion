# Makefile for cam-motion

# デフォルトターゲット
.DEFAULT_GOAL := run

# 仮想環境のディレクトリ
VENV           := venv
INSTALL_SCRIPT := scripts/install_deps.sh
RUN_SCRIPT     := scripts/run.sh

.PHONY: install run run-line clean

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

# clean: 仮想環境を削除
clean:
	@echo "[MAKE] clean: removing virtual environment..."
	@rm -rf $(VENV)
