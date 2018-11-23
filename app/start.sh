redis-server /etc/redis/redis.conf
nginx
uwsgi --ini /root/app/uwsgi.ini --logto /root/app/uwsgi.log &
# ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
