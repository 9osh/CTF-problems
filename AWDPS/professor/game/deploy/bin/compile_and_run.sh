#!/bin/sh

set -e
# Switch between c or cpp
fsanitize=$1
debug=$2
suffix=$3
compile=$4
vuln_idx=$5
other=$6

rm -rf /tmp/test
mkdir -m 750 /tmp/test
chown test:test /tmp/test

cp /home/sectest/challenge/main.$suffix /tmp/test/.main.tmp.$suffix
chown test:test /tmp/test/.main.tmp.$suffix
chmod 640 /tmp/test/.main.tmp.$suffix
# copy needed header.h
if [ -e /home/sectest/challenge/header.h ]
then
    cp /home/sectest/challenge/header.h /tmp/test/header.h
    chown test:test /tmp/test/header.h
    chmod 640 /tmp/test/header.h
fi
# copy needed check.c
if [ -e /root/check$vuln_idx.$suffix ]
then
    cp /root/check$vuln_idx.$suffix /tmp/test/.check$vuln_idx.$suffix
    chown test:test /tmp/test/.check$vuln_idx.$suffix
    chmod 640 /tmp/test/.check$vuln_idx.$suffix
fi

APPEND_ARGS=""

if [ $fsanitize ] # ASAN
then
    APPEND_ARGS="$APPEND_ARGS -fsanitize=address"
fi

if [ -e /tmp/test/.check$vuln_idx.$suffix ]
then
    if [ $debug = "False" ]
    then
        chroot --userspec test:test / $compile -w -c /tmp/test/.check$vuln_idx.$suffix -o /tmp/test/.check$vuln_idx.o 1>/dev/null 2>/dev/null
    else # Debug mode
        chroot --userspec test:test / $compile -g -D DEBUG -Wall -Wextra -c /tmp/test/.check$vuln_idx.$suffix -o /tmp/test/.check$vuln_idx.o
    fi
fi

if [ -e /tmp/test/.check$vuln_idx.o ]
then
    APPEND_ARGS="$APPEND_ARGS /tmp/test/.check$vuln_idx.o"
fi

if [ $debug = "False" ]
then
    chroot --userspec test:test / $compile -w $APPEND_ARGS /tmp/test/.main.tmp.$suffix  -o /tmp/test/main $other 1>/dev/null 2>/dev/null
else
    chroot --userspec test:test / $compile -g -D DEBUG -Wall -Wextra $APPEND_ARGS /tmp/test/.main.tmp.$suffix  -o /tmp/test/main $other
fi

set +e
cp /root/run /tmp/test/run
chown test:test /tmp/test/run
chmod 550 /tmp/test/run

[ -e /tmp/test/main ] && chown test:test /tmp/test/main && chmod 440 /tmp/test/main

rm -f /tmp/test/.check$vuln_idx.$suffix /tmp/test/.check$vuln_idx.o /tmp/test/.main.tmp.$suffix
