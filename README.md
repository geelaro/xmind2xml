# xmind2xml
转换xmind格式的用例为`Testlink`需要的xml格式.

## 搭建环境

有以下两种方法安装依赖包

1. 使用`pipenv install`安装依赖
2. `pip install -r requirements.txt`

## 使用

### 1. `main.py`

- 把xmind格式用例复制到`doc`目录，执行`python main.py`，程序运行成功，转换完成。
- xml格式的同名文档保存在`doc`目录

### 2. `main.exe`

####  打包为 exe程序

使用`pyinstaller`打包
```shell
pyinstaller -F main.py -p datatype.py,logger_handler.py,testlink_parse.py,xmind_parse.py
```

### 运行

- 于`main.exe`所在目录新建子目录doc，把需要转换的xmind格式复制到此目录，运行`main.exe`，转换后的xml文件存在在doc目录。