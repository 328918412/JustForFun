#!/bin/bash


resettem=$(tput sgr0)		#设置重置屏幕
declare -A ssharray			#联合数组
key=0						#数组key初始化为0
numbers=""					#提示信息字符串


if [[ $# -eq 0 ]];then
	#Iterate all file and print it,except monitor.sh
	for script_name in $(ls -I "monitor*" -I "*.txt" ./);do
		echo -e '\e[1;35m' "The script:${key} ==>${resettem} ${script_name}"
		ssharray[$key]=$script_name
		numbers="$numbers $key"
		key=$((key+1))
	done
	numbers="$numbers "

	#Get Input str,if str isn't a number ,exit.
	while true;do
		read -p "Please enter a number in [$numbers],or enter Q/q quit:" execnum

		#If input value is q or Q,then exit script.
		if [[ ${execnum} == 'q' || ${execnum} == 'Q' ]];then
			echo "Bye."
			exit 0

		#If input value isn't a number,print error msg.
		elif [[ ! ${execnum} =~ ^[0-9]+ ]];then
			echo -e "\e[1;31mERROR:Not a number!${resettem}"
			continue

		#If shell dosen't exists,print error msg.
		else
			shellname="./${ssharray[${execnum}]}"
			[ -f ${shellname} ] && /bin/bash ${shellname} || echo -e '\e[1;31m'"ERROR:File dosen't exist!" ${resettem}
		fi
	done
else
	echo -e '\e[1;31m'"ERROR:No parameters required!" ${resettem}
	exit 1
fi
