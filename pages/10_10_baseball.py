import streamlit as st
import pandas as pd
import pydeck as pdk

# MLB 팀 정보 예시 데이터
teams = [
    {
        "team": "New York Yankees",
        "city": "New York, NY",
        "lat": 40.8296,
        "lon": -73.9262,
        "representative_player": "Aaron Judge",
        "player_stats": "2022: 62 HR, .311 AVG, 131 RBI"
    },
    {
        "team": "Los Angeles Dodgers",
        "city": "Los Angeles, CA",
        "lat": 34.0739,
        "lon": -118.2396,
        "representative_player": "Mookie Betts",
        "player_stats": "2022: 35 HR, .269 AVG, 82 RBI"
    },
    {
        "team": "Chicago Cubs",
        "city": "Chicago, IL",
        "lat": 41.9484,
        "lon": -87.6553,
        "representative_player": "Dansby Swanson",
        "player_stats": "2022: 25 HR, .277 AVG, 96 RBI"
    }
]

df = pd.DataFrame(teams)

# Streamlit 화면 구성
st.title("🏟️ 미국 메이저리그 팀 지도")
st.markdown("MLB 팀의 위치를 확인하고, 각 팀 대표 선수의 전적을 살펴보세요.")

# pydeck 지도 시각화
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=50000,
    get_fill_color=[200, 30, 0, 160],
    pickable=True
)

tooltip = {
    "html": """
    <b>{team}</b><br/>
    🏙️ {city}<br/>
    ⭐ 대표 선수: {representative_player}<br/>
    📊 전적: {player_stats}
    """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

view_state = pdk.ViewState(
    latitude=39.8283,
    longitude=-98.5795,
    zoom=3.5,
    pitch=0
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )
)
