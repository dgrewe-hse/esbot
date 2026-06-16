#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jmeter-env.sh
source "${SCRIPT_DIR}/jmeter-env.sh"

if ! JMETER_BIN="$(resolve_jmeter_bin)"; then
  echo "JMeter not found. Install Apache JMeter 5.6+ or set JMETER_HOME." >&2
  echo "  Dev container: rebuild or run bash .devcontainer/scripts/install-jmeter.sh" >&2
  exit 1
fi

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="${SCRIPT_DIR}/results/load-${TIMESTAMP}"
mkdir -p "${RESULTS_DIR}"

echo "Running ESBot JMeter load test -> ${RESULTS_DIR}"
echo "  jmeter=${JMETER_BIN}"
echo "Defaults: 50 users, 60s ramp, 300s duration (override via -Jload.threads=...)"

"${JMETER_BIN}" -n \
  -t "${SCRIPT_DIR}/esbot-load-test.jmx" \
  -q "${SCRIPT_DIR}/user.properties" \
  -l "${RESULTS_DIR}/results.jtl" \
  -j "${RESULTS_DIR}/jmeter.log" \
  -e -o "${RESULTS_DIR}/html-report" \
  "$@"

echo "Load test finished."
echo "  JTL: ${RESULTS_DIR}/results.jtl"
echo "  HTML report: ${RESULTS_DIR}/html-report/index.html"
