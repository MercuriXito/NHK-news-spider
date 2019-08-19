#!/usr/bin/bash

# check error of crontab in /var/spool/mail/root

# env variables
localtime=`date +%Y-%m-%d`
slocaltime=`date +%Y-%m-%d_%H:%M:%S`
# fill the base path of the project
basepath='/root/Projects/NHK-news-spider' # for example
logfile=${localtime}'_crawl.log'
errorfile=${localtime}'_error.log'

cd $basepath
# create log
has_log=`ls ${basepath} | grep -w log`
if [ x$has_log == x ];then
    mkdir log
fi

# run
echo Crawling in ${slocaltime} >> ${basepath}/log/${logfile}
python3 start.py 1>> ${basepath}/log/${logfile} 2>> ${basepath}/log/${errorfile}
echo >> ${basepath}/log/${logfile}

errors=`cat ${basepath}/log/${errorfile}`
if [ x${errors} = x ];then
    rm -rf ${basepath}/log/${errorfile}
fi