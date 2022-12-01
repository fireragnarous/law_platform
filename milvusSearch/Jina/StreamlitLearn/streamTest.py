import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(page_title="图文多模态检索模型测试")

st.title('这是你的第一个Streamlit主页!')

st.markdown('') # 可以直接渲染markdown

code = '''def hello():
            print("Hello, Streamlit") ''' # code

df = pd.DataFrame(
    np.random.randn(50,20),
    columns=('col %d' % i for i in range(20)))


st.dataframe(df)

st.latex(r'''
    a^2 + b^2 + c^2 = (a+b+c)^2 - 2ab-2bc-2ac  \\
    
    \sum_{k=0}^{k=N}((a_k+b_k)^2+(a_k-b_k)^2) = 2* \sum_{k=0}^{k=N}a_k^2 +  2 * \sum_{k=0}^{k=N}b_k^2

''')