docker build -t autologin-with-python .
docker run -d -p 5000:5000 -it autologin-with-python