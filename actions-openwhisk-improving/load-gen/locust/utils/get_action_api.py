import subprocess
import json
import sys
sys.path.append('../')
import constant

with open("api_config.json", "r") as f:
    target_actions = json.load(f).keys()

# 获取wsk api list -i命令行的输出，并提取出action名字和对应的api链接
output = subprocess.check_output(['wsk', 'api', 'list', '-i']).decode('utf-8')
lines = output.strip().split('\n')[1:]
actions = []
apis = []
for line in lines:
    action_name = line.split()[0]
    api = line.split()[3].replace(constant.WHISK_APIHOST_HTTPS, "")
    # 只需要api_config.json里面的action
    if action_name in target_actions:
        print(f"Gerneating api of {action_name}")
        actions.append(action_name)
        apis.append(api)

# 将action名字和对应的api链接映射成json格式，并保存在本地中，叫做mapping.json
mapping = dict(zip(actions, apis))
with open('action_api.json', 'w') as f:
    json.dump(mapping, f)
