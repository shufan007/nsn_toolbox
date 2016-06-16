@echo off
set network_port=2
rem set capture time (unit: second) 
set /a capture_time=120
set out_file_name=raw_data.pcap
cd
set CurrentPath=%cd%
pushd %CurrentPath%
tshark -D
echo -----------------------------
echo network_port: %network_port%
echo capture_time: %capture_time% seconds

rem start capture packets
tshark -i 2 -a duration:%capture_time% -F pcap -w %out_file_name%