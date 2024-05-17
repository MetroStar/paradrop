#!/bin/sh

mkdir -p /etc/paradrop

mv -f /etc/paradrop/paradrop-agent /usr/bin/paradrop-agent
chmod -f 0755 /usr/bin/paradrop-agent

if [ ! -e /etc/paradrop/paradrop-agent.yaml ]; then
  cp -f /etc/paradrop/paradrop-agent.yaml.orig /etc/paradrop/paradrop-agent.yaml
fi

if [ "$(pgrep systemd -c)" -ge 2 ]; then
  INIT="systemd"
else
  INIT="other"
fi

if [ "$INIT" = "systemd" ]; then
  cp -f /etc/paradrop/paradrop-agent.service /etc/systemd/system/paradrop-agent.service
  systemctl daemon-reload
  systemctl restart paradrop-agent
fi

if [ "$INIT" = "other" ]; then
  cp -f /etc/paradrop/paradrop-agent.init /etc/init.d/paradrop-agent
  chmod -f 0755 /etc/init.d/paradrop-agent
  chkconfig paradrop-agent on
  /etc/init.d/paradrop-agent restart
fi
