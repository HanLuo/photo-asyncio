# 美女写真图爬虫 asyncio 版

*其他版本*

* [photo-go 版](https://github.com/chenjiandongx/photo-go)
* [photo-gevent 版](https://github.com/chenjiandongx/photo-gevent)

### aiohttp/aiofiles
之前写多线程/多进程爬虫基本上都是使用 requests，而 Python3 最大的魅力可能就是异步编程了。本爬虫以 asyncio 为基础，使用了 aiohttp/aiofiles 两个第三方异步库。


### 如何运行

#### 图片数据
图片地址数据保存在了 `data.txt`，共 17w+ 张照片，图片的数据是我从 [mmjpg](https://github.com/chenjiandongx/mmjpg) 和 [mzitu](https://github.com/chenjiandongx/mzitu) 里提取出来的。
```bash
$ wc -l data.txt
178075 data.txt
```

#### 运行代码
```bash
$ git clone https://github.com/chenjiandongx/photo-asyncio.git
$ cd photo-asyncio
$ pip install -r requirements.txt # 安装依赖
$ python core.py
```

#### 运行效果

![效果图](https://user-images.githubusercontent.com/19553554/41389455-8b99dc2c-6fc3-11e8-8e88-a0b188326317.gif)


## License

MIT [©chenjiandongx](https://github.com/chenjiandongx)
