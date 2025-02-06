#!/bin/bash

usage() {
  echo "usage: $0 <mid-clientid> <storageacct-name> <share-name> <mountpoint> <resource-group>"
  exit 1
}

assert() {
  echo "ERROR: ${1}"
  exit 1
}

next_log() {
	cnt=0
	log_path=/tmp/mount-storageacct.$$-${cnt}.log
	while [ -f ${log_path} ]; do
		((cnt++))
		log_path=/tmp/mount-storageacct.$$-${cnt}.log
	done

	echo "${log_path}"
}

run_cmd() {
	if [ $# -ne 2 ]; then return 0; fi
	title=${1}
	cmd=${2}

	log=$(next_log)
	echo -n "--> ${title}"
	echo "--> Executing: ${cmd} " > ${log} 2>&1
	eval ${cmd} >> ${log} 2>&1
	if [ $? -ne 0 ]; then
		echo " (failed | log = ${log})"
		return 1
	fi
	echo " (succeeded | log = ${log})"
	return 0
}

# validate commandline args
if [ $# -ne 5 ]; then usage; fi

# process commandline args
clientid=${1}
storageacct=${2}
share=${3}
mountpoint=${4}
rg=${5}

# login to Azure using managed identity
run_cmd "logging into Azure" "az login --identity --client-id ${clientid}"
if [ $? -ne 0 ]; then assert "failed to login to Azure"; fi


# lookup storage account access key
accesskey=$(az storage account keys list --account-name ${storageacct} --resource-group ${rg} --query [0].value --output tsv)
if [ $? -ne 0 ]; then assert "failed to get access key for storage account"; fi

# install cifs utilities
run_cmd "installing package: cifs-utils" "sudo yum install -y cifs-utils"
if [ $? -ne 0 ]; then assert "failed to install cifs utilities"; fi

# create mountpoint
run_cmd "creating mountpoint" "mkdir -p ${mountpoint}"
if [ $? -ne 0 ]; then assert "failed to create mountpoint"; fi

# mount storage account share
uid=$(id -u)
gid=$(id -g)
run_cmd "mounting cifs share" "sudo mount -t cifs //${storageacct}.file.core.windows.net/${share} ${mountpoint} -o uid=${uid},gid=${gid} -o username=${storageacct} -o password=${accesskey}"
if [ $? -ne 0 ]; then assert "failed to mount storage account share"; fi

# exit cleanly
exit 0
