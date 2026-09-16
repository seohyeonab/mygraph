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

    # 숫자형 데이터로 변환
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

movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


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

st.header("그래프 2. 일관객 합계 TOP 5 영화")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 일관객 변화를 비교합니다."
)


# 영화별 전체 기간 일관객 합계
movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)

# 합계가 가장 큰 5편
top5_movies = movie_total.head(5)["영화명"].tolist()

# TOP 5 영화 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y년 %m월 %d일}<br>"
        "일관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    hovermode="x"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성하세요.",
    placeholder="여기에 이 그래프로 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph2_explanation"
)


# =========================================================
# 그래프 3
# 날짜별 10위권 전체 일관객 합계
# =========================================================

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 합산하여 보여 줍니다."
)


# ---------------------------------------------------------
# 1. 날짜별 일관객 합계 계산
# ---------------------------------------------------------

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


# ---------------------------------------------------------
# 2. 일관객 합계가 가장 큰 날짜 3개 찾기
# ---------------------------------------------------------

top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)


# ---------------------------------------------------------
# 3. 영역 그래프 만들기
# ---------------------------------------------------------

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


# ---------------------------------------------------------
# 4. 마우스를 올렸을 때 정보 표시
# ---------------------------------------------------------

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y년 %m월 %d일}<br>"
        "10위권 일관객 합계: %{y:,.0f}명"
        "<extra></extra>"
    )
)


# ---------------------------------------------------------
# 5. 가장 큰 날 3일을 그래프 위에 표시
# ---------------------------------------------------------

for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y년 %m월 %d일')}"
            f"<br>{row['일관객']:,.0f}명"
        ),
        showarrow=True,
        arrowhead=2,
        yshift=15
    )


# ---------------------------------------------------------
# 6. 그래프 모양 설정
# ---------------------------------------------------------

fig3.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)


# 그래프 출력
st.plotly_chart(
    fig3,
    use_container_width=True
)


# =========================================================
# 그래프 3 설명 작성 공간
# =========================================================

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성하세요.",
    placeholder="여기에 이 그래프로 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph3_explanation"
)


# =========================================================
# 그래프 4
# =========================================================

st.header("그래프 4")

st.write(
    "앞으로 추가할 네 번째 그래프 영역입니다."
)

st.info(
    "여기에 네 번째 그래프를 추가할 예정입니다."
)
