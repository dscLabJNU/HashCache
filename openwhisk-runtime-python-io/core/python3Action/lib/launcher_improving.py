#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function
from sys import stdin
from sys import stdout
from sys import stderr
from os import fdopen
import aspectlib
import sys, os, json, traceback, warnings
import os
import shutil

def copy_tcp_file(source_path: str, dest_path: str):
    print(f"copyCmd: cp {source_path} {dest_path}")
    try:
        shutil.copy(source_path, dest_path)
    except Exception as e:
        print(f"Failed to copy file: {e}")


def analyze_socket_ports(file_path: str) -> bool:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Socket connections shown after the first line.
    lines = lines[1:]
    port_set = set()
    for line in lines:
        # Extract the port information from the line and convert from hex to decimal.
        port_set.add(int(line[29:33], 16))
    
    print("ports: ", port_set)
    
    # Every container opens 0000 port for local socket communication
    port_set.discard(0)
    # This 8080 port is for communication with OpenWhisk
    port_set.discard(8080)
    # I/O proxy port
    port_set.discard(8673)
    
    print("Unique port list: ", port_set)
    
    # Openwhisk invoker creates another connection with this proxy for sending invocation
    return len(port_set) != 1

def compare_two_files(old_file: str, new_file: str) -> list:
    with open(old_file, 'r') as file:
        lines_old = file.readlines()
    
    with open(new_file, 'r') as file:
        lines_new = file.readlines()
        
    ports = []
    print(f"Comparing {old_file} and {new_file}")
    
    # Find lines that are in the new file but not in the old file
    final_list = [line for line in lines_new if line not in lines_old]
    
    if len(final_list) == 0:
        print("They are the same")
    else:
        print("Recording the ports: ")
        for line in final_list:
            # Extract the port information from the line and convert from hex to decimal.
            ports.append(int(line[29:33], 16))
        
        print("Here is the difference: ")
        for line in final_list:
            print(line)
    
    return ports

try:
  # if the directory 'virtualenv' is extracted out of a zip file
  path_to_virtualenv = os.path.abspath('./virtualenv')
  if os.path.isdir(path_to_virtualenv):
    # activate the virtualenv using activate_this.py contained in the virtualenv
    activate_this_file = path_to_virtualenv + '/bin/activate_this.py'
    if not os.path.exists(activate_this_file): # try windows path
      activate_this_file = path_to_virtualenv + '/Scripts/activate_this.py'
    if os.path.exists(activate_this_file):
      with open(activate_this_file) as f:
        code = compile(f.read(), activate_this_file, 'exec')
        exec(code, dict(__file__=activate_this_file))
    else:
      sys.stderr.write("Invalid virtualenv. Zip file does not include 'activate_this.py'.\n")
      sys.exit(1)
except Exception:
  traceback.print_exc(file=sys.stderr, limit=0)
  sys.exit(1)

# now import the action as process input/output
from main__ import main as main

out = fdopen(3, "wb")
if os.getenv("__OW_WAIT_FOR_ACK", "") != "":
    out.write(json.dumps({"ok": True}, ensure_ascii=False).encode('utf-8'))
    out.write(b'\n')
    out.flush()

env = os.environ
while True:
  tcp_file = '/proc/net/tcp'
  tcp_snapshot = './tcp.snp'
  # back up the original tcp file
  copy_tcp_file(source_path=tcp_file, dest_path=tcp_snapshot)
  line = stdin.readline()
  if not line: break
  args = json.loads(line)
  payload = {}
  for key in args:
    if key == "value":
      payload = args["value"]
    else:
      env["__OW_%s" % key.upper()]= args[key]
  res = {}
  try:
    is_open = False

    @aspectlib.Aspect
    def open_hook(*args, **kwargs):
      global is_open
      is_open = True
      print("hook")
      result = yield aspectlib.Proceed
      yield aspectlib.Return(result)

    with aspectlib.weave(open, open_hook):
      os.environ['http_proxy'] = 'hashcache-global-proxy.default:8674'
      os.environ['https_proxy'] = 'hashcache-global-proxy.default:8674'
      print(f"HTTP_PROXY: {os.environ['http_proxy']}")
      res = main(payload)
    res = {"data":res,"is_open":is_open}
    # Compare the backup tcp file with the newest one
    addtional_ports = compare_two_files(old_file=tcp_snapshot, new_file=tcp_file)
    if addtional_ports:
      res['is_open'] = True
  except Exception as ex:
    print(traceback.format_exc(), file=stderr)
    res = {"error": str(ex)}
  out.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
  out.write(b'\n')
  stdout.flush()
  stderr.flush()
  out.flush()
