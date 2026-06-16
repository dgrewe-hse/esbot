#!/usr/bin/env bash
# ESBot REST API workflow test via curl.
#
# Runs a happy-path learning session flow plus key negative checks.
# Mirrors scenarios in tests/integration/api/.
#
# Usage:
#   ./tests/test_api_workflow.sh
#   BASE_URL=http://localhost:8000 ./tests/test_api_workflow.sh
#
# Requires: curl, and jq OR python3 for JSON parsing.

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
USER_ID="${USER_ID:-curl-test-user}"
PASS=0
FAIL=0

# --- helpers -----------------------------------------------------------------

die() {
  echo "ERROR: $*" >&2
  exit 1
}

have_jq() { command -v jq >/dev/null 2>&1; }

json_get() {
  local json="$1" key="$2"
  if have_jq; then
    echo "${json}" | jq -r "${key}"
  else
    python3 -c "import json,sys; d=json.load(sys.stdin); print(${key})" <<<"${json}"
  fi
}

assert_status() {
  local name="$1" expected="$2" actual="$3" body="${4:-}"
  if [[ "${actual}" == "${expected}" ]]; then
    echo "  PASS  ${name} (HTTP ${actual})"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  ${name} — expected HTTP ${expected}, got ${actual}" >&2
    [[ -n "${body}" ]] && echo "        body: ${body}" >&2
    FAIL=$((FAIL + 1))
  fi
}

curl_json() {
  local method="$1" url="$2"
  shift 2
  curl -sS -w "\n%{http_code}" -X "${method}" "${url}" "$@"
}

# body is all lines except last; status is last line
split_response() {
  local raw="$1"
  HTTP_BODY="$(echo "${raw}" | sed '$d')"
  HTTP_CODE="$(echo "${raw}" | tail -n 1)"
}

# --- checks ------------------------------------------------------------------

echo "ESBot API workflow test"
echo "  base_url=${BASE_URL}"
echo

# 1. Health
raw="$(curl_json GET "${BASE_URL}/api/v1/health")"
split_response "${raw}"
assert_status "GET /api/v1/health" 200 "${HTTP_CODE}" "${HTTP_BODY}"
status="$(json_get "${HTTP_BODY}" '.status')"
[[ "${status}" == "ok" ]] && echo "        status=${status}" || die "health status not ok"

# 2. Negative: invalid session create
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"","title":"Invalid"}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions (empty user_id)" 422 "${HTTP_CODE}"

# 3. Create session
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"${USER_ID}\",\"title\":\"Curl Workflow Test\"}")"
split_response "${raw}"
assert_status "POST /api/v1/sessions" 201 "${HTTP_CODE}" "${HTTP_BODY}"
[[ "${HTTP_CODE}" == "201" ]] || exit 1
SESSION_ID="$(json_get "${HTTP_BODY}" '.id')"
[[ -n "${SESSION_ID}" && "${SESSION_ID}" != "null" ]] || die "no session id in create response"
echo "        session_id=${SESSION_ID}"

# 4. Get session
raw="$(curl_json GET "${BASE_URL}/api/v1/sessions/${SESSION_ID}")"
split_response "${raw}"
assert_status "GET /api/v1/sessions/{id}" 200 "${HTTP_CODE}"

# 5. List sessions
raw="$(curl_json GET "${BASE_URL}/api/v1/sessions?user_id=${USER_ID}")"
split_response "${raw}"
assert_status "GET /api/v1/sessions?user_id=" 200 "${HTTP_CODE}"

# 6. Send message
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${SESSION_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"content":"What is equivalence partitioning?"}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{id}/messages" 201 "${HTTP_CODE}" "${HTTP_BODY}"
assistant_role="$(json_get "${HTTP_BODY}" '.assistant_message.role')"
[[ "${assistant_role}" == "assistant" ]] || die "expected assistant role, got ${assistant_role}"

# 7. Message history
raw="$(curl_json GET "${BASE_URL}/api/v1/sessions/${SESSION_ID}/messages")"
split_response "${raw}"
assert_status "GET /api/v1/sessions/{id}/messages" 200 "${HTTP_CODE}" "${HTTP_BODY}"
if have_jq; then
  msg_count="$(echo "${HTTP_BODY}" | jq '.messages | length')"
else
  msg_count="$(python3 -c "import json,sys; print(len(json.load(sys.stdin)['messages']))" <<<"${HTTP_BODY}")"
fi
[[ "${msg_count}" -ge 2 ]] || die "expected at least 2 messages, got ${msg_count}"
echo "        messages=${msg_count}"

# 8. Negative: empty message content
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${SESSION_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"content":"   "}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{id}/messages (blank content)" 422 "${HTTP_CODE}"

# 9. Generate quiz
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${SESSION_ID}/quiz" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Software Testing","count":2}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{id}/quiz" 201 "${HTTP_CODE}" "${HTTP_BODY}"
QUESTION_ID="$(json_get "${HTTP_BODY}" '.items[0].id')"
CORRECT_ANSWER="$(json_get "${HTTP_BODY}" '.items[0].correct_answer')"
[[ -n "${QUESTION_ID}" && "${QUESTION_ID}" != "null" ]] || die "no question id in quiz response"
echo "        question_id=${QUESTION_ID}"

# 10. Negative: empty quiz topic
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${SESSION_ID}/quiz" \
  -H "Content-Type: application/json" \
  -d '{"topic":"  "}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{id}/quiz (blank topic)" 422 "${HTTP_CODE}"

# 11. Submit correct answer
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${SESSION_ID}/quiz/${QUESTION_ID}/answer" \
  -H "Content-Type: application/json" \
  -d "{\"answer\":\"${CORRECT_ANSWER}\"}")"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{id}/quiz/{qid}/answer" 200 "${HTTP_CODE}" "${HTTP_BODY}"
is_correct="$(json_get "${HTTP_BODY}" '.is_correct')"
[[ "${is_correct}" == "true" ]] || die "expected is_correct=true, got ${is_correct}"

# 12. Negative: session not found
UNKNOWN_ID="$(python3 -c 'import uuid; print(uuid.uuid4())')"
raw="$(curl_json GET "${BASE_URL}/api/v1/sessions/${UNKNOWN_ID}")"
split_response "${raw}"
assert_status "GET /api/v1/sessions/{unknown}" 404 "${HTTP_CODE}"

# 13. Negative: message on unknown session
raw="$(curl_json POST "${BASE_URL}/api/v1/sessions/${UNKNOWN_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello"}')"
split_response "${raw}"
assert_status "POST /api/v1/sessions/{unknown}/messages" 404 "${HTTP_CODE}"

# 14. Delete session
HTTP_CODE="$(curl -sS -o /dev/null -w "%{http_code}" -X DELETE \
  "${BASE_URL}/api/v1/sessions/${SESSION_ID}")"
assert_status "DELETE /api/v1/sessions/{id}" 204 "${HTTP_CODE}"

# 15. Deleted session gone
raw="$(curl_json GET "${BASE_URL}/api/v1/sessions/${SESSION_ID}")"
split_response "${raw}"
assert_status "GET /api/v1/sessions/{id} after delete" 404 "${HTTP_CODE}"

# --- summary -----------------------------------------------------------------

echo
echo "Results: ${PASS} passed, ${FAIL} failed"
if [[ "${FAIL}" -gt 0 ]]; then
  exit 1
fi
echo "All API workflow checks passed."
