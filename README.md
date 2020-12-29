# 风语
将信息发送到每处, 接受每一处的结果, 返回最喜欢的那一处. 并支持获取其余处结果的可能性.

## 运行方式
### 依赖
python3.6+
其余依赖参见 `requirements.txt`, 可使用`pip3 install -r requirements.txt`进行一键式安装
### 虚拟环境
可自建, 或者使用`source env_use.profile`, 将在用户目录下新建`/env`目录,创建虚拟环境
### 运行命令
`python3 windwhisper.py` 默认端口`5481`, 此方式可方便断点调试
或
`uvicorn windwhisper:app --reload --port 5481` 此方式可用于测试环境

其余可详细参考`uvicorn --help`使用符合实际情况的运行参数。


## APPS
现有以下几个APP：
### 用户

### RSS

### 城市
