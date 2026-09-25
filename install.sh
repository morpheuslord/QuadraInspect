#!/usr/bin/env bash
#
# Complete installer for QuadraInspect (Linux / macOS).
#
# One command to go from a fresh clone to a fully working setup:
#   1. install uv (if missing)
#   2. install all Python dependencies (core + the analysis-script extras)
#   3. download and set up every integrated tool and add-on
#
# Usage:
#   ./install.sh            # dependencies + tools + add-ons
#   ./install.sh --deps-only    # only the Python dependencies
#
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

deps_only=0
if [[ "${1:-}" == "--deps-only" ]]; then
    deps_only=1
fi

info() { printf '\033[1;36m[*]\033[0m %s\n' "$1"; }

# 1. Ensure uv is available.
if ! command -v uv >/dev/null 2>&1; then
    info "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Install Python dependencies (core framework + bundled-tool helpers).
info "Installing Python dependencies..."
uv sync --extra tools

if [[ "$deps_only" -eq 1 ]]; then
    info "Dependencies installed. Skipping tools (--deps-only)."
    exit 0
fi

# 3. Install every integrated tool and add-on in one pass.
info "Installing integrated tools and add-ons..."
uv run quadrainspect --mode argm --command full-install

info "Complete installation finished."
info "Run 'uv run quadrainspect' to start."
