import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 페이지 설정
st.set_page_config(page_title="산불 피해 시각화", layout="wide")
st.title("🔥 2015–2024 산불 피해 시각화 대시보드")

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
st.subheader("📊 연도별 산불 발생 건수")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df['연도'], df['발생 건 수'], marker='o', color='orangered')
ax1.set_xlabel("year")
ax1.set_ylabel("number")
#ax1.set_title("Number of forest fires by year")
ax1.grid(True)
st.pyplot(fig1)

# 📉 산불 피해면적 그래프
st.subheader("📏 연도별 산불 피해 면적 (ha)")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(df['연도'], df['피해면적(ha)'], color='darkgreen')
ax2.set_xlabel("year")
ax2.set_ylabel("Damaged area(ha)")
#ax2.set_title("연도별 산불 피해면적")
ax2.grid(axis='y')
st.pyplot(fig2)
