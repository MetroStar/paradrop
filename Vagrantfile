# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/jammy64"
    config.vm.hostname = "paradrop-ubuntu22-01"
    config.vm.provider "virtualbox" do |v|
        v.name = "paradrop-ubuntu22-01"
        v.memory = 8192
        v.cpus = 4
        v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
    end
    config.vm.network "forwarded_port", guest: 8443, host: 8443
    config.vm.network "forwarded_port", guest: 9200, host: 9200
    config.vm.network "forwarded_port", guest: 5601, host: 5601
    config.vm.synced_folder ".", "/paradrop", SharedFoldersEnableSymlinksCreate: true
    config.vm.provision "shell", inline: <<-SHELL
# Setup Elastic sysctl Params
sysctl -w vm.max_map_count=262144
sysctl -w vm.swappiness=10
sysctl -w net.ipv4.tcp_retries2=5

# Setup Security File Limits
cat <<'EOF' >/etc/security/limits.d/99-limits.conf
* soft nofile 999999
* hard nofile 999999
root soft nofile 999999
root hard nofile 999999

* soft stack unlimited
* hard stack unlimited
root soft stack unlimited
root hard stack unlimited
EOF

# Setup NodeJS v18
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

# Setup Base Packages
ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get update -y
ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get remove -y whoopsie apport apport-gtk ubuntu-report unattended-upgrades kerneloops plymouth thunderbird transmission-common cheese aisleriot gnome-mahjongg gnome-mines gnome-sudoku remmina mlocate
ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get autoremove -y
ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get install -y curl jq vim net-tools dnsutils screen nodejs python3-pip python3-dev make unzip htop clamav libopenscap8 dmidecode shellcheck wget apt-transport-https gnupg lsb-release

# Setup Docker
curl -fsSL https://get.docker.com -o ./get-docker.sh
sh ./get-docker.sh
rm ./get-docker.sh

systemctl enable docker
systemctl restart docker

# Install Trivy Scanner
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
apt-get update
apt-get install trivy

# Install OpenScap Content Guides
curl -OLs https://github.com/ComplianceAsCode/content/releases/download/v0.1.72/scap-security-guide-0.1.72.zip
unzip scap-security-guide-0.1.72.zip
mkdir -p /usr/share/scap-security-guide
cp -rf scap-security-guide-0.1.72/* /usr/share/scap-security-guide/
rm -rf scap-security-guide-0.1.72*

# Install Python Deps
cd /paradrop
make pip
pip3 install flake8

# Setup Golang
GOVER="1.22.3"
curl -OLs "https://golang.org/dl/go$GOVER.linux-amd64.tar.gz"
tar -zxf ./"go$GOVER.linux-amd64.tar.gz"
mv -f ./go /usr/local/
rm -f ./"go$GOVER.linux-amd64.tar.gz"
ln -s /usr/local/go/bin/go /usr/bin/go

# Setup Golang Env & Build Agent
mkdir -p /home/vagrant/go/{src/github.com/Metrostar,bin,pkg}
ln -s /paradrop/agent /home/vagrant/go/src/github.com/Metrostar/paradrop
chown -Rf vagrant:vagrant /home/vagrant
export GOPATH=/home/vagrant/go
cd /home/vagrant/go/src/github.com/Metrostar/paradrop
make
chmod -f 0755 ./paradrop-agent

# Run paradrop Stack
cd /paradrop
make local

# Setup paradrop-agent
mkdir -p /etc/paradrop

cat <<'EOF'>/etc/paradrop/paradrop-agent.yaml
api_url: https://localhost:8443/v1/add-host
api_username: admin@paradrop.io
api_token: b97a81c5-3c2b-4a96-8881-38af26dc8407
api_insecure_ssl: true
tags: ["app=paradrop-agent-vagrant","health=https://localhost:8443/v1/health"]
oscap_xccdf_xml: "/usr/share/scap-security-guide/ssg-ubuntu2204-ds.xml"
EOF

cp -f /paradrop/agent/paradrop-agent /usr/bin/

timeout 200 paradrop-agent -d

# Restart
systemctl reboot
SHELL
    end
