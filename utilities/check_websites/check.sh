#!/bin/bash

basepath=$(cd $(dirname $0);pwd)
declare -a websites		#Store website
test -d ${basepath}/logs || mkdir ${basepath}/logs
# Read configuration from WebSite.conf
getWebSite(){
    count=0
    while read website
    do
    	if [[ ${website} =~ ^http.*$ ]];then
    		websites[$count]=${website}
			count=$((count+1))
    	fi
    done < ${basepath}/WebSites.conf
}

# Check website's availability
checkAllSites(){
	for ws in ${websites[*]};do
		checkSite $ws	
	done
}

# Check Single website
# If occur an error,echo error to logs,and send e-mail to admin.
checkSite(){

	#Get response's status code.
	http_code=$(curl -s -w "%{http_code}" -I ${1} -m 10 -o /dev/null)

	#http_location is used for 30X redirect.
    http_location=$(curl -s -I ${1} -m 10 | grep "Location" | awk '{print $2}' | cat -A | tr -d '^M$' )
    now_date=$(date +"%F %T")
    if [[ http_code -eq 200 ]];then
    	echo "INFO:${1} STATUS:${http_code} ${now_date}" >> ${basepath}/logs/$(date +"%F").info.log
    elif [[ ${http_code} =~ ^3[0-9]{2}$ ]];then
    	checkSite $http_location		
    else
    	echo "ERROR:${1} STATUS:${http_code} ${now_date}" >> ${basepath}/logs/$(date +"%F").error.log
		sendmail "${1}" "${now_date}"
    fi		
}

# Call python module to  send email
sendmail(){
	${basepath}/send.py "${1}" "${2}" &>/dev/null && echo "Send Warning message. ${2}" 
}

main(){
	getWebSite
	checkAllSites
}
main
