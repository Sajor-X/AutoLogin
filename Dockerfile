FROM python:3.6.15

WORKDIR /home/app

#If we add the requirements and install dependencies first, docker can use cache if requirements don't change
ADD requirements.txt /home/app
RUN python -m pip install --upgrade pip  -i https://pypi.tuna.tsinghua.edu.cn/simple \
        && pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.douban.com/simple/ \
        && rm -rf /tmp/* && rm -rf /root/.cache/* \
        && touch uwsgi.pid \
        && sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com/#g' /etc/apt/sources.list\
        && apt-get --allow-releaseinfo-change update && apt install libgl1-mesa-glx -y

ADD . /home/app
CMD uwsgi --ini uwsgi.ini

EXPOSE 5000
