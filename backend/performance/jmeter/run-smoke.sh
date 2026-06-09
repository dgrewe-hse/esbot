#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JMETER_BIN="${JMETER_HOME:-/opt/apache-jmeter}/bin/jmeter"

if ! command -v "${JMETER_BIN}" >/dev/null 2>&1 && ! command -v jmeter >/dev/null 2>&1; then
  if command -v jmeter >/dev/null 2>&1; then
    JMETER_BIN="jmeter"
  else
    echo "JMeter not found. Install Apache JMeter 5.6+ or set JMETER_HOME." >&2
    exit 1
  fi
fi

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
RESULTS_DIR="${SCRIPT_DIR}/results/smoke-${TIMESTAMP}"
mkdir -p "${RESULTS_DIR}"

echo "Running ESBot JMeter smoke test -> ${RESULTS_DIR}"

"${JMETER_BIN}" -n \
  -t "${SCRIPT_DIR}/esbot-smoke-test.jmx" \
  -q "${SCRIPT_DIR}/user.properties" \
  -l "${RESULTS_DIR}/results.jtl" \
  -j "${RESULTS_DIR}/jmeter.log" \
  "$@"

echo "Smoke test finished. Review ${RESULTS_DIR}/results.jtl"
