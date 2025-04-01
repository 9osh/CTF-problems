#!/bin/bash
echo $CHECK_NUMBERS
service ssh restart;
# set *.h can't modify
find . -type f -name '*.h' -exec chmod 640 {} \;
if [ $CHECK_NUMBERS ];then
   echo $CHECK_NUMBERS > /root/total_times;
   sed -i "s/CHECK_NUMBERS/$CHECK_NUMBERS/g" /home/sectest/challenge/readme.txt
else
   sed -i "s/CHECK_NUMBERS/20/g" /home/sectest/challenge/readme.txt
fi
sleep infinity;
