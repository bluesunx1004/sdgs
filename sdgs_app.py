# sdgs_app.py

import streamlit as st
import os

# 🔽 여기서 SDGs 정보를 직접 정의
SDGS = [
    {
        "id": 1,
        "title": "빈곤 퇴치",
        "short": "모든 형태의 빈곤을 모든 곳에서 종식시키자.",
        "detail": "전 세계적으로 극심한 빈곤 상태에 있는 사람들을 줄이기 위해 노력하고 있습니다. 2030년까지 하루 1.25달러 미만으로 살아가는 사람의 비율을 0%로 만드는 것이 목표입니다.",
        "example": "국내: 긴급복지 지원 제도\n해외: UNDP의 마이크로금융 지원"
    },
    {
        "id": 2,
        "title": "기아 종식",
        "short": "기아를 종식하고 식량 안보와 영양 개선을 달성하자.",
        "detail": "소득이 낮고 농업 기반이 취약한 국가에서 식량 생산성 향상 및 지속가능한 농업을 촉진하는 것이 핵심 목표입니다.",
        "example": "국내: 학교 무상급식\n해외: FAO의 식량 원조 프로그램"
    },
    # ... SDG 3 ~ 17 추가
]

# 🔽 UI 코드
st.set_page_config(page_title="SDGs 소개", layout="wide")
st.title("🌍 지속가능발전목표 (SDGs) 알아보기")
st.markdown("유엔이 채택한 **17가지 지속가능발전목표(SDGs)** 를 시각적으로 탐색해보세요!")

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
