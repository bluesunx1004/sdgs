# -*- coding: utf-8 -*-
import streamlit as st
import os

# SDG 정보 (간단히 3개만 예시)
SDGS = [
    {
        "id": 1,
        "title": "빈곤 퇴치",
        "short": "모든 형태의 빈곤을 모든 곳에서 종식시키자.",
        "detail": "2030년까지 극심한 빈곤 상태의 인구를 0으로 줄이는 것이 목표입니다.",
        "example": "국내: 긴급복지 지원 제도\n해외: UNDP 마이크로금융 지원"
    },
    {
        "id": 2,
        "title": "기아 종식",
        "short": "기아를 종식하고 영양을 개선하자.",
        "detail": "지속가능한 농업 시스템을 촉진하여 모든 사람에게 안정적인 식량을 보장합니다.",
        "example": "국내: 무상급식\n해외: FAO 식량지원 프로그램"
    },
    {
        "id": 3,
        "title": "건강과 웰빙",
        "short": "모든 연령대의 건강한 삶을 보장하자.",
        "detail": "질병 예방, 정신 건강 개선, 출산 지원 등을 통해 보편적인 건강 시스템 구축을 지향합니다.",
        "example": "국내: 건강보험\n해외: WHO 백신 보급"
    },
]

st.set_page_config(page_title="SDGs 소개", layout="wide")
st.title("🌍 지속가능발전목표 (SDGs) 알아보기")
st.markdown("유엔이 정한 **17가지 지속가능발전목표(SDGs)** 를 살펴보세요!")

cols = st.columns(3)

for i, sdg in enumerate(SDGS):
    col = cols[i % 3]
    with col:
        with st.expander(f"🎯 {sdg['id']}. {sdg['title']}"):
            image_path = f"images/sdg{sdg['id']}.png"
            if os.path.exists(image_path):
                st.image(image_path, width=100)
            st.write(f"**간단 설명:** {sdg['short']}")
            st.write(f"**자세한 설명:** {sdg['detail']}")
            st.write(f"**사례:**\n{sdg['example']}")
