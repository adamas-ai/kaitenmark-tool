import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import io
import base64

st.set_page_config(page_title="グラフ差玉測定ツール", layout="wide")
st.title("🎯 サイトセブンのグラフ画像から差玉を推定")

# プライマリボタンの見た目変更（白背景）
st.markdown("""
<style>
button[kind="primary"] {
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # 画像読み込み
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # Base64変換してcanvas用に設定
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    background_url = f"data:image/png;base64,{img_str}"

    # 測定設定
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)

    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    # 操作モード
    drawing_option = st.radio("操作モードを選択", ("0ライン（青）", "終点ライン（赤）", "移動（パン）"))

    drawing_mode_map = {
        "0ライン（青）": "line",
        "終点ライン（赤）": "line",
        "移動（パン）": "pan"
    }

    line_colors = {
        "0ライン（青）": "rgba(0, 0, 255, 0.7)",    # 青
        "終点ライン（赤）": "rgba(255, 0, 0, 0.7)",  # 赤
    }

    stroke_width = 3 if drawing_option != "移動（パン）" else 0
    fill_color = line_colors.get(drawing_option, "rgba(0,0,0,0)") if drawing_option != "移動（パン）" else "rgba(0,0,0,0)"

    canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    background_image=image,  # ← PIL Image を直接指定
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode=drawing_mode_map[drawing_option],
    key="canvas"
)

    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        lines = [obj for obj in objs if obj["type"] == "line"]

        if len(lines) % 2 != 0:
            st.warning("ラインは0ラインと終点ラインのペアで引いてください（偶数本）")
        else:
            results = []
            for i in range(0, len(lines), 2):
                line0 = lines[i]
                line1 = lines[i + 1]
                dy = abs(line1["y1"] - line0["y1"])
                estimated_balls = int(dy * bullets_per_pixel)

                results.append({
                    "ペア": f"{i+1}-{i+2}",
                    "差(px)": round(dy, 1),
                    "推定差玉": estimated_balls
                })

            df = pd.DataFrame(results)

            # 色付き表示
            st.dataframe(df.style.applymap(
                lambda v: 'color: blue' if isinstance(v, str) and '-' in v else '', subset=['ペア']
            ).applymap(
                lambda v: 'color: red' if isinstance(v, (int, float)) and v > 0 else '', subset=['推定差玉'])
            )

            # LINE用テキスト
            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
