FROM ubuntu:16.04

RUN apt update -y && \
    apt install python3 python3-pip nginx redis-server supervisor python3-mysqldb language-pack-zh-hans ssh -y && \
    pip3 install --upgrade pip && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:certbot/certbot -y && \
    apt update -y

COPY ./ /root/app/
COPY ./nginx.conf /etc/nginx/nginx.conf
# COPY ./myuwsgi.service /lib/systemd/system/system/myuwsgi.service
# COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Startup project
RUN pip3 install -r /root/app/requirements.txt && \
    chmod +x /root/app/start.sh

EXPOSE 15522 80 443
# CMD ["bin/sh", '/root/app/start.sh']
# sudo docker image build -t myblog:0.1 ./
# sudo docker run --name blog1 -p 22:22 -p 80:80 -p 443:443 -t -d myblog:0.1