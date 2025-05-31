import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("Plastic Waste Around the World.csv") 

# 🌐 페이지 설정
st.set_page_config(page_title="국가별 플라스틱 폐기물 현황", layout="wide")
st.title("🌍 국가별 플라스틱 폐기물 현황 분석 대시보드")

# 1. 국가별 플라스틱 폐기량
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

# 2. 국가 선택 분석기
st.markdown("### 🔍 선택 국가 분석기")

country = st.selectbox("국가를 선택하세요", df["Country"].unique())
row = df[df["Country"] == country].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("총 플라스틱 폐기량", f"{row['Total_Plastic_Waste_MT']} 백만 톤")
col2.metric("재활용률", f"{row['Recycling_Rate']} %")
col3.metric("1인당 배출량", f"{row['Per_Capita_Waste_KG']} kg")
st.info(f"해안 폐기물 위험도: **{row['Coastal_Waste_Risk']}**")

# 위험도 수치화
risk_map = {"Low": 1, "Medium": 2, "High": 3, "Very_High": 4}
df["Risk_Level_Num"] = df["Coastal_W
