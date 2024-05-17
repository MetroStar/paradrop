#!/bin/sh

if [ "$1" = "" ]; then
  echo "First argument empty, need version"
  exit 1
fi

mkdir -p /etc/paradrop

cp -f ./paradrop-agent.service /etc/paradrop/
cp -f ../paradrop-agent /etc/paradrop/

cat <<'EOF'>/etc/paradrop/paradrop-agent.yaml.orig
api_url: https://localhost:8443/v1/add-host
api_username:
api_token:
api_insecure_ssl:
oscap_xccdf_xml:
tags: []
EOF

fpm -t deb -s dir -n paradrop-agent -v "$1" -a amd64 -p "paradrop-agent-$1-amd64.deb" --license GPLv3 --vendor Perlogix -m paradrop@metrostar.com --url "https://github.com/MetroStar/paradrop" --description "MetroStar paradrop-agent binary distribution" --after-install ./install.sh --after-remove ./uninstall.sh --deb-no-default-config-files /etc/paradrop
fpm -t rpm -s dir -n paradrop-agent -v "$1" -a amd64 -p "paradrop-agent-$1-amd64.rpm" --license GPLv3 --vendor Perlogix -m paradrop@metrostar.com --url "https://github.com/MetroStar/paradrop" --description "MetroStar paradrop-agent binary distribution" --after-install ./install.sh --after-remove ./uninstall.sh /etc/paradrop
