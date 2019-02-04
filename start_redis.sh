#!/bin/bash
if [ ! -d redis-stable/src ]; then
    curl -O http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    rm redis-stable.tar.gz
    cd redis-stable
    make
else
    cd redis-stable
fi

#vm.overcommit_memory = 1
#echo never > /sys/kernel/mm/transparent_hugepage/enabled

src/redis-server

exit 0
