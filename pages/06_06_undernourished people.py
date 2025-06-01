# pages/05_05_undernourished_korea.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────────── 페이지 설정 ─────────────────────────
st.set_page_config(page_title="🇰🇷 영양섭취부족 인구 분석", layout="wide")
st.title("🥕 우리나라 영양섭취부족 인구 시각화 (SDG 2)")

# ───────────────────────── 데이터 로드 ─────────────────────────
def read_csv(name):
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path)
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

age_df = read_csv("undernourished-ages.csv")   # Year, 01~02, 03~05 …
mf_df  = read_csv("undernourished-mf.csv")     # Year, 전국, 여성, 남성

# ───────────────────────── 전처리 ──────────────────────────────
age_long = age_df.melt(id_vars="Year",
                       var_name="Age_Group",
                       value_name="Percent")
mf_long  = mf_df.melt(id_vars="Year",
                      var_name="Sex",
                      value_name="Percent")

# ───────────────────────── 연령별 추세 ─────────────────────────
st.markdown("### 📈 연령대별 영양섭취부족 인구 비율 추세")

all_ages = sorted(age_long["Age_Group"].unique())
sel_age  = st.multiselect("비교할 연령대를 선택하세요", all_ages,
                          default=["03~05", "19~29", "65~"])
plot_age = age_long[age_long["Age_Group"].isin(sel_age)]

fig_age = px.line(plot_age, x="Year", y="Percent", color="Age_Group",
                  markers=True,
                  labels={"Percent": "영양섭취부족 비율(%)"},
                  title="연령대별 영양섭취부족 추세")
fig_age.update_layout(title_font_size=18, legend_title_text="연령대")
st.plotly_chart(fig_age, use_container_width=True)

# ───────────────────────── 성별 추세 ───────────────────────────
st.markdown("### 👩‍🦰👨‍🦰 성별 영양섭취부족 인구 비율 추세")

fig_sex = px.line(mf_long, x="Year", y="Percent", color="Sex",
                  markers=True,
                  labels={"Percent": "영양섭취부족 비율(%)"},
                  title="성별 영양섭취부족 추세")
fig_sex.update_layout(title_font_size=18, legend_title_text="성별")
st.plotly_chart(fig_sex, use_container_width=True)

# ───────────────────────── 특정 연도 비교(막대) ────────────────
st.markdown("### 📊 특정 연도의 연령·성별 비교")

sel_year = st.slider("연도 선택", int(age_df["Year"].min()),
                     int(age_df["Year"].max()),
                     int(age_df["Year"].max()))

age_year = age_df[age_df["Year"] == sel_year].melt(id_vars="Year",
                                                   var_name="Age_Group",
                                                   value_name="Percent")
sex_year = mf_df[mf_df["Year"] == sel_year].melt(id_vars="Year",
                                                 var_name="Sex",
                                                 value_name="Percent")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### 🧒 연령대별 ({sel_year}년)")
    st.bar_chart(age_year.set_index("Age_Group")["Percent"])
with col2:
    st.markdown(f"#### ⚥ 성별 ({sel_year}년)")
    st.bar_chart(sex_year.set_index("Sex")["Percent"])

# ───────────────────────── 데이터 미리보기 ──────────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.write("연령별 데이터", age_df.head())
    st.write("성별 데이터", mf_df.head())

# ───────────────────────── SDG 연계 & 교육 요소 ────────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 어떤 **연령대**에서 영양섭취부족 비율이 높게 나타나나요? 그 이유는 무엇일까요?  
2. 같은 연령대라도 **성별**에 따라 차이가 나는 이유는 무엇일까요?  
3. **SDG 2 ‘Zero Hunger’** 달성을 위해 우리 사회가 우선적으로 개선해야 할 점은 무엇일까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **데이터 해석 능력**: 연령·성별에 따라 건강 지표가 어떻게 달라지는지 이해  
- **정책 분석**: 보건·복지 정책의 우선순위를 데이터로 판단  
- **SDGs 통합 학습**: 목표 2(기아 종식)와 목표 3(건강과 웰빙)의 상호 연계성 탐구
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역 조사**: 학교·지역사회 식생활 실태 조사 후 개선 방안 제안  
- **캠페인 기획**: 특정 취약 연령층 대상 균형 잡힌 식단 캠페인 디자인  
- **국제 비교**: 다른 국가의 영양실조·섭취부족 통계와 비교 분석, 해결 사례 연구
""")
