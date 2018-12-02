1.安装mysql，并修改app/myblog/myblog/setting.py中的数据库设置

编码配置：https://chengfy.com/post/3

2.构建docker镜像及容器
```bash
# sudo docker image build -t myblog:0.1 ./
# sudo docker run --name blog1 -p 15522:22 -p 80:80 -p 443:443 -d myblog:0.1
```

3.进入容器，执行初始化脚本

```
# cd /root/app
# ./start.sh
```

4.https设置
```
# 这几条命令用来配置https，由于需要用户输入，所以单独执行
# apt-get install python-certbot-nginx -y
# certbot --nginx
# certbot renew --dry-run
```

5.ssh设置

修改/etc/ssh/sshd_config，允许root远程登录，记得设置root用户密码
```
PermitRootLogin yes
/etc/init.d/ssh restart
```
