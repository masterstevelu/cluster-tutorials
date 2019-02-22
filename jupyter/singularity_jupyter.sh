#!/bin/bash

exist_jupyter=`qstat | grep singularity_jupyter | grep " R "`
if [[ $exist_jupyter == *"singularity_jupyter"* ]]; then
	exist_arr=(${exist_jupyter//./ })
	exist_jobid=${exist_arr[0]}
	echo "singularity_jupyter job exists!"
	cat log/tunnel.$exist_jobid.rmdx-cluster.edu.com.cn
	exit
fi

# get input

# get input
while :; do
  read -p "Enter singularity image path: " image_path
  echo $image_path
  if [ -f $image_path ]; then
    echo "Image exists!"
    break
  else
    echo "No image on the path : $image_path , try again!"
  fi
done

while :; do
  read -p "Enter a number between 9001 and 9999: " port_number
  [[ $port_number =~ ^[0-9]+$ ]] || { echo "Enter a valid port_number"; continue; }
  if ((port_number >= 9001 && port_number <= 9999)); then
    echo "valid port_number"
    break
  else
    echo "number out of range, try again!"
  fi
done

sub=`qsub -v IMAGE=$image_path,PORT=$port_number submit_singularity_jupyter.pbs`
sub_arr=(${sub//./ })
jobid=${sub_arr[0]}
sleep 6 

echo "log/tunnel.$jobid.rmdx-cluster.edu.com.cn" 
if [ -f log/tunnel.$jobid.rmdx-cluster.edu.com.cn ]; then
    cat log/tunnel.$jobid.rmdx-cluster.edu.com.cn
fi
if [ -f log/port_in_use ]; then
    cat log/port_in_use
    rm log/port_in_use
fi
