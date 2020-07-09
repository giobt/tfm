#!/bin/bash
./filebeat modules enable suricata
./filebeat setup
./filebeat -e