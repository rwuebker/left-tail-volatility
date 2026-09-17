#!/bin/sh
set -eu
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$PROJECT_ROOT"
export PATH="$PROJECT_ROOT/.tools/codex-adapter/node_modules/.bin:$PATH"
export JUPYTER_RUNTIME_DIR="$PROJECT_ROOT/.uv-cache/jupyter-ai-runtime"
export JUPYTER_CONFIG_DIR="$PROJECT_ROOT/.uv-cache/jupyter-config"
export IPYTHONDIR="$PROJECT_ROOT/.uv-cache/ipython"
export MPLCONFIGDIR="$PROJECT_ROOT/.uv-cache/matplotlib"
exec .venv/bin/python -m jupyterlab --no-browser --ip=127.0.0.1 --port=8889 --ServerApp.port_retries=0 --ServerApp.root_dir="$PROJECT_ROOT" --ServerApp.default_url=/lab/tree/notebooks/01_garch_foundations.ipynb
