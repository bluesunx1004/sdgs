import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 데이터 불러오기
file_path = "sealevel_data_download.csv"
df = pd.read_csv(file_path)

# 페이지 설정
st.set_page_config(page_title="📈 해수면 상승과 SDGs", layout="wide")
st.title("📈 해수면 상승과 지속가능발전목표(SDGs)")

# -------------------
# 1️⃣ 연도별 해수면 평균 변화 추이
# -------------------
year_columns = [col for col in df.columns if col.isnumeric()]
df_yearly = df[year_columns].mean().reset_index()
df_yearly.columns = ["Year", "Avg_Sea_Level"]
df_yearly["Year"] = df_yearly["Year"].astype(int)

st.markdown("### 🌊 전 세계 평균 해수면 변화 추이")
fig_line = px.line(df_yearly, x="Year", y="Avg_Sea_Level", markers=True,
                   labels={"Avg_Sea_Level": "해수면(mm)"},
                   title="연도별 평균 해수면 변화")
fig_line.update_layout(title_font_size=18)
st.plotly_chart(fig_line, use_container_width=True)

# -------------------
# 2️⃣ 해수면 상승량 상위 지역
# -------------------
# -------------------
# 2️⃣ 해수면 상승량 상위 지역
# -------------------
df["Change_1978_2018"] = df["2018"] - df["1978"]
top_rising = df.sort_values(by="Change_1978_2018", ascending=False).head(10).copy()

# 지역 + 국가명 조합 컬럼 추가
top_rising["location_country"] = top_rising["location"] + " (" + top_rising["country"] + ")"

st.markdown("### 📌 해수면 상승이 큰 지역 Top 10")
fig_bar = px.bar(top_rising, 
                 x="location_country", 
                 y="Change_1978_2018", 
                 color="continent",
                 title="1978~2018년 해수면 상승량 상위 지역",
                 labels={"Change_1978_2018": "해수면 상승(mm)", "location_country": "지역 (국가)"})
fig_bar.update_layout(title_font_size=18, xaxis_tickangle=-30)
st.plotly_chart(fig_bar, use_container_width=True)


# -------------------
# 3️⃣ 국가별 상세 분석
# -------------------
st.markdown("### 🔍 특정 지역 상세 해수면 변화 분석")

# 지역 + 국가명으로 표시
df["location_country"] = df["location"] + " (" + df["country"] + ")"
location_map = dict(zip(df["location_country"], df["location"]))

selected_display = st.selectbox("지역 선택", df["location_country"].sort_values())
selected_location = location_map[selected_display]  # 실제 location 값

row = df[df["location"] == selected_location].iloc[0]

# 해수면 시계열
sea_level_series = row[year_columns].reset_index()
sea_level_series.columns = ["Year", "Sea_Level"]
sea_level_series["Year"] = sea_level_series["Year"].astype(int)

fig_detail = px.line(sea_level_series, x="Year", y="Sea_Level", 
                     title=f"{selected_location} ({row['country']}) 해수면 변화 추이")
st.plotly_chart(fig_detail, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("1978년 해수면", f"{row['1978']} mm")
col2.metric("2018년 해수면", f"{row['2018']} mm")
col3.metric("총 변화량", f"{row['Change_1978_2018']} mm")

# -------------------
# 4️⃣ 토론 질문 및 교육적 함의
# -------------------
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
- 해수면 상승이 어떤 방식으로 우리 삶에 영향을 미칠까요?
- 기후 변화와 해수면 상승 간의 연관성은 무엇일까요?
- 우리 지역은 해수면 상승에 얼마나 취약할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- 데이터를 통해 기후 변화의 구체적인 지표를 해석할 수 있음  
- 지역과 글로벌 문제 간의 연계를 탐색하며 SDG 13(기후행동), SDG 14(해양생태계 보호)와 연결  
- 과학적 근거 기반의 문제 해결 능력 강화
""")

st.markdown("### 🔍 확장 활동")
st.markdown("""
- 우리 지역 해안선 지도 위에 예상 해수면 상승선을 그려보기  
- 해안 도시들의 대응 사례를 조사하고 발표  
- 해수면 상승을 막기 위한 국제 협력 사례 조사 및 토론
""")
