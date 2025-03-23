import subprocess
import os
import argparse
import signal
import sys
import time

def run_scrapy(spider_name):
    try:
        # 获取项目根目录（main.py 所在目录）
        project_root = os.path.dirname(os.path.abspath(__file__))
        scrapy_dir = os.path.join(project_root, "myproject")

        # 验证路径
        if not os.path.exists(scrapy_dir):
            raise NotADirectoryError(f"Scrapy 目录不存在: {scrapy_dir}")
        if not os.path.isdir(scrapy_dir):
            raise NotADirectoryError(f"路径不是目录: {scrapy_dir}")

        # 运行 Scrapy
        result = subprocess.run(
            ["scrapy", "crawl", spider_name],
            cwd=scrapy_dir,
            shell=True,  # Windows 可能需要 shell=True
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Scrapy 执行失败: {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def run_streamlit(data_file):
    """启动 Streamlit 并返回子进程对象"""
    try:
        streamlit_dir = os.path.join(os.getcwd(), "streamlit_app")
        process = subprocess.Popen(
            ["streamlit", "run", "app.py", "--", "--data-file", data_file],
            cwd=streamlit_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"启动 Streamlit 失败: {e}")
        return None

def handle_exit(signum, frame):
    """捕获退出信号，终止 Streamlit 进程"""
    print("\n正在关闭 Streamlit...")
    if streamlit_process:
        streamlit_process.terminate()  # 终止子进程
        streamlit_process.wait()       # 等待子进程退出
    sys.exit(0)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--spider", default="danbooru", help="要运行的爬虫名称")
    args = parser.parse_args()
    data_file = f"{args.spider}.json"

    # 注册信号处理器（Ctrl+C）
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # 运行 Scrapy
    if not run_scrapy(args.spider):
        sys.exit(1)

    # 启动 Streamlit
    streamlit_process = run_streamlit(data_file)
    if not streamlit_process:
        sys.exit(1)

    # 主线程循环等待（防止直接退出）
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_exit(None, None)
