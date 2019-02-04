#!/bin/bash
if [ ! -d redis-stable/src ]; then
    echo "Redis not installed at ./redis-stable/src"
else
    cd redis-stable
fi

src/redis-cli shutdown

exit 0
