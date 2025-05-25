import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="미세먼지 예측", layout="wide")
st.title("🌫 미세먼지 시각화 및 예측")

# ✅ 예시 데이터 생성
@st.cache_data
def load_data():
    base_date = datetime.today() - timedelta(days=7)
    data = []
    for i in range(7):
        for city in ['서울', '부산', '대구']:
            date = base_date + timedelta(days=i)
            pm10 = np.random.randint(30, 80) + (5 if city == '서울' else 0)
            data.append({"날짜": date.date(), "지역": city, "PM10": pm10})
    return pd.DataFrame(data)

df = load_data()

# 🎯 지역 선택
city = st.selectbox("지역을 선택하세요", df['지역'].unique())
city_df = df[df['지역'] == city].copy().sort_values(by='날짜')

# 📈 최근 7일 시각화
st.subheader(f"📊 최근 7일간 {city} 미세먼지 (PM10) 농도")
fig = px.line(city_df, x='날짜', y='PM10', markers=True, title=f"{city} PM10 추이")
st.plotly_chart(fig, use_container_width=True)

# 🤖 사용자 입력 기반 예측: 원하는 "월"을 선택
st.subheader("🔮 원하는 달의 PM10 예측")

# 현재 날짜 기준 다음 6개월 중에서 선택
today = datetime.today()
month_options = [(today + timedelta(days=30*i)).strftime("%Y-%m") for i in range(1, 7)]
selected_month_str = st.selectbox("예측할 월을 선택하세요", month_options)

# 선택한 달의 첫날을 datetime 객체로 변환
selected_month = datetime.strptime(selected_month_str + "-01", "%Y-%m-%d")
last_date = datetime.combine(city_df['날짜'].max(), datetime.min.time())
days_ahead = (selected_month - last_date).days

def get_air_quality_grade(pm10):
    if pm10 <= 30:
        return "좋음", "😃 공기 상태가 매우 좋아요! 야외 활동하기에 적합합니다.", "success"
    elif pm10 <= 80:
        return "보통", "😐 공기 상태가 보통입니다. 민감군은 주의해주세요.", "info"
    elif pm10 <= 150:
        return "나쁨", "😷 공기가 탁해요. 가급적 외출을 자제하고, 마스크 착용을 권장합니다.", "warning"
    else:
        return "매우 나쁨", "😡 공기 질이 매우 나쁩니다. 외출을 삼가고 실내 환기도 주의하세요.", "error"

        
# 유효성 검사
if days_ahead < 1:
    st.warning("선택한 달은 이미 예측 범위 안에 있어요. 이후 달을 선택해 주세요.")
else:
    # ✅ 예측 및 등급 처리 코드: 전부 이 안에서만 실행해야 안전합니다
    X = np.arange(len(city_df)).reshape(-1, 1)
    y = city_df['PM10'].values
    model = LinearRegression()
    model.fit(X, y)

    target_index = np.array([[len(city_df) + days_ahead - 1]])
    predicted_pm10 = round(model.predict(target_index)[0], 2)

    grade, message, msg_type = get_air_quality_grade(predicted_pm10)

    st.success(f"📌 예측된 {selected_month_str}의 PM10 수치는 **{predicted_pm10} ㎍/m³** 입니다.")
    
    if msg_type == "success":
        st.success(f"🌬 예보된 등급: **{grade}**  \n{message}")
    elif msg_type == "info":
        st.info(f"🌬 예보된 등급: **{grade}**  \n{message}")
    elif msg_type == "warning":
        st.warning(f"🌬 예보된 등급: **{grade}**  \n{message}")
    else:
        st.error(f"🌬 예보된 등급: **{grade}**  \n{message}")
