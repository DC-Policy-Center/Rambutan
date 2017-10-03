#!/bin/bash




DATE=`date +%Y-%m-%d`
echo $(hostname -I)
echo $DATE
echo  $DATE: $(hostname -I) >> ip_log.txt
