启动方式：python run.py -f config.yaml

# config.yaml
```
config:
  HOST: # 应用监听的ip
    '0.0.0.0'
  PORT: # 应用的端口
    7779
  DEBUG: # 应用的debug模式
    true
  SECRET_KEY: # 加密key，无固定生成方式，可随意填写
    'abcdefg'
  MONGODB_URL: # 程序的mongo地址
    'mongodb://192.168.0.48:38213/MOOP_SERVICE'
  LOG_FORMAT: # 输出日志格式
    '%(asctime)s - %(filename)s:%(lineno)s - %(name)s:%(funcName)s - [%(levelname)s] %(message)s'
```
