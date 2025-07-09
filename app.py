import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="回転率推定ツール", layout="wide")
st.title("🎰 グラフ画像から回転率を推定")

st.markdown("""
このツールでは、サイトセブンの出玉グラフ画像を使って
**「0ラインと終点の差」から打ち込み玉数を自動計算し、回転率を推定**します。

---
1. 画像をアップロードしてください（サイトセブンの出玉グラフ）
2. 目盛線（例：-10,000〜-20,000）の間隔（mm）を入力
3. 画像上で 0ラインとグラフ終点のペアを **複数** 指定してください（左から順に2点1組）
4. 各台の「通常回転数」を入力（複数行対応）
---
""")

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    width, height = image.size

    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("-10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("画面上での-10,000〜-20,000の距離（ピクセル）", min_value=10, max_value=300, value=100)

    # mm換算率
    mm_per_pixel = pixel_distance / pixel_length  # mm / px
    bullets_per_mm = 1000  # 1mm = 1,000発
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    st.subheader("🖱️ 画像上で0ラインと終点をクリック（複数可、2点1組）")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # 赤半透明
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="freedraw",
        key="canvas",
    )

    points = canvas_result.json_data["objects"] if canvas_result.json_data else []
    click_points = [p["top"] for p in points if p["type"] == "rect"]  # rectでy座標取得

    if len(click_points) >= 2 and len(click_points) % 2 == 0:
        st.success(f"{len(click_points) // 2}台分のクリックを検出しました。")

        st.markdown("### 🔁 通常回転数（上から順に改行で複数台分入力）")
        input_str = st.text_area("例：\n825\n1034\n751", height=150)
        try:
            rotation_list = list(map(int, input_str.strip().split("\n")))
        except:
            rotation_list = []

        if len(rotation_list) != len(click_points) // 2:
            st.warning("通常回転数の数がクリックペア数と一致しません。")
        else:
            results = []
            for i in range(0, len(click_points), 2):
                y0 = click_points[i]
                y1 = click_points[i + 1]
                pixel_diff = abs(y0 - y1)
                bullets = pixel_diff * bullets_per_pixel
                rotation = rotation_list[i // 2]
                rpm = rotation / bullets * 250 if bullets > 0 else 0
                
                evaluation = "✗" if rpm <= 18.0 else "△" if rpm <= 19.5 else "○"

                results.append({
                    "通常回転数": rotation,
                    "推定打ち込み玉数": int(bullets),
                    "回転率": round(rpm, 2),
                    "評価": evaluation,
                })

            st.markdown("### 📊 結果")
            st.dataframe(results)

            st.markdown("### 📤 LINE共有用")
            lines = []
            for r in results:
                lines.append(f"🔁{r['通常回転数']}回 / 💣{r['推定打ち込み玉数']}発 → 📈{r['回転率']}回 → {r['評価']}")
            st.text_area("コピー用メッセージ", "\n".join(lines), height=150)
    else:
        st.info("0ラインと終点を2点1組でクリックしてください。")
