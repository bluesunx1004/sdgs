# pages/08_08_energy_production.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ─────────────────────── 페이지 설정 ───────────────────────
st.set_page_config(page_title="🔋 에너지원별 발전량 변화", layout="wide")
st.title("🔋 우리나라 에너지원별 발전량 및 비중 변화 (SDG 7)")

# ─────────────────────── 데이터 로드 ───────────────────────
def read_csv(name):
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path)
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

df = read_csv("energy.csv")

# ─────────────────────── 데이터 전처리 ─────────────────────
df.columns = ["연도", "구분", "계", "원자력", "석탄", "LNG", "신재생", "유류", "양수", "기타"]
df = df.dropna(subset=["연도"])
df["연도"] = df["연도"].astype(int)
long_df = df.melt(id_vars=["연도", "구분"], var_name="에너지원", value_name="값")

# 발전량 데이터와 비중 데이터로 나누기
gen_df = long_df[long_df["구분"] == "발전량"]
rate_df = long_df[long_df["구분"] == "비중"]

# 수치형으로 변환 (천 단위 콤마 제거)
def to_numeric(series):
    return pd.to_numeric(series.astype(str).str.replace(",", ""), errors="coerce")

gen_df["값"] = to_numeric(gen_df["값"])
rate_df["값"] = to_numeric(rate_df["값"])

# ───────────────────── 시각화: 발전량 변화 ─────────────────────
st.markdown("### 📊 에너지원별 발전량 추세")

sel_sources = st.multiselect("에너지원 선택", gen_df["에너지원"].unique(),
                             default=["원자력", "석탄", "LNG", "신재생"])
plot_gen = gen_df[gen_df["에너지원"].isin(sel_sources)]

fig_gen = px.line(plot_gen, x="연도", y="값", color="에너지원",
                  markers=True, labels={"값": "발전량 (GWh)"},
                  title="에너지원별 발전량 추세")
fig_gen.update_layout(title_font_size=18)
st.plotly_chart(fig_gen, use_container_width=True)

# ───────────────────── 시각화: 에너지원 비중 변화 ──────────────
st.markdown("### 📈 에너지원별 비중(%) 변화")

sel_sources2 = st.multiselect("비중 확인 에너지원", rate_df["에너지원"].unique(),
                              default=["원자력", "석탄", "신재생"])
plot_rate = rate_df[rate_df["에너지원"].isin(sel_sources2)]

fig_rate = px.line(plot_rate, x="연도", y="값", color="에너지원",
                   markers=True, labels={"값": "비중 (%)"},
                   title="에너지원별 비중 변화")
fig_rate.update_layout(title_font_size=18)
st.plotly_chart(fig_rate, use_container_width=True)

# ───────────────────── SDG 연계 및 교육 요소 ────────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 우리나라에서 **신재생 에너지 비중**은 어떻게 변화해 왔나요?  
2. 여전히 **석탄 발전** 비중이 큰 이유는 무엇일까요?  
3. **SDG 7 ‘에너지의 지속가능성 확보’**를 달성하기 위해 어떤 변화가 필요할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **에너지 전환 이해**: 에너지원의 변화 추이를 통해 지속가능한 에너지 필요성 이해  
- **데이터 기반 사고력**: 수치 변화에서 정책적 흐름이나 환경 영향을 유추  
- **SDGs 통합적 접근**: 목표 7과 목표 13(기후변화 대응) 등과의 연계 학습
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역 조사 활동**: 지역 내 태양광/풍력/신재생 시설 탐방  
- **캠페인 디자인**: 에너지 절약 및 전환을 위한 포스터·영상 제작  
- **정책 제안서 작성**: 학생 관점에서 지속 가능한 에너지 정책 제안서 작성
""")

with st.expander("🔍 원본 데이터 미리보기"):
    st.dataframe(df)
