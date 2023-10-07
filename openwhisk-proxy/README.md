# openwhisk-proxy

### required
- [mitmdump](https://mitmproxy.org/)

### FTP setup
```bash
$ bash ftp-setup.sh
```
This command will launch a lightweight FTP service, the root directory of the service is `/`.

### Run proxy
Please make sure you already set the docker proxy as https_proxy="http://127.0.0.1:8080" and http_proxy="http://127.0.0.1:8080"
```bash
$ bash proxy-setup.sh
```

### Run in one single script
The `run.sh` script monitoring the Control+C trap, kill the proxy server and the FTP server when tap Control+C
```bash
$ bash run.sh
```