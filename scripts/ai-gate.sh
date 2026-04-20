#!/bin/bash

# Configuration: Allow script to finish all checks
set +e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

EXIT_CODE=0
SCRIPT_NAME=$(basename "$0")

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}       AI CONTENT INTEGRITY GATE       ${NC}"
echo -e "${BLUE}=======================================${NC}"

run_check() {
    local pattern=$1
    local msg=$2
    local severity=$3
    
    local results=$(grep -rnP "$pattern" . \
        --exclude-dir=.git \
        --exclude-dir=node_modules \
        --exclude="$SCRIPT_NAME" \
        2>/dev/null)

    if [ ! -z "$results" ]; then
        if [ "$severity" == "ERROR" ]; then
            echo -e "${RED}[✖] $msg${NC}"
            EXIT_CODE=1
        else
            echo -e "${YELLOW}[!] $msg${NC}"
        fi
        
        # Format the output to be readable
        echo "$results" | while read -r line; do
            echo -e "    ${YELLOW}→${NC} $line"
        done
        echo ""
    fi
}

# 1. Meta-Questions
run_check '(?m)^\s*\*\*(Do you need me|Would you like me).*\*\*\s*$' "Found AI follow-up questions (unremoved meta-talk)" "ERROR"

# 2. Separators
run_check '(?m)^---$' "Found forbidden horizontal rule separators (---)" "ERROR"

# 3. Typography (AI Dashes)
run_check '[\x{2013}\x{2014}]' "Found LLM-style dashes (—/–). Replace with standard hyphens (-)" "ERROR"

# 4. Invisible Characters
run_check '[\x{200B}-\x{200D}\x{FEFF}]' "Found invisible Unicode characters (Potential AI watermark)" "WARN"

# 5. Transition Phrases
AI_PHRASES="Moreover|Furthermore|In conclusion|It is important to note|Additionally"
run_check "($AI_PHRASES)" "Found transition words highly characteristic of AI writing" "WARN"

# Final Status
echo -e "${BLUE}=======================================${NC}"
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}STATUS: FAILED${NC}"
    echo -e "Please fix the ERRORS listed above to merge your PR."
    exit 1
else
    echo -e "${GREEN}STATUS: PASSED${NC}"
    echo -e "No critical AI artifacts found."
    exit 0
fi