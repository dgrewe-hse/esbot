#!/usr/bin/env bash
# Dev container bootstrap: uv, Python deps (incl. Locust), JMeter.
set -euo pipefail

cd /workspace

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
fi

cd backend
uv sync --extra dev

bash /workspace/.devcontainer/scripts/install-jmeter.sh

echo "Dev container ready: uv, Locust, and JMeter installed."
