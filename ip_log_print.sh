#!/bin/bash




DATE=`date +%Y-%m-%d`
echo $(hostname -I)
echo $DATE
echo  $DATE: $(hostname -I) >> ~/Documents/github/Rambutan/ip_log.txt
