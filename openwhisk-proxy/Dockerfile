From python:3.9-buster

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir -p /proxy/src
COPY src/ /proxy/src

COPY run.sh /proxy/run.sh
RUN chmod +x /proxy/run.sh
WORKDIR /proxy

# socks5 Port
EXPOSE 8673
# HTTP/HTTPs Port
EXPOSE 8674

CMD ["bash", "/proxy/run.sh"]