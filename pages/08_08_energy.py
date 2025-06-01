# pages/08_08_energy.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────── 페이지 설정 ─────────────────────
st.set_page_config(page_title="🇰🇷 에너지원별 비중 분석", layout="wide")
st.title("🔋 우리나라 에너지원별 발전 비중 분석 (SDG 7)")

# ───────────────────── 데이터 불러오기 ──────────────────
def read_csv(name):
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path)
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

df = read_csv("energy.csv")
df.columns = df.columns.str.strip()
df["연도"] = df["연도"].astype(int)

# ───────────────────── 데이터 변환 ──────────────────────
df_long = df.melt(id_vars="연도", var_name="에너지원", value_name="비율(%)")

# ───────────────────── 비중 추세 그래프 ──────────────────
st.markdown("### 📈 에너지원별 비중 변화 추세")
sources = sorted(df_long["에너지원"].unique())
sel_sources = st.multiselect("분석할 에너지원 선택", sources, default=sources)

plot_df = df_long[df_long["에너지원"].isin(sel_sources)]
fig = px.line(plot_df, x="연도", y="비율(%)", color="에너지원", markers=True,
              title="에너지원별 발전 비중 변화",
              labels={"연도": "연도", "비율(%)": "비중 (%)"})
fig.update_layout(title_font_size=18, legend_title_text="에너지원")
st.plotly_chart(fig, use_container_width=True)

# ───────────────────── 특정 연도 비교 ───────────────────
st.markdown("### 📊 특정 연도별 에너지원 비중")
sel_year = st.slider("연도 선택", int(df["연도"].min()), int(df["연도"].max()), int(df["연도"].max()))
year_df = df[df["연도"] == sel_year].drop(columns="연도").T.reset_index()
year_df.columns = ["에너지원", "비율(%)"]

bar_fig = px.bar(year_df, x="에너지원", y="비율(%)", text="비율(%)",
                 title=f"{sel_year}년 에너지원별 비중")
bar_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
bar_fig.update_layout(yaxis_range=[0, max(year_df["비율(%)"]) + 10])
st.plotly_chart(bar_fig, use_container_width=True)

# ───────────────────── 데이터 미리보기 ───────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df)

# ───────────────────── SDG 연계 및 수업 요소 ────────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 어떤 에너지원이 시간이 지남에 따라 **증가하거나 감소**했나요?  
2. **신재생에너지의 비중**은 충분하다고 생각하나요? 왜 그런가요?  
3. **탄소중립 사회**로 전환하기 위해 어떤 에너지원의 확대가 필요할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **시계열 데이터 분석**을 통해 사회 변화 관찰  
- **에너지 정책**의 방향성과 SDG 7(모두를 위한 에너지)의 연결  
- **기후변화 대응**을 위한 에너지 전환 이해
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역별 에너지 사용 실태 조사 및 발표**  
- **국가 간 에너지원 비중 비교 분석**  
- **미래 에너지 포트폴리오 제안서 작성**
""")
