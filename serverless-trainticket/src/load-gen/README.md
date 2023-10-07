# 1. 创建并应用虚拟环境
```shell
conda create -n load-gen python=3.8
pip3 install -r requirements.txt
conda activate load-gen
```

# 2. 生成action对应的API
生成 action_api.json，记录了 api_config.json 中所有 action 对应的 API
```shell
cd utils
python get_action_api.py
```

# 3. 设置locust config file
```shell
locust --config=locust.conf
```

# 3. 选择策略，运行负载
```shell
bash run_load.sh [HashCache, FaaSCache, OpenWhisk]
```