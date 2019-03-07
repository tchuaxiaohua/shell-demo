#!/bin/bash

#HOST='172.16.223.54'
HOST='172.16.11.248'
PORT='6379'
CLIENT="redis-cli -h $HOST -p $PORT"
FILE_NAME="$1"

if [ $# -ne 1 ]
then
echo "请输入所删除key文件路径"
exit;
fi


cat $FILE_NAME | while read line
do
${CLIENT} keys $line
${CLIENT} keys $line | xargs ${CLIENT} del
done
