# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/jammy64"
    config.vm.hostname = "ubuntu22"
    config.vm.provider "virtualbox" do |v|
        v.name = "ubuntu22"
        v.memory = 4096
        v.cpus = 2
        v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
    end
    config.vm.network "forwarded_port", guest: 443, host: 8443
    config.vm.network "forwarded_port", guest: 9200, host: 9200
    config.vm.network "forwarded_port", guest: 9300, host: 9300
    config.vm.synced_folder ".", "/home/vagrant/paradrop"
    config.vm.provision "shell", inline: <<-SHELL
    apt-get update -y
    apt-get upgrade -y
    apt-get install -y curl nodejs npm python3-pip python3-dev docker.io docker-compose make
    systemctl enable docker
    systemctl start docker
SHELL
end
