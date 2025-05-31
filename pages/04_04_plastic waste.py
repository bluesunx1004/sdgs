import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 🌍 페이지 설정
st.set_page_config(page_title="국가별 플라스틱 폐기물 현황", layout="wide")
st.title("🌍 국가별 플라스틱 폐기물 현황 분석 대시보드")

# 데이터 로드
import os
import pandas as pd

base_path = os.getcwd()
csv_path = os.path.join(base_path, "Plastic Waste Around the World.csv")
df = pd.read_csv(csv_path)
# 위험도 수치화
risk_map = {"Low": 1, "Medium": 2, "High": 3, "Very_High": 4}
df["Risk_Level_Num"] = df["Coastal_Waste_Risk"].map(risk_map)

# 국가 좌표 (샘플용)
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

# 1️⃣ 플라스틱 폐기량 상위 10개국
st.markdown("### 📊 총 플라스틱 폐기량 상위 10개국")

top10 = df.sort_values(by="Total_Plastic_Waste_MT", ascending=False).head(10)

fig1 = px.bar(
    top10,
    x="Country",
    y="Total_Plastic_Waste_MT",
    color="Main_Sources",
    title="플라스틱 폐기량 상위 10개국 (단위: 백만 톤)"
)
fig1.update_layout(title_font_size=18, legend_title_text="주요 배출원")
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ 선택 국가 상세 분석
st.markdown("### 🔍 국가별 상세 분석기")

country = st.selectbox("국가를 선택하세요", df["Country"].unique())
row = df[df["Country"] == country].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("총 플라스틱 폐기량", f"{row['Total_Plastic_Waste_MT']} 백만 톤")
col2.metric("재활용률", f"{row['Recycling_Rate']} %")
col3.metric("1인당 배출량", f"{row['Per_Capita_Waste_KG']} kg")
st.info(f"🌊 해안 폐기물 위험도: **{row['Coastal_Waste_Risk']}**")

# 3️⃣ 해양 폐기물 위험도 지도 시각화
st.markdown("### 🗺️ 해양 플라스틱 폐기물 위험 국가 분포")

fig2 = px.scatter_geo(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="Country",
    size="Total_Plastic_Waste_MT",
    color="Coastal_Waste_Risk",
    projection="natural earth",
    title="해양 플라스틱 폐기물 위험도 세계 분포",
    color_discrete_map={
        "Low": "green",
        "Medium": "orange",
        "High": "red",
        "Very_High": "darkred"
    }
)
fig2.update_layout(title_font_size=18, legend_title_text="폐기물 위험도")
st.plotly_chart(fig2, use_container_width=True)

# 4️⃣ 토론 질문 및 교육적 확장
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
- 플라스틱 폐기물 문제는 왜 일부 국가에서 더 심각할까요?
- 우리나라는 현재 어떤 문제에 직면해 있을까요?
- 해결을 위해 국제적으로 어떤 협력이 필요할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- 데이터 분석을 통해 환경 문제의 지역적 특성과 국제적 연관성을 파악할 수 있음  
- 지속가능한 발전(SDGs) 목표 중 ‘12. 책임 있는 소비와 생산’, ‘14. 해양 생태계 보호’와 연계
""")

st.markdown("### 🔍 확장 활동")
st.markdown("""
- 실제 우리 지역 또는 학교 주변에서 플라스틱 사용량 조사  
- 대체 소재나 재사용 방안에 대한 캠페인 기획  
- SDGs 목표 중 하나를 골라 구체적인 실천방안 제시
""")
