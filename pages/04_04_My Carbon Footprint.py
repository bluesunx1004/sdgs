import streamlit as st

st.set_page_config(page_title="나의 탄소 발자국 계산기")
st.title("🌍 나의 탄소 발자국은 얼마일까?")

st.markdown("당신의 일상 습관을 입력하면 연간 **이산화탄소 배출량**을 계산해 드려요!")

# 입력값 받기
meat_days = st.slider("일주일에 고기를 먹는 날 수", 0, 7, 3)
car_km = st.number_input("하루에 자동차를 타는 거리 (km)", 0, 100, 10)
electricity_kwh = st.number_input("한 달 전기 사용량 (kWh)", 0, 1000, 300)

if st.button("계산하기"):
    # 단순 계산식
    meat_emission = meat_days * 52 * 2.5  # 1일 2.5kg CO2
    car_emission = car_km * 365 * 0.2     # 1km당 0.2kg CO2
    elec_emission = electricity_kwh * 12 * 0.5  # 1kWh당 0.5kg CO2

    total = round(meat_emission + car_emission + elec_emission, 2)

    st.metric("🥤 예상 연간 탄소 배출량", f"{total} kg CO₂")

    # 결과 등급
    if total < 3000:
        st.success("✅ 탄소 배출이 낮은 편이에요! 지구를 생각하는 습관, 멋져요 :)")
    elif total < 5000:
        st.warning("⚠️ 조금 더 절약하는 습관을 실천해보면 어때요?")
    else:
        st.error("🚨 탄소 배출이 높은 편이에요! 고기 섭취/이동수단을 줄여보세요.")
