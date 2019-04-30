#!/bin/bash

custom_echo(){
	echo -e "${1}"
	echo "=========================================================================================="
}
echo '=========================================================================================='
#realease version
version=$(cat /etc/redhat-release)
custom_echo  "Realse Version:$version"
#architecture
architecture=$(uname -m)
custom_echo  "Architecture:$architecture"
#kernel release
kernel=$(uname -r)
custom_echo  "Kernel Version:$kernel"
#internal ip
interip=$(hostname -I)
custom_echo  "Internal IP:$interip"
#external ip
exterip=$(curl -s -m 5 ip.cn | awk -F'[ ：]' '{print $3}')
custom_echo  "External IP:$exterip"
#dns
dns=$(cat /etc/resolv.conf | grep -E '\<nameserver' | awk '{print $NF}')
custom_echo  "DNS:\n$dns"
#Check if connected to internet
ping -c 3 baidu.com &>/dev/null && connect="online" || connect="offline"
custom_echo  "Connection Status:$connect"
#Check login User
who > /tmp/who.txt
[[ -f /tmp/who.txt ]] && custom_echo "All Users:\n$(cat /tmp/who.txt)"
rm -rf /tmp/who.txt

#Check cpuinfo
cpuname=$(cat /proc/cpuinfo | grep "model name" | sort -u | awk -F':' '{print $2}')
corenum=$(cat /proc/cpuinfo | grep "core id" | sort -u | wc -l)
threadnum=$(cat /proc/cpuinfo | grep "processor" | sort -u | wc -l)
custom_echo  "CPU Info:$cpuname ${corenum} x Core ${threadnum} x Thread "

#custom_echo meminfo
freepath="/tmp/meminfo$(date +'%F%H%M%S')\.txt"
free -mh > ${freepath}
[[ -f ${freepath} ]] && custom_echo "Memory Info:$(cat ${freepath})"

#check adapter info
adapter=$(lspci | grep "Ethernet" | awk -F': ' '{print $2}')
custom_echo "Adapter Info:\n${adapter}"


#custom_echo disk info
diskinfo=$(df -hP | grep -vE 'tmpfs' | awk 'NR!=1{print}')
custom_echo  "Disk Info:\n${diskinfo}"

#custom_echo load average
loadavg=$(w|head -1 |awk -F':' '{print $NF}')
custom_echo  "Load Average:${loadavg}"
