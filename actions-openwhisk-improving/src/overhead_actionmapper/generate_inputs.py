import json
import multiprocessing
import os
import random
import string
import argparse

# 定义生成随机字符串的函数


def generate_random_string(length):
    # 生成包含数字和字母的字符集
    chars = string.ascii_letters + string.digits

    # 随机选择字符生成字符串
    return "".join(random.choice(chars) for _ in range(length))


# 定义生成输入输出对的函数
def generate_input_output_pair(pair_size):
    # 生成随机输入和输出
    input_data = generate_random_string(pair_size)
    output_data = generate_random_string(pair_size)

    # 将输入和输出保存到字典中
    pair = {"input": input_data, "output": output_data}
    return pair


# 定义生成输入输出对的进程函数
def generate_pairs_in_process(queue, pair_size, pairs_per_process):
    pairs = []
    for _ in range(pairs_per_process):
        pair = generate_input_output_pair(pair_size)
        pairs.append(pair)
    queue.put(pairs)


def parallel_generation(num_pairs, pair_size, data_file):
    # 计算每个进程需要生成的输入输出对数量
    num_processes = multiprocessing.cpu_count()
    pairs_per_process = num_pairs // num_processes

    # 创建进程池并生成输入输出对
    pool = multiprocessing.Pool(num_processes)
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    processes = []

    for i in range(num_processes):
        if i == num_processes - 1:
            pairs_per_process = num_pairs - i * pairs_per_process
        # 在进程池中启动生成输入输出对的进程
        process = pool.apply_async(
            generate_pairs_in_process, (queue, pair_size, pairs_per_process))
        processes.append(process)

    # 等待所有进程完成
    pool.close()
    pool.join()

    # 从队列中获取所有进程生成的输入输出对
    pairs = []
    while not queue.empty():
        pairs.extend(queue.get())

    # 将所有输入输出对保存到JSON文件中
    with open(data_file, "w") as f:
        json.dump(pairs, f)


def generate_inputs(data_file, pair_size, num_pairs):
    # 检查文件是否已经存在
    if os.path.exists(data_file):
        print(f"Data file: [{data_file}] is existed")
        
        # check length of the existed file
        with open(data_file, "r") as f:
            print(f"Checking the length of file: {data_file}")
            num_pairs_existed = len(json.load(f))
        if num_pairs_existed != num_pairs:
            print(f"Length didn't fit the requirement ({num_pairs})")
            print(f"Now regenerating...")
            parallel_generation(num_pairs, pair_size, data_file)
        else:
            print(f"The length requirement is mathed!")
    else:
        parallel_generation(num_pairs, pair_size, data_file)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_input_pairs", type=int,
                        required=True, help="number of input-output pairs")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    data_file = "input_output_pairs.json"
    # 定义要生成的输入输出对数量和大小
    num_pairs = args.num_input_pairs
    pair_size = 50 * 1024  # 50 KB

    generate_inputs(data_file=data_file,
                    num_pairs=num_pairs, pair_size=pair_size)
