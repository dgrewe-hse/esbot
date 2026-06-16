#!/usr/bin/env bash
# Resolve JMeter binary: JMETER_HOME, common install paths, or PATH.

resolve_jmeter_bin() {
  if [[ -n "${JMETER_HOME:-}" && -x "${JMETER_HOME}/bin/jmeter" ]]; then
    echo "${JMETER_HOME}/bin/jmeter"
    return 0
  fi
  for install_dir in /opt/apache-jmeter /opt/jmeter; do
    if [[ -x "${install_dir}/bin/jmeter" ]]; then
      echo "${install_dir}/bin/jmeter"
      return 0
    fi
  done
  if command -v jmeter >/dev/null 2>&1; then
    echo "jmeter"
    return 0
  fi
  return 1
}
