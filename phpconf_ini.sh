#!/bin/bash
cpu_total=$(cat /proc/cpuinfo |grep "processor"|wc -l)
mem_total=$(cat /proc/meminfo |awk '{if($1=="MemTotal:"){print $2}}')
