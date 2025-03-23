import subprocess
import os
import argparse
import time

def run_scrapy(spider_name):
    try:
        scrapy_dir = os.path.join(os.getcwd(), "myproject")
        subprocess.run(
            ["scrapy", "crawl", spider_name],
            cwd=scrapy_dir,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Scrapy 执行失败: {e}")
        return False

def wait_for_file(data_file, timeout=10):
    start = time.time()
    print(f"等待文件 {data_file} 出现...")
    while True:
        if os.path.exists(os.path.join("data", data_file)):
            return True
        elif time.time() - start > timeout:
            return False
        time.sleep(1)

def run_streamlit(data_file):
    try:
        streamlit_dir = os.path.join(os.getcwd(), "streamlit_app")
        subprocess.run(
            ["streamlit", "run", "app.py", "--", "--data-file", data_file],
            cwd=streamlit_dir
        )
        return True
    except Exception as e:
        print(f"启动 Streamlit 失败: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--spider", required=True, help="要运行的爬虫名称")
    parser.add_argument("--spider", default="danbooru", help="要运行的爬虫名称")
    args = parser.parse_args()

    data_file = f"{args.spider}.json"  # 生成对应的数据文件名

    if run_scrapy(args.spider):
        if wait_for_file(data_file):
            run_streamlit(data_file)
        else:
            print(f"超时：未找到文件 {data_file}")