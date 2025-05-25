import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="산불 피해 시각화", layout="wide")
st.title("🔥 연도별 국내 산불 피해 시각화 대시보드")

# ✅ 한글 폰트 설정 (NanumGothic.ttf 포함 방식 추천)
font_path = "NanumGothic.ttf"  # 프로젝트 안에 있어야 함
try:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    st.warning("폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")

plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("2015_2024 fire.csv")
    df.columns = df.columns.str.strip()
    df['연도'] = df['연도'].astype(str)
    return df

df = load_data()

# 📈 산불 발생 건수 그래프
st.subheader("📊 국내 연도별 산불 발생 건수")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df['연도'], df['발생 건 수'], marker='o', color='orangered')
ax1.set_xlabel("year")
ax1.set_ylabel("number")
#ax1.set_title("Number of forest fires by year")
ax1.grid(True)
st.pyplot(fig1)

# 📉 산불 피해면적 그래프
st.subheader("📏 국내 연도별 산불 피해 면적 (ha)")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(df['연도'], df['피해면적(ha)'], color='darkgreen')
ax2.set_xlabel("year")
ax2.set_ylabel("Damaged area(ha)")
#ax2.set_title("연도별 산불 피해면적")
ax2.grid(axis='y')
st.pyplot(fig2)

# 데이터 불러오기
@st.cache_data
def load_data():
    df2 = pd.read_csv("2025_monthly_fire.csv")
    return df2

df2 = load_data()

# 📌 Melt해서 월별/지역별로 시각화 가능한 형태로 변환
df2_melted = df2.melt(id_vars='지역', var_name='월', value_name='산불 발생 건수')
df2_melted['월'] = df2_melted['월'].astype(str)

# 📊 1. 월별 지역별 산불 발생 그래프
st.subheader("📊 월별 지역별 산불 발생 건수 (막대그래프)")
fig_bar = px.bar(
    df2_melted,
    x="월", y="산불 발생 건수",
    color="지역",
    barmode="group",
    title="월별 산불 발생 추이",
)
st.plotly_chart(fig_bar, use_container_width=True)

# 🔥 2. 지역별 월간 누적 히트맵
st.subheader("🗺 지역별 월별 산불 발생 건수 (히트맵)")
pivot_df2 = df2_melted.pivot(index="지역", columns="월", values="산불 발생 건수")
st.dataframe(pivot_df2.style.background_gradient(cmap='OrRd'), height=500)

# 📈 3. 총 발생 건수 순위
st.subheader("📈 지역별 산불 총합 순위")
df2_sum = df2.set_index("지역").sum(axis=1).sort_values(ascending=False)
st.bar_chart(df2_sum)
