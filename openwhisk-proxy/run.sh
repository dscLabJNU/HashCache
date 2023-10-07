# !/bin/bash
proxy_cmd="mitmdump -s ./src/mitmproxy_script.py --mode socks5@8673 --mode regular@8674"
ftp_cmd="http.server 2016"

trap 'onCtrlC' INT
function execRemoteCMD() {
    ps_command=$1
    exec_command=$2

    filter_result=$ps_command
    if [ -n "$filter_result" ]; then
        echo "Executing: $exec_command"
        $exec_command
    else
        echo "Nothing to do..."
    fi
}

function kill_proxy() {
    echo '===============Killing Proxy process==============='
    ps_command=$(ps -ef | grep -v grep | grep "$proxy_cmd" | awk "{print \$2}")
    echo "Proxy Process: $ps_command"
    exec_command="kill $ps_command"
    execRemoteCMD "${ps_command}" "${exec_command}"
    echo '===============Killed Proxy process==============='
}

function kill_ftp() {
    echo '===============Killing FTP server process==============='
    ps_command=$(ps -ef | grep -v grep | grep "$ftp_cmd" | awk "{print \$2}")
    echo "FTP process: $ps_command "
    exec_command="kill $ps_command"
    execRemoteCMD "${ps_command}" "${exec_command}"
    echo '===============Killed FTP server process==============='
}

function onCtrlC () {
    echo 'capture Ctrl + C'
    kill_ftp &
    kill_proxy &
    wait
    exit
}


$proxy_cmd &

cd /

python3 -m $ftp_cmd &


while true; do
    sleep 1
done
