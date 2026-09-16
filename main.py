import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("영화 데이터를 시간의 흐름에 따라 살펴보는 그래프입니다.")


# =========================================================
# 데이터 불러오기
# =========================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_URL,
        encoding="utf-8-sig"
    )

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형으로 변환
    number_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in number_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# =========================================================
# 그래프 1
# =========================================================

st.header("그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 선택하면 그 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)


# 영화 선택
movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# 선 그래프
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)


# 마우스를 올렸을 때 표시
fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y년 %m월 %d일}<br>"
        "관객수: %{y:,.0f}명"
        "<extra></extra>"
    )
)


fig1.update_layout(
    height=500,
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================================================
# 그래프 1 설명 작성 공간
# =========================================================

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성하세요.",
    placeholder="여기에 이 그래프로 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph1_explanation"
)


# =========================================================
# 그래프 2
# =========================================================

st.header("그래프 2")

st.write(
    "앞으로 추가할 두 번째 그래프 영역입니다."
)

st.info("여기에 두 번째 그래프를 추가할 예정입니다.")


# =========================================================
# 그래프 3
# =========================================================

st.header("그래프 3")

st.write(
    "앞으로 추가할 세 번째 그래프 영역입니다."
)

st.info("여기에 세 번째 그래프를 추가할 예정입니다.")


# =========================================================
# 그래프 4
# =========================================================

st.header("그래프 4")

st.write(
    "앞으로 추가할 네 번째 그래프 영역입니다."
)

st.info("여기에 네 번째 그래프를 추가할 예정입니다.")
