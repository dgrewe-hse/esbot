#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "Running ESBot Gatling smoke simulation against ${BASE_URL}"

mvn -f "${SCRIPT_DIR}/pom.xml" \
  -DbaseUrl="${BASE_URL}" \
  -Dgatling.runMultipleSimulations=false \
  -Dgatling.simulationClass=esbot.ESBotSmokeSimulation \
  gatling:test
