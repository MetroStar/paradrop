#!/bin/sh

if [ "$(pgrep systemd -c)" -ge 2 ]; then
  INIT="systemd"
else
  INIT="other"
fi

if [ "$INIT" = "systemd" ]; then
  systemctl stop paradrop-agent
  rm -rf /etc/systemd/system/paradrop-agent.service /etc/metrostar/paradrop-agent /usr/bin/paradrop-agent
  systemctl daemon-reload
fi

if [ "$INIT" = "other" ]; then
  /etc/init.d/paradrop-agent stop
  chkconfig paradrop-agent off
  rm -rf /etc/init.d/paradrop-agent /etc/metrostar/paradrop-agent /usr/bin/paradrop-agent
fi
