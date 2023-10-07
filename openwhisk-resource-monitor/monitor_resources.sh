#!/bin/bash

ethn=$(cat paramaters.json | jq -r '.NIC') # 网卡名称
disk=$(cat paramaters.json | jq -r '.DISK') # 分区名称

time=0
echo "Time(s),Net_Receive(MB/s),CPU_Util(%),Disk_WR(0.1*MB/s),Mem_Util(0.01*MB),StateBridgeMem(MB),OWControllerMem(MB)"
while true
do
  # CPU
  CPULOG_1=$(cat /proc/stat | grep 'cpu ' | awk '{print $2" "$3" "$4" "$5" "$6" "$7" "$8}')
  SYS_IDLE_1=$(echo $CPULOG_1 | awk '{print $4}')
  Total_1=$(echo $CPULOG_1 | awk '{print $1+$2+$3+$4+$5+$6+$7}')
  
  # NET
  RX_pre=$(cat /proc/net/dev | grep -w $ethn | sed 's/:/ /g' | awk '{print $2}')
  TX_pre=$(cat /proc/net/dev | grep -w $ethn | sed 's/:/ /g' | awk '{print $10}')

  # DISK
  RD_pre=$(cat /proc/diskstats | grep -w $disk | awk '{print $6}')
  WR_pre=$(cat /proc/diskstats | grep -w $disk | awk '{print $10}')
  
  # Wait a moment
  sleep 1

  # CPU
  CPULOG_2=$(cat /proc/stat | grep 'cpu ' | awk '{print $2" "$3" "$4" "$5" "$6" "$7" "$8}')
  SYS_IDLE_2=$(echo $CPULOG_2 | awk '{print $4}')
  Total_2=$(echo $CPULOG_2 | awk '{print $1+$2+$3+$4+$5+$6+$7}')
  SYS_IDLE=`expr $SYS_IDLE_2 - $SYS_IDLE_1`
  Total=`expr $Total_2 - $Total_1`
  SYS_USAGE=`expr $SYS_IDLE/$Total*100 |bc -l`
  SYS_Rate=`expr 100-$SYS_USAGE |bc -l`
  Disp_SYS_Rate=`expr "scale=3; $SYS_Rate/1" |bc`

  # NET
  RX_next=$(cat /proc/net/dev | grep -w $ethn | sed 's/:/ /g' | awk '{print $2}')
  TX_next=$(cat /proc/net/dev | grep -w $ethn | sed 's/:/ /g' | awk '{print $10}')


  # DISK grep -w 表示全字匹配
  RD_next=$(cat /proc/diskstats | grep -w $disk | awk '{print $6}')
  WR_next=$(cat /proc/diskstats | grep -w $disk | awk '{print $10}')

  # RD_rate=$((${RD_next}-${RD_pre}))
  RD_rate=`expr ${RD_next} - ${RD_pre}`
  WR_rate=`expr ${WR_next} - ${WR_pre}`

  RD_rate=$(echo $RD_rate | awk '{print $1*(512/(1024*1024*10))}') # 10*MB/s
  WR_rate=$(echo $WR_rate | awk '{print $1*(512/(1024*1024*10))}') # 10*MB/s
  # echo -e "\t RX `date +%k:%M:%S` TX"

  RX=$((${RX_next}-${RX_pre}))
  TX=$((${TX_next}-${TX_pre}))
  # KB/S
  RX=$(echo $RX | awk '{print $1/(1024*1024)}') # MB/s
  TX=$(echo $TX | awk '{print $1/(1024*1024)}') # MB/s

  Mem_Usage=$(free -m | awk '/Mem/{printf("RAM Usage: %.2f\n"), $3/100}'| awk '{print $3}')
  StateBridgeMem=$(kubectl top pod -l app=hashcache-global-proxy --no-headers | awk '{size=$3; printf "%.2f\n", size}')
  OWControllerMem=$(kubectl top pod -n openwhisk --no-headers  | grep owdev-controller- | awk '{ sum += $3 } END { printf "%.2f\n", sum }')
  time=`expr $time + 1`
  echo -e "${time},$RX,$Disp_SYS_Rate,$WR_rate,$Mem_Usage,$StateBridgeMem,$OWControllerMem"


done

