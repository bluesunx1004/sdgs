# pages/09_09_employment_rate.py
"""
청년 고용 동향 분석 – SDG 8 (양질의 일자리와 경제 성장)
이 페이지는 employmentrate.csv 파일(2010‑2024)을 활용해 우리나라 청년 고용 지표를 시각화하고,
학생 토론‧교육적 함의‧확장 활동을 제시합니다.
"""

# ───────────────────── 라이브러리 ─────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────── 페이지 설정 ─────────────────────
st.set_page_config(page_title="🇰🇷 청년 고용 동향 분석", layout="wide")
st.title("👩‍💼 우리나라 청년 고용 동향 분석 (SDG 8)")

# ───────────────────── 데이터 불러오기 ──────────────────

def read_csv(name: str) -> pd.DataFrame:
    """앱 폴더 상위(root)에 있는 CSV를 읽거나, 업로드 위젯 제공"""
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path, encoding="utf-8-sig")
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

raw = read_csv("employmentrate.csv")

# ───────────────────── 데이터 전처리 ─────────────────────
raw = raw.set_index("Unnamed: 0").T  # 행·열 전치, 지표를 열로
raw.index.name = "연도"

# 쉼표 제거 & 실수형 변환
raw = raw.applymap(lambda x: float(str(x).replace(",", "")))

# 지표 계산: 고용률, 경제활동참가율
raw["고용률(%)"] = raw["취업자"] / raw["경제활동인구"] * 100
raw["참여율(%)"] = raw["경제활동인구"] / raw["생산가능인구"] * 100

# 연도 열을 앞으로, int 변환
raw = raw.reset_index()
raw["연도"] = raw["연도"].astype(int)

# ───────────────────── 롱 데이터 변환 ────────────────────
df_long = raw.melt(id_vars="연도", var_name="지표", value_name="값")

# ───────────────────── 비중 추세 그래프 ──────────────────
st.markdown("### 📈 연도별 주요 지표 추이")
metrics = sorted(df_long["지표"].unique())
sel_metrics = st.multiselect("분석할 지표 선택", metrics, default=["경제활동인구", "취업자", "실업률", "고용률(%)"])

plot_df = df_long[df_long["지표"].isin(sel_metrics)]
fig = px.line(plot_df, x="연도", y="값", color="지표", markers=True,
              title="청년 고용 주요 지표 연도별 추이",
              labels={"연도": "연도", "값": "값"})
fig.update_layout(title_font_size=18, legend_title_text="지표")
st.plotly_chart(fig, use_container_width=True)

# ───────────────────── 특정 연도 지표 비교 ────────────────
st.markdown("### 📊 특정 연도별 지표 값")
sel_year = st.slider("연도 선택", int(raw["연도"].min()), int(raw["연도"].max()), int(raw["연도"].max()))

year_df = raw[raw["연도"] == sel_year].drop(columns="연도").T.reset_index()
year_df.columns = ["지표", "값"]

bar_fig = px.bar(year_df, x="지표", y="값", text="값",
                 title=f"{sel_year}년 청년 고용 지표 현황")
bar_fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
bar_fig.update_layout(yaxis_range=[0, year_df["값"].max() * 1.15])
st.plotly_chart(bar_fig, use_container_width=True)

# ───────────────────── 데이터 미리보기 ───────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(raw)

# ───────────────────── SDG 연계 및 수업 요소 ───────────────

st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. **실업률이 가장 높았던 해**는 언제이며, 그 해의 사회·경제적 요인은 무엇이었나요?  
2. **고용률과 실업률**이 항상 반비례하지 않는 이유는 무엇일까요?  
3. **코로나19**(2020년경)가 청년 고용에 미친 영향은 어떻게 나타났나요?  
4. SDGs **목표 8** 관점에서 _"양질의 일자리"_ 는 무엇을 의미하며, 청년층에게 왜 중요할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **자료 해석력 향상**: 국가 통계 시계열 해석을 통해 수리적·비판적 사고력 강화  
- **사회·경제 구조 이해**: 청년 고용 변화와 정책의 상관관계를 탐구  
- **지속가능발전 목표 접목**: 데이터 기반으로 _포용적·지속가능한 성장_ 의 필요성 고찰
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역·성별 데이터 추가 분석**으로 고용 격차 탐색  
- 과거 추세를 활용한 **미래 고용률 예측 모델**(선형 회귀 등) 실습  
- **청년 인터뷰/설문 프로젝트**: 통계 수치와 실제 경험 비교  
- **정책 제안서 작성**: 데이터 근거로 청년 고용 개선 방안 제시
""")

# ───────────────────── 푸터 ──────────────────────────
st.info("데이터 출처: 통계청 청년 고용 동향(2010–2024) | © 2025, 교육용 예시 스크립트")
