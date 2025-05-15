# Makefile for cam-motion

# デフォルトターゲット
.DEFAULT_GOAL := run

# 仮想環境のディレクトリ
VENV := venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip
INSTALL_SCRIPT := scripts/install_deps.sh
RUN_SCRIPT := scripts/run.sh

.PHONY: install run clean

# install: 仮想環境作成＋依存インストール
install:
	@echo "[MAKE] install: setting up virtual environment and dependencies..."
	@chmod +x $(INSTALL_SCRIPT)
	@$(INSTALL_SCRIPT)

# run: install の後に実行スクリプトを起動
run: install
	@echo "[MAKE] run: launching cam-motion..."
	@chmod +x $(RUN_SCRIPT)
	@$(RUN_SCRIPT)

# clean: 仮想環境を削除
clean:
	@echo "[MAKE] clean: removing virtual environment..."
	@rm -rf $(VENV)
