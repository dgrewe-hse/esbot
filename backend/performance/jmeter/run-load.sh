#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JMETER_BIN="${JMETER_HOME:-/opt/apache-jmeter}/bin/jmeter"

if ! command -v "${JMETER_BIN}" >/dev/null 2>&1 && command -v jmeter >/dev/null 2>&1; then
  JMETER_BIN="jmeter"
elif ! command -v "${JMETER_BIN}" >/dev/null 2>&1; then
  echo "JMeter not found. Install Apache JMeter 5.6+ or set JMETER_HOME." >&2
  exit 1
fi

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="${SCRIPT_DIR}/results/load-${TIMESTAMP}"
mkdir -p "${RESULTS_DIR}"

echo "Running ESBot JMeter load test -> ${RESULTS_DIR}"
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
