#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://localhost:8000}"
STRESS_USERS="${STRESS_USERS:-200}"
STRESS_RAMP_SECONDS="${STRESS_RAMP_SECONDS:-600}"
STRESS_DURATION_SECONDS="${STRESS_DURATION_SECONDS:-900}"

echo "WARNING: Stress simulation ramps up to ${STRESS_USERS} users."
read -r -p "Continue? [y/N] " CONFIRM
if [[ ! "${CONFIRM}" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

echo "Running ESBot Gatling stress simulation against ${BASE_URL}"

mvn -f "${SCRIPT_DIR}/pom.xml" \
  -DbaseUrl="${BASE_URL}" \
  -DstressUsers="${STRESS_USERS}" \
  -DstressRampSeconds="${STRESS_RAMP_SECONDS}" \
  -DstressDurationSeconds="${STRESS_DURATION_SECONDS}" \
  -Dgatling.runMultipleSimulations=false \
  -Dgatling.simulationClass=esbot.ESBotStressSimulation \
  gatling:test
