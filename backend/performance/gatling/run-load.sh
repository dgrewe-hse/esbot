#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://localhost:8000}"
LOAD_USERS="${LOAD_USERS:-50}"
LOAD_RAMP_SECONDS="${LOAD_RAMP_SECONDS:-60}"
LOAD_DURATION_SECONDS="${LOAD_DURATION_SECONDS:-300}"

echo "Running ESBot Gatling load simulation against ${BASE_URL}"
echo "  users=${LOAD_USERS} ramp=${LOAD_RAMP_SECONDS}s duration=${LOAD_DURATION_SECONDS}s"

mvn -f "${SCRIPT_DIR}/pom.xml" \
  -DbaseUrl="${BASE_URL}" \
  -DloadUsers="${LOAD_USERS}" \
  -DloadRampSeconds="${LOAD_RAMP_SECONDS}" \
  -DloadDurationSeconds="${LOAD_DURATION_SECONDS}" \
  -Dgatling.runMultipleSimulations=false \
  -Dgatling.simulationClass=esbot.ESBotLoadSimulation \
  gatling:test
