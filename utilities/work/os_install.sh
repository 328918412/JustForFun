#!/bin/bash
# 1.Generate ssh public key:
ssh-keygen -t rsa -C "N0mansky"

# Current NIC name.
curr_nic="/etc/sysconfig/network-scripts/ifcfg-ens33"

echo "==================Installing Software=================="
# Installing software
yum -y install openssh openssh-server
yum -y install vim
yum -y install git
yum -y install tcpdump
yum -y install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
yum -y install wget
yum -y install mysql
yum -y install iptables-services
yum -y install dosfstools
yum -y install tmux
yum -y install tree
yum -y install htop
systemctl stop firewalld
systemctl disable firewalld
systemctl start iptables
systemctl enable iptables
echo "==================Installed Software==================="

echo "==================Modifying Configuration==================="
# Modifying vim configuration.
echo "set number
set tabstop=4
set shiftwidth=4
set autoindent
set cindent" > ~/.vimrc
sed -i 's/^alias.*/#&/' ~/.bashrc
echo "==================Modified Configuration===================="

# Git clone. 
mkdir ~/workspace
cd ~/workspace
git clone git@git.coding.net:nomansky/PersonalRepo.git

# Install python3.6
mkdir -p /usr/src/local && cd /usr/src/local
wget http://mirrors.sohu.com/python/3.6.3/Python-3.6.3.tgz
tar zxvf Python-3.6.3.tgz && cd Python-3.6.3
mkdir /usr/local/python3
./configure --prefix=/usr/local/python3
make && make install
ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
ln -s /usr/local/python3/bin/pyvenv-3.6 /usr/bin/pyvenv

# Install kvm
sed -i 's/=enforcing/=disabled/' /etc/sysconfig/selinux
yum -y install epel-release zip
yum -y install qemu-kvm libvirt virt-install bridge-utils 
systemctl restart libvirtd
# Backup NIC file
file_names=$(ls /etc/sysconfig/network-scripts/ifcfg-*)
for file in ${file_names};do
	cp ${file} "${file}.$(date +%F).bak"
done
br_nic="/etc/sysconfig/network-scripts/ifcfg-br0"
echo "BOOTPROTO=static
DEVICE=br0
TYPE=Bridge
NM_CONTROLLED=no" >> ${br_nic}
grep DNS1 $curr_nic >> ${br_nic}
grep NETMASK $curr_nic >> ${br_nic}
grep IPADDR $curr_nic >> ${br_nic}
grep GATEWAY $curr_nic >> ${br_nic}

rm -rf $curr_nic
temp_curr_nic_name=$(basename $curr_nic)
curr_nic_name=${temp_curr_nic_name#*-}
echo "TYPE=Ethernet
NAME=${curr_nic_name}
DEVICE=${curr_nic_name}
ONBOOT=yes
BRIDGE=br0
DEFROUTE=yes
NM_CONTROLLED=no" >> $curr_nic

# Install MySQL

# Modify pip source
mkdir -p ~/.pip/ && echo "[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf
