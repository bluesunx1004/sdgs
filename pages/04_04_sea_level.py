# climate_sealevel_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 페이지 설정
st.set_page_config(page_title="해수면 상승 분석 대시보드", layout="wide")
st.title("🌊 기후변화와 해수면 상승 분석")

# CSV 파일 불러오기
csv_path = Path("/mnt/data/sealevel_data_download.csv")  # 업로드한 파일 경로
df = pd.read_csv(csv_path)

# 데이터 전처리 (예: 컬럼 확인)
st.markdown("#### 데이터 미리보기")
st.dataframe(df.head())

# 년도별 해수면 상승 시각화
st.markdown("### 📈 연도별 해수면 상승 추세")
fig = px.line(df, x="Year", y="GMSL", title="전지구 평균 해수면(GMSL) 변화 추이", labels={"GMSL": "해수면(mm)"})
fig.update_layout(title_font_size=18)
st.plotly_chart(fig, use_container_width=True)

# 특정 기간 필터링
st.markdown("### 🔍 특정 기간 필터")
start_year, end_year = st.slider("연도 범위 선택", int(df["Year"].min()), int(df["Year"].max()), (1993, 2023))
filtered = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

fig2 = px.line(filtered, x="Year", y="GMSL", title=f"{start_year} ~ {end_year} 해수면 변화")
st.plotly_chart(fig2, use_container_width=True)

# 통계 지표 출력
st.markdown("### 📊 통계 정보")
st.metric("📏 평균 해수면(mm)", round(filtered["GMSL"].mean(), 2))
st.metric("📈 최대값", round(filtered["GMSL"].max(), 2))
st.metric("📉 최소값", round(filtered["GMSL"].min(), 2))

# 🌱 SDGs 연계 시각화 안내
st.markdown("### 🌱 SDGs와의 연계")
st.markdown("""
- **SDG 13 (기후 행동)**: 해수면 상승은 기후 변화의 직접적인 결과입니다. 탄소 배출 저감의 필요성을 강조합니다.  
- **SDG 14 (해양 생태계 보호)**: 해양 생태계와 해안 지역 커뮤니티에 직접적인 영향을 줍니다.
""")

# 💬 학생 토론 질문
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
- 해수면 상승은 어떤 국가나 지역에 더 큰 영향을 줄까요?
- 이러한 변화가 해양 생태계에 어떤 영향을 줄 수 있을까요?
- 기후 변화에 대응하기 위한 국제적 협력 방안은 무엇이 있을까요?
""")

# 📚 교육적 함의
st.markdown("### 📚 교육적 함의")
st.markdown("""
- 실제 데이터를 바탕으로 과학적 사실을 파악하고 비판적 사고 능력을 기를 수 있습니다.  
- 기후변화와 지속가능성의 상관관계를 이해하고 SDGs 목표와 실생활 연결을 경험할 수 있습니다.  
- 데이터 리터러시, 시각화, 환경 문제 해결 능력을 종합적으로 향상시킬 수 있습니다.
""")

# 🔍 확장 활동
st.markdown("### 🔍 확장 활동")
st.markdown("""
- 지역별 해수면 변화 자료를 추가로 조사하여 비교 분석  
- 기후 행동 캠페인 기획 및 실천 방안 제시  
- 데이터 기반의 뉴스 아티클 또는 인포그래픽 제작
""")
