import streamlit as st
import pandas as pd
from collections import defaultdict
import numpy as np

uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.sidebar.write("ファイルの内容：")
    st.sidebar.dataframe(df)
    dct = defaultdict(list)
    column_names = df.columns.tolist()
    for idx, row in df.iterrows():
        key = (row['品番'], row['外径'])
        dct[key].append((row['値段'], row['在庫数']))

    def find_screws(diameter, weight):
        try:
            weight = np.float64(weight)
            key = (diameter, weight)
            return dct[key]
        except ValueError:
            return 0
        
    if "messages" not in st.session_state:
        # 辞書形式で定義
        st.session_state["messages"] = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("品番と外径を改行区切りで入力してください"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        L = prompt.split('\n')

        if(len(L) < 2):
            response = "要素数が少ないです。  \n・品番  \n・外径  \nの順番に入力してください"
            print(response)
        elif(len(L) > 2):
            response = "要素数が多いです。  \n・品番  \n・外径  \nの順番に入力してください"
            print(response)
        else:
            p_id,diameter = L[0], L[1]
            if diameter and p_id:
                result = find_screws(p_id,diameter)
                if result == 0:
                    response = f"""
                                品番 : {p_id}  \n
                                外径 : {diameter}  \n
                                は正しい入力形式ではありません。(カンマや空白などが入っていない確認してください)  \n
                                """
                elif result:
                    response = f"""
                                見つかりました。  \n
                                品番 : {p_id}  \n
                                外径 : {diameter}  \n
                                価格 : {result[0][1]} \n
                                在庫 : {result[0][0]}  \n
                                """
                else:
                    response = f"""
                                品番 : {p_id}  \n
                                外径 : {diameter}  \n
                                に該当するものは見つかりませんでした。  \n
                                """
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})