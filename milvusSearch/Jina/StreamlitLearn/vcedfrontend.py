import streamlit as st
from jina import Client, DocumentArray, Document
import json
import os
import time
import uuid


DATA_PATH = f"{os.getcwd}/data"

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

if not os.path.exists(DATA_PATH + '/test/'):
    os.mkdir(DATA_PATH + "/test")

# jina的监听端口
PORT = 51258
# 创建Jina客户端
c = Client(host=f"grpc://localhost:{PORT}")


st.set_page_config(page_title="司法数据检索平台",page_icon="")
st.title("Welcome to Law Retrival")



#获取视频组件，视频组件上传
uploaded_file = st.file_uploader("选择一份文书文件")
file_name = None

if uploaded_file is not None:
    video_bytes = uploaded_file.read()
    st.video(video_bytes)

    # save file to disk for later process
    file_name = uploaded_file.name
    with open(f'',mode='wb') as file:
        file.write(video_bytes) # 将视频文件存到服务器本地

video_file_path = f"{DATA_PATH}/{file_name}"
uid = uuid.uuid1()

# 文本输入框
text_prompt = st.text_input(
    "Description", placeholder="please input the description", help='The description of clips from the video'
)


# top_k输入宽
top_value = st.text_input(

)



