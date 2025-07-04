import streamlit as st

st.title("回転率マークツール")

date = st.text_input("日付")
shop = st.text_input("店名")
machine = st.text_input("機種名")
number = st.text_input("台番号")
hits = st.number_input("総打ち込み玉数", min_value=0)
spins = st.number_input("総回転数", min_value=0)

if hits > 0 and spins > 0:
    rotation = (250 * spins) / hits
    st.success(f"回転率: {rotation:.2f} 回転／250玉")
    st.write("---")
    st.write(f"🗓 日付: {date}")
    st.write(f"🏪 店名: {shop}")
    st.write(f"🎰 機種名: {machine}")
    st.write(f"🎯 台番号: {number}")
    st.write(f"🔢 打ち込み玉数: {hits}")
    st.write(f"🔁 総回転数: {spins}")
else:
    st.info("打ち込み玉数と総回転数を入力してください。")
