#!/bin/bash

# python3 docker_stats.py

echo "(test_$1.json)"
for (( i=1; i<=10; i++ ))
do  
   echo "Test $i:"
   curl -X POST -H "Content-Type: application/json" -d @test_$1.json http://192.168.1.53:8080/rule/create
done