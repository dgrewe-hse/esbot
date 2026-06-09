#!/usr/bin/env bash
# Install Apache JMeter for ESBot performance testing (idempotent).
set -euo pipefail

JMETER_VERSION="${JMETER_VERSION:-5.6.3}"
INSTALL_DIR="${JMETER_HOME:-/opt/apache-jmeter}"
ARCHIVE="apache-jmeter-${JMETER_VERSION}.tgz"
DOWNLOAD_URL="https://dlcdn.apache.org/jmeter/binaries/${ARCHIVE}"

if [[ -x "${INSTALL_DIR}/bin/jmeter" ]]; then
  echo "JMeter already installed at ${INSTALL_DIR}"
  exit 0
fi

echo "Installing Apache JMeter ${JMETER_VERSION} to ${INSTALL_DIR}..."
tmpdir="$(mktemp -d)"
trap 'rm -rf "${tmpdir}"' EXIT

curl -fsSL -o "${tmpdir}/${ARCHIVE}" "${DOWNLOAD_URL}"
mkdir -p "${INSTALL_DIR}"
tar -xzf "${tmpdir}/${ARCHIVE}" -C "${INSTALL_DIR}" --strip-components=1

cat >/etc/profile.d/jmeter.sh <<EOF
export JMETER_HOME=${INSTALL_DIR}
export PATH="\${JMETER_HOME}/bin:\${PATH}"
EOF

echo "JMeter installed: $("${INSTALL_DIR}/bin/jmeter" --version 2>&1 | tail -1)"
