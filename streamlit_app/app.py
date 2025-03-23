
import streamlit as st
import json
import os
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("--data-file", default="danbooru.json", help="数据文件名")
args = parser.parse_args()

# 统一数据目录路径
data_dir = os.path.join(os.path.dirname(os.getcwd()), "data")
data_path = os.path.join(data_dir, args.data_file)

st.info('This is a purely informational message', icon="ℹ️")

# 展示数据
st.title("图片展示应用")
try:
    with open(data_path, 'r', encoding='utf-8') as f:
        images = json.load(f)
        for img in images:
            st.image(img['preview_img'], caption=img.get('id', ''))
except FileNotFoundError:
    st.error(f"文件 {args.data_file} 不存在！请先运行对应爬虫。")
