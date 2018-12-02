redis-server /etc/redis/redis.conf
nginx
uwsgi --ini /root/app/uwsgi.ini --logto /root/app/uwsgi.log &
# ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
# sed -n '/PermitRootLogin/p' /etc/ssh/sshd_config #PermitRootLogin yes
/usr/sbin/sshd -D &

