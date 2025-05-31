import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 🌊 페이지 설정
st.set_page_config(page_title="해수면 상승 분석", layout="wide")
st.title("🌊 전지구 해수면 상승 분석 대시보드")

# 📂 데이터 불러오기
csv_path = os.path.join(os.path.dirname(__file__), "..", "sealevel_data_download.csv")
df = pd.read_csv(csv_path)

# 📆 연도별 열만 추출
year_cols = [col for col in df.columns if col.startswith("19") or col.startswith("20")]
df_long = df.melt(id_vars=["location", "country", "continent"], 
                  value_vars=year_cols, 
                  var_name="Year", 
                  value_name="Sea_Level_mm")

# 숫자형으로 변환
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
df_long.dropna(subset=["Year", "Sea_Level_mm"], inplace=True)

# 📈 전지구 해수면 평균 변화 추이 (국가 전체 평균)
avg_by_year = df_long.groupby("Year")["Sea_Level_mm"].mean().reset_index()

st.markdown("### 📈 전지구 평균 해수면 상승 추이")
fig = px.line(avg_by_year, x="Year", y="Sea_Level_mm",
              labels={"Sea_Level_mm": "해수면(mm)"},
              title="전지구 평균 해수면(GMSL) 변화 추이")
fig.update_layout(title_font_size=18)
st.plotly_chart(fig, use_container_width=True)

# 🌍 대륙별 해수면 변화 추이
st.markdown("### 🌍 대륙별 해수면 상승 비교")

continent_avg = df_long.groupby(["continent", "Year"])["Sea_Level_mm"].mean().reset_index()

fig2 = px.line(continent_avg, x="Year", y="Sea_Level_mm", color="continent",
               title="대륙별 평균 해수면 변화 추이", labels={"Sea_Level_mm": "해수면(mm)"})
fig2.update_layout(title_font_size=18, legend_title_text="대륙")
st.plotly_chart(fig2, use_container_width=True)

# 🔍 특정 국가 선택 분석
st.markdown("### 🔍 국가별 해수면 변화 분석")

selected_country = st.selectbox("분석할 국가를 선택하세요", sorted(df_long["country"].unique()))
country_df = df_long[df_long["country"] == selected_country]

fig3 = px.line(country_df, x="Year", y="Sea_Level_mm", color="location",
               title=f"{selected_country} 해수면 변화 추이", labels={"Sea_Level_mm": "해수면(mm)"})
fig3.update_layout(title_font_size=18, legend_title_text="관측소 위치")
st.plotly_chart(fig3, use_container_width=True)

# 💬 학생 토론 질문
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
- 해수면 상승이 우리 삶에 어떤 영향을 미칠 수 있을까요?
- 어떤 지역이 가장 큰 영향을 받을까요?
- 이 문제 해결을 위해 어떤 국제적 협력이 필요할까요?
""")

# 📚 교육적 함의
st.markdown("### 📚 교육적 함의")
st.markdown("""
- 해수면 상승은 기후 변화의 명확한 지표이며, SDGs 목표 중 '13. 기후 변화 대응'과 밀접한 관련이 있음  
- 과학적 데이터 분석을 통해 글로벌 이슈를 이해하고, 지역적 대응을 고민할 수 있는 기회 제공  
- 다양한 관측소 데이터를 통해 과학적 탐구 능력 강화
""")

# 🔍 확장 활동
st.markdown("### 🔍 확장 활동")
st.markdown("""
- 우리 지역의 해수면 변화나 기후 변화 현상 조사  
- 모의 유엔 회의 형식으로 기후 변화 대응 전략 발표  
- 해양 생태계 보존을 위한 캠페인 기획
""")
