#!/bin/bash

RESETTEM=$(tput sgr0)
#检查Web Server是否正常运行
check_web_server(){
	status_code=$(curl -I -s -m 5 -w %{http_code} ${1} -o /dev/null)
	if [ ${status_code} -eq 000 -o ${status_code} -ge 500 ];then
		echo -e "\e[1;31mERROR:Web server occur an error.CODE:$status_code" 
	else
		echo -e "\e[1;35mINFO:Web server is running.CODE:$status_code"
	fi
	echo -e "${RESETTEM}\c"
}

#Mysql主从备份状态检查
mysql_slave_server=""
check_mysql_server(){
	nc -z -w2 ${mysql_slave_server} 3306
}


