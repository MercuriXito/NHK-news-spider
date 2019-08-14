#!/usr/bin/bash

# env variables
localtime=`date +%Y-%m-%d`
slocaltime=`date +%Y-%m-%d_%H:%M:%S`
basepath='/root/Projects/nhkspider'
logfile=${localtime}'_crawl.log'
errorfile=${localtime}'_error.log'

cd $basepath
echo Crawling in ${slocaltime} >> ${basepath}/logs/${logfile}
python3 start.py 1>> ${basepath}/logs/${logfile} 2>> ${basepath}/logs/${errorfile}
echo >> ${basepath}/logs/${logfile}

errors=`cat ${basepath}/logs/${errorfile}`
if [ x${errors} = x ];then
    rm -rf ${basepath}/logs/${errorfile}
fi