import streamlit as st
from numpy import char
from openai import OpenAI
from datetime import datetime  # 获取当前时间
import os
import json
# 页面设置
st.set_page_config(
    page_title="AI 智能伴侣", # 页面标题
    page_icon="🤖", # 页面图标
    # 布局
    layout="wide",
    # 侧边栏状态
    initial_sidebar_state="expanded",
    # 菜单栏按钮
    menu_items={}
)

# 获取当前格式化时间
def get_now_time():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# 保存会话信息
def save_session():
    if st.session_state.current_session:
        print("----------> 保存会话信息：")
        session_data = {
            "nick_name":st.session_state.nick_name,
            "character":st.session_state.character,
            "current_session": st.session_state.current_session,
            "messages":st.session_state.messages
        }

        # 构建session目录
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 创建会话文件
        with open(f"sessions/{st.session_state.current_session}.json","w",encoding = "utf-8") as f:
            json.dump(session_data,f,ensure_ascii=False,indent=4)
            print("保存成功")

# 新建会话
def new_session():
    st.session_state.messages = []
    st.session_state.current_session = get_now_time()

# 获取会话列表信息
def get_session_list():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions") # 文件列表
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5]) # 切片
    return session_list

# 加载指定会话
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)  # 转为字典
                # 保存会话信息
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.character = session_data["character"]
                st.session_state.current_session = session_data["current_session"]
                st.session_state.messages = session_data["messages"]
    except:
        st.error("加载会话失败") # 错误提示

# 删除指定会话
def delete_session(session_name):
    try:
        path = f"sessions/{session_name}.json"
        if os.path.exists(path):
            os.remove(path)
            if st.session_state.current_session == session_name:
                new_session()
    except:
        st.error("删除会话失败")
# 大标题
st.title("AI智能伴侣")


# logo
st.logo("resources/ai-partner-logo.jpg")

# 创建与AI大模型交互的客户端对象（使用的大模型集成网站推理时代的APIKEY）
client = OpenAI(
    api_key=("your-api-key"),
    base_url="your-base-url"
)

# 系统提示词
system_prompt = f"""
        你是 %s，是用户的真实伴侣，请完全代入伴侣角色
        规则：
            1.每次只回一条消息
            2.禁止任何场景或状态描述性文字
            3.匹配用户的语言
            4.回答简短，像微信聊天一样
            5.可酌情使用emoji表情
            6.回复的内容要充分体现伴侣的性格特征
            7.用符合伴侣性格的方式对话
        伴侣性格：
            - %s
        你必须遵守以上规则来回复用户
"""

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = [] # 列表存储聊天信息

# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"

# 性格
if "character" not in st.session_state:
    st.session_state.character = "温柔的东北姑娘"

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = get_now_time()

st.text(f"会话名称：{st.session_state.current_session}")

# 展示聊天信息
for message in st.session_state.messages: # {"role": "user", "content": prompt}
    st.chat_message(message["role"]).write(message["content"])


# 左侧的侧边栏 with: python 中的一个上下文管理器
with st.sidebar:
    # 会话信息
    st.sidebar.subheader("AI控制面板")

    # 新建会话
    if st.button("新建会话",width = "stretch",icon="🖋️"): # 按钮，宽度铺满侧边栏，图标

        save_session()
        if st.session_state.messages:
            new_session()
        st.rerun()  # 因为按钮点击，会先重新渲染页面再执行内部逻辑，所以需要重新运行

    # 历史会话管理
    st.text("历史会话")
    with st.container(height=150):
        session_list = get_session_list()
        if not session_list:
            st.info("暂无历史会话") # 提示信息
        else:
            for session in session_list:
                col1, col2 = st.columns([4, 1])  # 创建两个列，代码块

                # 当前会话高亮
                if session == st.session_state.current_session:
                    b_type = "primary"
                else:
                    b_type = "secondary"

                with col1:
                    if st.button(session, use_container_width= True, icon="📝", key=f"load_{session}",type = b_type):  # 设置key，标识不同组件，保证渲染正确
                        load_session(session)
                        st.rerun() # 踩坑点：rerun()必须和按钮同一级，否则页面渲染出错
                with col2:
                    if st.button("", use_container_width= True, icon="❌", key=f"delete_{session}"):
                        delete_session(session)
                        st.rerun()


    # 伴侣信息
    st.sidebar.subheader("伴侣信息")
    # 昵称输入框 （text -> 单行文本框）
    nick_name = st.text_input("昵称",placeholder= "请输入昵称", value=st.session_state.nick_name) # placeholder: 占位符（提示文本;value: 默认值）
    if nick_name:
        st.session_state.nick_name = nick_name # 若输入，则覆盖保存
    # 性格输入框 (area -> 多行文本框）
    character = st.text_area("性格",placeholder="请输入性格", value=st.session_state.character)
    if character:
        st.session_state.character = character # 若输入，则覆盖保存


# 聊天输入框
prompt = st.chat_input("请输入您的问题...")
if prompt:  # 字符串自动转换为布尔值
    st.chat_message("user").write(prompt) # 展示消息内容
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    response = client.chat.completions.create(
        model="your-model-id",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name,st.session_state.character)},
            # % 意思是：将%s替换成后面的参数，字符串格式化
            *st.session_state.messages
        ],
        stream=True # 启用流式传输，此时reponse接受多个数据块，而不是一个字符串
    )
    # 大模型返回的结果（非流式输出的解析方式）
    # output = response.choices[0].message.content
    # print("<---------- AI大模型返回结果：",output)
    # st.chat_message("assistant").write(output)

    # 大模型返回的结果（流式输出的解析方式）
    response_message =  st.empty() # 创建一个空的组件，用于展示大模型返回的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()