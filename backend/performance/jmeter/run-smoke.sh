#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jmeter-env.sh
source "${SCRIPT_DIR}/jmeter-env.sh"

if ! JMETER_BIN="$(resolve_jmeter_bin)"; then
  echo "JMeter not found. Install Apache JMeter 5.6+ or set JMETER_HOME." >&2
  echo "  Dev container: rebuild or run bash .devcontainer/scripts/install-jmeter.sh" >&2
  echo "  Manual install:  export JMETER_HOME=/path/to/apache-jmeter" >&2
  exit 1
fi

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="${SCRIPT_DIR}/results/smoke-${TIMESTAMP}"
mkdir -p "${RESULTS_DIR}"

echo "Running ESBot JMeter smoke test -> ${RESULTS_DIR}"
echo "  jmeter=${JMETER_BIN}"

"${JMETER_BIN}" -n \
  -t "${SCRIPT_DIR}/esbot-smoke-test.jmx" \
  -q "${SCRIPT_DIR}/user.properties" \
  -l "${RESULTS_DIR}/results.jtl" \
  -j "${RESULTS_DIR}/jmeter.log" \
  "$@"

echo "Smoke test finished. Review ${RESULTS_DIR}/results.jtl"
