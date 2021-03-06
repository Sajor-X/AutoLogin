# AutoLogin

## 原理介绍
[自动登录工具开发](http://blog.sajor.top/16110385786886.html)


## 依赖安装
```shell
pip install -r requirements.txt
```

## 接口
http://localhost:5000/login

## Windows
针对windows，可以使用此打包命令打包

```shell script
pyinstaller -F ./app.py -p ./ -n AutoLogin
```

因为需要`tesserocr`支持，所以要使用`dist`中的`tessdata`包依赖

`AutoLogin/dist/AutoLogin.exe` 为已打好的包可直接在Windows中使用
