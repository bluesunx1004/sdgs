import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="국가별 플라스틱 폐기물 현황", layout="wide")
st.title("📊국가별 플라스틱 폐기물 현황")

# 1. 국가별 플라스틱 폐기량
st.subheader("📊 상위 10개국 총 플라스틱 폐기량")

top10 = df.sort_values(by="Total_Plastic_Waste_MT", ascending=False).head(10)

fig1 = px.bar(top10,
              x="Country", y="Total_Plastic_Waste_MT",
              color="Main_Sources",
              title="플라스틱 폐기량 상위 10개국 (백만 톤 기준)")

st.plotly_chart(fig1, use_container_width=True)

# 2.국가 선택 분석기
st.subheader("🔍 국가별 분석기")
country = st.selectbox("국가를 선택하세요", df["Country"].unique())
row = df[df["Country"] == country].iloc[0]
st.metric("총 플라스틱 폐기량", f"{row['Total_Plastic_Waste_MT']} 백만 톤")
st.metric("재활용률", f"{row['Recycling_Rate']} %")
st.metric("1인당 배출량", f"{row['Per_Capita_Waste_KG']} kg")
st.info(f"해안 폐기물 위험도: **{row['Coastal_Waste_Risk']}**")

# 위험도 수치화 (선택적)
risk_map = {"Low": 1, "Medium": 2, "High": 3, "Very_High": 4}
df["Risk_Level_Num"] = df["Coastal_Waste_Risk"].map(risk_map)

# 샘플 국가 중심 좌표 추가 (간단 예시용)
coords = {
    "United States": [38.0, -97.0],
    "China": [35.0, 105.0],
    "India": [21.0, 78.0],
    "Indonesia": [-5.0, 120.0],
    "Brazil": [-10.0, -55.0],
    "Russia": [60.0, 100.0],
    "Germany": [51.0, 10.0],
    "Japan": [36.0, 138.0],
    "Philippines": [13.0, 122.0],
    "Vietnam": [16.0, 107.5],
}
df["lat"] = df["Country"].map(lambda x: coords.get(x, [None, None])[0])
df["lon"] = df["Country"].map(lambda x: coords.get(x, [None, None])[1])
df_map = df.dropna(subset=["lat", "lon"])

# 🌍 지도 시각화
fig = px.scatter_geo(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="Country",
    size="Total_Plastic_Waste_MT",
    color="Coastal_Waste_Risk",
    projection="natural earth",
    title="🌊 해양 플라스틱 폐기물 위험 국가 분포",
    color_discrete_map={
        "Low": "green",
        "Medium": "orange",
        "High": "red",
        "Very_High": "darkred"
    }
)
fig.update_layout(legend_title_text="Coastal Waste Risk")

st.plotly_chart(fig, use_container_width=True)

# 🎥 해양 쓰레기 유튜브 영상
st.subheader("🌊 해양 쓰레기 문제, 얼마나 심각할까요?")
col1, col2, col3 = st.columns([1, 2, 1])  # 가운데 2 비율만 차지

with col2:
    st.video("https://youtu.be/j7jCm0-7UiY?feature=shared")

# 🔁 지속 실천 독려
st.markdown("""
> 💡 오늘부터 작은 실천이 모여 큰 변화를 만들어냅니다.  
> 내일은 텀블러 하나, 에코백 하나 챙겨보는 건 어떨까요?
""")
