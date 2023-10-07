import json
import subprocess as sp
SCRIPT_PATH=".."
with open("parameters.json","r") as load_f:
    load_dict = json.load(load_f)
INIT_SCRIPT_PATH=f"{SCRIPT_PATH}/init.sh"
RUN_SCRIPT_PATH=f"{SCRIPT_PATH}/run.sh"

# ./invoke.py init -main Handler $JAR_PATH
init_output=sp.check_output(f"python3 ../invoke.py init -main Handler {load_dict['JAR_PATH']}", shell=True)
print(f"init output:\n{init_output.decode('utf-8')}")

# ./invoke.py run $INPUT_STRING
run_output=sp.check_output(f"python3 ../invoke.py run '{json.dumps(load_dict['INPUT_STRING'])}'", shell=True)
print(f"invoke output:\n{run_output.decode('utf-8')}")
