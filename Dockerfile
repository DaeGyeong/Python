FROM centos:latest
MAINTAINER dg kwon <dg.kwon@navercorp.com>

RUN yum groupinstall -y 'Development Tools' &&\
    yum install -y wget net-tools gcc* libtool* expat-devel

# 아파치
RUN mkdir -p /apps/web
WORKDIR /apps/web

RUN wget http://mirror.navercorp.com/apache/httpd/httpd-2.4.29.tar.gz
RUN wget http://mirror.navercorp.com/apache/apr/apr-1.6.3.tar.gz
RUN wget http://mirror.navercorp.com/apache/apr/apr-util-1.6.1.tar.gz
RUN wget http://downloads.sourceforge.net/project/pcre/pcre/8.41/pcre-8.41.tar.gz

RUN tar xzf httpd-2.4.29.tar.gz
RUN tar xzf apr-1.6.3.tar.gz
RUN tar xzf apr-util-1.6.1.tar.gz
RUN tar xzf pcre-8.41.tar.gz

WORKDIR /apps/web/pcre-8.41
RUN ./configure
RUN make && make install

WORKDIR /apps/web
RUN mv apr-1.6.3 httpd-2.4.29/srclib/apr
RUN mv apr-util-1.6.1 httpd-2.4.29/srclib/apr-util

WORKDIR /apps/web/httpd-2.4.29
RUN ./configure --prefix=/apps/apache2
RUN make; make install

RUN echo "alias apachectl='/apps/apache2/bin/apachectl'" >> ~/.bashrc
RUN source ~/.bashrc
EXPOSE 80

# MySQL
RUN mkdir /apps/data
WORKDIR /apps/data
RUN wget http://downloads.sourceforge.net/project/boost/boost/1.59.0/boost_1_59_0.tar.gz
RUN wget mirror.koreaidc.com/mysql/mysql-5.7.9.tar.gz
RUN tar xzf boost_1_59_0.tar.gz
RUN tar xzf mysql-5.7.9.tar.gz

WORKDIR /apps/data/mysql-5.7.9
RUN yum -y install ncurses ncurses-devel cmake
RUN cmake \
  -DCMAKE_INSTALL_PREFIX=/apps/mysql \
  -DWITH_EXTRA_CHARSETS=all \
  -DMYSQL_DATADIR=/apps/mysql_data \
  -DENABLED_LOCAL_INFILE=1 \
  -DDOWNLOAD_BOOST=1 \
  -DWITH_BOOST=../boost_1_59_0 \
  -DWITH_INNOBASE_STORAGE_ENGINE=1 \
  -DENABLED_LOCAL_INFILE=1 \
  -DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
  -DSYSCONFDIR=/etc \
  -DDEFAULT_CHARSET=utf8 \
  -DDEFAULT_COLLATION=utf8_general_ci \
  -DWITH_EXTRA_CHARSETS=all

RUN make; make install

RUN echo "Servername "`hostname -I`:80 >> /apps/apache2/conf/httpd.conf
RUN apachectl start


WORKDIR /apps/data
RUN wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
RUN tar xzf Python-3.6.4.tgz
RUN wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.4.13.tar.gz
RUN tar xzf 4.4.13.tar.gz

RUN yum install -y git zlib*
RUN yum install -y bzip2-devel db4-devel gdbm-devel libpcap-devel ncurses-devel openssl-devel readline-devel sqlite-devel xz-devel zlib-devel

WORKDIR /apps/data/Python-3.6.4
RUN ./configure --prefix=/apps/Python3 CFLAGS=-fPIC --enable-shared --with-threads
#RUN ./configure --prefix=/apps/Python3 CFLAGS=-fPIC --enable-shared
RUN echo "export LD_RUN_PATH=/usr/lib">>~/.bashrc
RUN source ~/.bashrc
RUN make
RUN make install
RUN ln -s /apps/Python3/lib/libpython3.6m.so.1.0 /usr/lib
RUN rm -rf /apps/Python3
RUN make clean
RUN ./configure --prefix=/apps/Python3 CFLAGS=-fPIC --enable-shared --with-threads
RUN make
RUN make install
RUN ln -s /apps/Python3/lib/libpython3.6m.so.1.0 /lib64/

WORKDIR /apps/data/mod_wsgi-4.4.13
RUN ln -s /apps/apache2/bin/apxs /usr/bin/
RUN ./configure CFLAGS=-fPIC --with-python=/apps/Python3/bin/python3 --prefix=/apps/apache2/modules
RUN make
RUN make install

RUN echo "#python3">>~/.bashrc
RUN echo "alias python='/apps/Python3/bin/python3'">>~/.bashrc
RUN echo "alias pip='/apps/Python3/bin/pip3'">>~/.bashrc
RUN echo "alias django='/apps/Python3/bin/django-admin.py'">>~/.bashrc
RUN source ~/.bashrc

RUN /apps/Python3/bin/pip3 install django==1.8
RUN /apps/Python3/bin/pip3 install django-bootstrap3
RUN /apps/Python3/bin/pip3 install pymysql

RUN mkdir /apps/web_root
WORKDIR /apps/web_root

RUN git clone https://github.com/DaeGyeong/Django.git
WORKDIR /apps/web_root/Django

# httpd.conf 파일 수정 합시다
RUN ip=`hostname -I`
RUN sed -i "s/#ServerName www.example.com/ServerName `hostname -I|cut -f 1 -d ' '`/g" /apps/apache2/conf/httpd.conf


RUN echo "LoadModule wsgi_module modules/mod_wsgi.so" >> /apps/apache2/conf/httpd.conf

RUN echo "WSGIScriptAlias / /apps/web_root/Django/learning_log/wsgi.py" >> /apps/apache2/conf/httpd.conf
RUN echo "WSGIPythonPath /apps/web_root/Django" >> /apps/apache2/conf/httpd.conf
RUN echo "WSGIDaemonProcess testdjango lang='ko_KR.UTF-8' locale='ko_KR.UTF-8'" >> /apps/apache2/conf/httpd.conf
RUN echo "<Directory /apps/web_root/Django/learning_log>" >> /apps/apache2/conf/httpd.conf
RUN echo "<Files wsgi.py>" >> /apps/apache2/conf/httpd.conf
RUN echo "Order deny,allow" >> /apps/apache2/conf/httpd.conf
RUN echo "Require all granted" >> /apps/apache2/conf/httpd.conf
RUN echo "</Files>" >> /apps/apache2/conf/httpd.conf
RUN echo "</Directory>" >> /apps/apache2/conf/httpd.conf

#DB 생성해봅시다
RUN useradd -M mysql -u 27 >& /dev/null
RUN chown -R root:mysql /apps/mysql
WORKDIR /apps/mysql

RUN \
echo "[client]" > /etc/my.cnf && \
echo "default-character-set = utf8" >> /etc/my.cnf && \
echo "port = 3306" >> /etc/my.cnf && \
echo "socket = /tmp/mysql.sock" >> /etc/my.cnf && \
echo "default-character-set = utf8" >> /etc/my.cnf && \
echo "[mysqld]" >> /etc/my.cnf && \
echo "socket=/tmp/mysql.sock" >> /etc/my.cnf && \
echo "datadir=/apps/mysql_data" >> /etc/my.cnf && \
echo "basedir = /apps/mysql" >> /etc/my.cnf && \
echo "port = 3306" >> /etc/my.cnf && \
echo "skip-external-locking" >> /etc/my.cnf && \
echo "skip-grant-tables" >> /etc/my.cnf && \
echo "key_buffer_size = 384M" >> /etc/my.cnf && \
echo "max_allowed_packet = 1M" >> /etc/my.cnf && \
echo "table_open_cache = 512" >> /etc/my.cnf && \
echo "sort_buffer_size = 2M" >> /etc/my.cnf && \
echo "read_buffer_size = 2M" >> /etc/my.cnf && \
echo "read_rnd_buffer_size = 8M" >> /etc/my.cnf && \
echo "myisam_sort_buffer_size = 64M" >> /etc/my.cnf && \
echo "thread_cache_size = 8" >> /etc/my.cnf && \
echo "query_cache_size = 32M" >> /etc/my.cnf && \
echo "skip-name-resolve" >> /etc/my.cnf && \
echo "max_connections = 1000" >> /etc/my.cnf && \
echo "max_connect_errors = 1000" >> /etc/my.cnf && \
echo "wait_timeout= 60" >> /etc/my.cnf && \
echo "explicit_defaults_for_timestamp" >> /etc/my.cnf && \
echo "symbolic-links=0" >> /etc/my.cnf && \
echo "log-error=/apps/mysql_data/mysqld.log" >> /etc/my.cnf && \
echo "pid-file=/tmp/mysqld.pid" >> /etc/my.cnf && \
echo "character-set-client-handshake=FALSE" >> /etc/my.cnf && \
echo "init_connect = SET collation_connection = utf8_general_ci" >> /etc/my.cnf && \
echo "init_connect = SET NAMES utf8" >> /etc/my.cnf && \
echo "character-set-server = utf8" >> /etc/my.cnf && \
echo "collation-server = utf8_general_ci" >> /etc/my.cnf && \
echo "symbolic-links=0" >> /etc/my.cnf && \
 \
echo "key_buffer_size = 32M" >> /etc/my.cnf && \
echo "bulk_insert_buffer_size = 64M" >> /etc/my.cnf && \
echo "myisam_sort_buffer_size = 128M" >> /etc/my.cnf && \
echo "myisam_max_sort_file_size = 10G" >> /etc/my.cnf && \
echo "myisam_repair_threads = 1" >> /etc/my.cnf && \
 \
echo "default-storage-engine = InnoDB" >> /etc/my.cnf && \
echo "innodb_buffer_pool_size = 1024MB" >> /etc/my.cnf && \
echo "innodb_data_file_path = ibdata1:10M:autoextend" >> /etc/my.cnf && \
echo "innodb_write_io_threads = 8" >> /etc/my.cnf && \
echo "innodb_read_io_threads = 8" >> /etc/my.cnf && \
echo "innodb_thread_concurrency = 16" >> /etc/my.cnf && \
echo "innodb_flush_log_at_trx_commit = 1" >> /etc/my.cnf && \
echo "innodb_log_buffer_size = 8M" >> /etc/my.cnf && \
echo "innodb_log_file_size = 128M" >> /etc/my.cnf && \
echo "innodb_log_files_in_group = 3" >> /etc/my.cnf && \
echo "innodb_max_dirty_pages_pct = 90" >> /etc/my.cnf && \
echo "innodb_lock_wait_timeout = 120" >> /etc/my.cnf && \
 \
echo "[mysqldump]" >> /etc/my.cnf && \
echo "default-character-set = utf8" >> /etc/my.cnf && \
echo "max_allowed_packet = 16M" >> /etc/my.cnf && \
 \
echo "[mysql]" >> /etc/my.cnf && \
echo "no-auto-rehash" >> /etc/my.cnf && \
echo "default-character-set = utf8" >> /etc/my.cnf && \
 \
echo "[myisamchk]" >> /etc/my.cnf && \
echo "key_buffer_size = 256M" >> /etc/my.cnf && \
echo "sort_buffer_size = 256M" >> /etc/my.cnf && \
echo "read_buffer = 2M" >> /etc/my.cnf && \
echo "write_buffer = 2M" >> /etc/my.cnf

RUN ./bin/mysqld --initialize --user=mysql --basedir=/apps/mysql --datadir=/apps/mysql_data
#RUN ./support-files/mysql.server start
RUN /apps/mysql/support-files/mysql.server start &&\
./bin/mysql -e "create database django;" &&\
./bin/mysql -e "use mysql; update user set authentication_string=password('root') where user='root';"&&\
/apps/mysql/bin/mysql -e "insert into mysql.user(host,user,authentication_string,ssl_cipher,x509_issuer,x509_subject) values('%','root',password('root'),'','','');" &&\
#/apps/mysql/bin/mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'" &&\
/apps/mysql/bin/mysql -e "flush privileges;"


RUN sed -i 's/skip-grant-tables/#skip-grant-tables/g' /etc/my.cnf
RUN ./support-files/mysql.server restart
#RUN ./support-files/mysql.server restart &&\
#./bin/mysql -u root -pMyNewPass -e "use mysql; set password=password('root');"


WORKDIR /apps/web_root/Django
RUN sed -i "s/localhost/`hostname -I|cut -f 1 -d ' ' `/g" /apps/web_root/Django/learning_log/settings.py
RUN sed -i "s/13306/3306/g" /apps/web_root/Django/learning_log/settings.py

RUN echo "/apps/mysql/support-files/mysql.server restart" >> /apps/init_config
RUN echo "/apps/mysql/bin/mysql -u root -proot -e 'set password=password('root');'" >> /apps/init_config
RUN echo "/apps/mysql/bin/mysql -u root -proot -e 'set password for 'root'@'%'=password('root');'" >> /apps/init_config
RUN echo "/apps/mysql/bin/mysql -u root -proot -e 'GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'; flush privileges;'" >> /apps/init_config
RUN echo "/apps/Python3/bin/python3 manage.py makemigrations" >> /apps/init_config
RUN echo "/apps/Python3/bin/python3 manage.py migrate" >> /apps/init_config

RUN chmod +x /apps/init_config
#RUN /apps/init_config

EXPOSE 80
#EXPOSE 3306


RUN echo "alias apachectl='/apps/apache2/bin/apachectl'" >> ~/.bashrc
RUN echo "alias mysql_service='/apps/mysql/support-files/mysql.server'" >> ~/.bashrc
RUN echo "alias mysql='/apps/mysql/bin/mysql'" >> ~/.bashrc
