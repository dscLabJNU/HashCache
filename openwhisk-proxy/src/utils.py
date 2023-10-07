import os
import const


def check_file_exsited_storage(file_name: str):
    print(file_name)
    if str(file_name) in os.listdir(const.STORAGE_PATH):
        print("file existed")
        return True
    return False


def save_files(saved_file_name: str, response_content: bytes):
    # 将二进制流保存到本地文件
    saved_file_path = os.path.join(const.STORAGE_PATH, saved_file_name)
    with open(saved_file_path, 'wb') as f:
        f.write(response_content)
    print(f"file has saved in {saved_file_path}")

