find all  修改ip，port
虚拟机修改fdfs：cd /etc/fdfs 
sudo vi client.conf
sudo vi  mod_fastdfs.conf
sudo vi storage.conf

启动tracker，storage，nginx
sudo service fdfs_trackerd start
sudo service fdfs_storaged start
sudo /usr/local/nginx/sbin/nginx

虚拟机：celery -A  celery_tasks.tasks worker -l info
python manage.py rebuild_index 重新生成搜索索引文件
