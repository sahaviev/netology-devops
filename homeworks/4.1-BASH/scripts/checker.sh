#!/usr/bin/env bash

services=(173.194.222.113 192.168.0.1 87.250.250.242)

: > checks.log
: > checks.error

for service in ${services[@]};
do
    for attempt in {1..5}
    do
        echo "attempt ${attempt} for service ${service}:80";
        curl -sI "${service}:80" -m 1 > /dev/null;
        if (($? != 0))
        then
          echo "attempt ${attempt}:  ${service}:80 unavailable" >> checks.error;
          exit 2
        else
          echo "attempt ${attempt}:  ${service}:80 available" >> checks.log;
        fi
    done
    sleep 1
done
