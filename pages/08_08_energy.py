# pages/08_08_energy.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────────── 페이지 설정 ─────────────────────────
st.set_page_config(page_title="⚡ 에너지원별 발전량 분석", layout="wide")
st.title("⚡ 우리나라 에너지원별 발전량 분석 (SDG 7)")

# ───────────────────────── 데이터 로드 ─────────────────────────
def read_csv(name):
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path)
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

df = read_csv("energy.csv")  # 연도, 에너지원, 발전량(기가와트시)

# ───────────────────────── 전처리 ──────────────────────────────
df = df.dropna()
df.columns = df.columns.str.strip()
df["연도"] = df["연도"].astype(int)
df["발전량"] = pd.to_numeric(df["발전량"], errors="coerce")
df = df.dropna()

# 발전 비중 계산
total_by_year = df.groupby("연도")["발전량"].sum().reset_index(name="총발전량")
rate_df = df.merge(total_by_year, on="연도")
rate_df["비중"] = (rate_df["발전량"] / rate_df["총발전량"]) * 100

# ───────────────────────── 발전량 추세 ─────────────────────────
st.markdown("### 📈 에너지원별 발전량 추세")

all_sources = sorted(df["에너지원"].unique())
sel_sources = st.multiselect("확인할 에너지원 선택", all_sources,
                             default=["석탄", "천연가스", "신재생"])
plot_df = df[df["에너지원"].isin(sel_sources)]

fig1 = px.line(plot_df, x="연도", y="발전량", color="에너지원",
               markers=True,
               labels={"발전량": "발전량(GWh)"},
               title="에너지원별 발전량 변화")
fig1.update_layout(title_font_size=18, legend_title_text="에너지원")
st.plotly_chart(fig1, use_container_width=True)

# ───────────────────────── 발전 비중 추세 ──────────────────────
st.markdown("### 📊 에너지원별 발전 비중 추세")

# 기본값으로 존재하는 항목만 선택
available_sources = sorted(rate_df["에너지원"].dropna().unique())
default_sources = [src for src in ["원자력", "석탄", "신재생"] if src in available_sources]

sel_sources2 = st.multiselect("비중 확인 에너지원", available_sources,
                              default=default_sources)
plot_rate = rate_df[rate_df["에너지원"].isin(sel_sources2)]

fig2 = px.line(plot_rate, x="연도", y="비중", color="에너지원",
               markers=True,
               labels={"비중": "발전 비중(%)"},
               title="에너지원별 발전 비중 변화")
fig2.update_layout(title_font_size=18, legend_title_text="에너지원")
st.plotly_chart(fig2, use_container_width=True)

# ───────────────────────── 데이터 미리보기 ──────────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df.head())

# ───────────────────────── SDGs 연계 콘텐츠 ─────────────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 우리나라에서 **가장 많이 사용되는 에너지원**은 무엇인가요?  
2. 발전 비중이 **줄어드는 에너지원**과 **늘어나는 에너지원**은 무엇인가요?  
3. **SDG 7 'Affordable and Clean Energy'** 달성을 위해 어떤 에너지원이 확대되어야 할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **데이터 기반 환경 분석**: 에너지 생산 방식에 따른 사회·환경적 영향 이해  
- **에너지 전환 정책 탐구**: 국가별 에너지 전략과 SDGs 목표의 연계성 고찰  
- **과학-사회 융합 학습**: 지속가능한 과학 기술과 정책의 상호작용 학습
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역 에너지 조사**: 지역 내 태양광, 풍력 등 신재생 에너지 시설 현황 조사  
- **국제 비교 분석**: 다른 나라의 에너지 믹스 및 탄소 배출과의 상관관계 탐색  
- **미래 에너지 제안**: 우리 사회가 추구해야 할 미래 에너지 구성을 데이터로 설계
""")
