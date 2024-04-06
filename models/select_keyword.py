from pytz import timezone
# from dtw import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from datetime import datetime
from models.trend import trend_maincode
from models.utils import get_secret
import asyncio
import time


def select_keyword(table, today, mode):

    result_tmp, result_tmp_gph, table_graph = prepare_data(table, today, mode)
    # prepare_data 함수의 반환 값 중 None이 있는지 확인
    if result_tmp is None or result_tmp_gph is None or table_graph is None:

        return None, None, None

    # 데이터프레임의 행 수 확인

    try:

        # 검색량 기준
        last = result_tmp.iloc[-1, 0]  # 가장 최근 일자 상대적 검색량
        last_2 = result_tmp.iloc[-2, 0]  # 바로 그 전 일자 상대적 검색량

        # 분산 기준
        var = np.var(result_tmp.iloc[:, 0])

        # 조건 적용 및 분류 로직
        return check_surge_conditions(
            last, last_2, var, result_tmp, result_tmp_gph, table_graph, mode=mode
        )
    except Exception as e:
        # 데이터 처리 중 발생한 예외를 처리
        print(f"An error occurred during keyword selection: {e}")
        return None, None, None


# 주어진 모드에 따라 데이터를 준비하고 전처리하는 함수.
def prepare_data(table, today, mode, days=None, year=None, years=None):
    """
    주어진 모드에 따라 데이터를 준비하고 전처리하는 함수.

    Parameters:
    - table: DataFrame, 분석 대상 데이터
    - today: datetime, 현재 날짜
    - mode: str, 분석 모드 ('daily')

    Returns:
    - result_tmp: DataFrame, 처리된 데이터
    - result_tmp_gph: DataFrame, 그래프용 처리된 데이터
    - error: str, 에러 메시지 (있을 경우)
    """

    days = 1
    year = 1
    years = 1
    period = [1, 1]
    Gap = 1

    ##############################################
    end_time, table_tmp, table_graph = set_analysis_period(
        table, today, days=days, year=year, yearss=years, mode=mode
    )

    if end_time is None or table_tmp is None or table_graph is None:

        return None, None, None

    else:

        result_tmp, result_tmp_gph = preprocess_data(
            end_time,
            table_tmp,
            table_graph,
            mode=mode,
            period=period,
            Gap=Gap,
        )

        return result_tmp, result_tmp_gph, table_graph


# 주어진 날짜와 기간을 바탕으로 데이터 분석 기간을 설정하고, 해당 기간의 데이터를 필터링하여 반환함.
def set_analysis_period(table, today, days=0, year=0, yearss=0, mode="daily"):
    try:

        std_time = datetime.strptime(today, "%y%m%d")
        day = relativedelta(days=days)
        years_delta = relativedelta(years=yearss)  # 3
        year_delta = relativedelta(years=year)  # 2
        # 날짜 계산
        end_time = std_time - day
        start_time = std_time - year_delta - day  # start_time = 지금-2년
        start_before = std_time - years_delta - day
        end_time_str = end_time.strftime("%Y-%m-%d")
        start_time_str = start_time.strftime("%Y-%m-%d")
        start_before_str = start_before.strftime("%Y-%m-%d")

        # 분석 기간 설정
        table.index = pd.to_datetime(table.index)

        table_tmp = table[
            (table.index >= start_time_str) & (table.index <= end_time_str)
        ]
        table_graph = table[
            (table.index >= start_before_str) & (table.index <= end_time_str)
        ]

        # 데이터가 충분한지 확인
        dateLimit = 200

        if len(table_tmp) < dateLimit:
            return None, None, None
        return end_time_str, table_tmp, table_graph

    except Exception as e:

        print(f"An error occurred in set_analysis_period: {e}")

        return None, None, None


# 데이터 전처리 및 분석 기간 설정을 위한 함수.
def preprocess_data(end_time, table_tmp, table_graph, mode, period, Gap):
    # 일별 데이터는 이미 최적화된 상태이므로 추가 처리 없이 반환
    result_tmp = table_tmp / table_tmp.max() * 100
    result_tmp_gph = table_graph / table_graph.max() * 100
    return result_tmp, result_tmp_gph


# 급상승 키워드 조건을 평가하고, 해당하는 경우 데이터와 상승률을 반환함.
def check_surge_conditions(
    last, last_2, var, result_tmp, result_tmp_gph, table_graph, mode
):
    """
    급상승 조건을 확인하고 결과를 반환하는 함수.
    round((last - last_2)/last_2 * 100,2) : 지표(추세성, 상승률)
    """
    vars = 200
    period_str = "일별"
    last_Boundary = 85

    rate = round((last - last_2) / last_2 * 100, 2)

    # 그림용 테이블 생성
    result_graph = create_result_graph(
        result_tmp, result_tmp_gph, formatted_today, mode
    )

    if var > vars:

        return None, None, None

    if (last > last_2 * 2.0) & (last >= 60):
        print(f"{period_str} 급상승 키워드 발견: {table_graph.columns[0]}")

        return result_graph, result_graph, rate

    elif (last >= 95) & (last > last_2):
        print(f"{period_str} 급상승 키워드 발견: {table_graph.columns[0]}")
        return result_graph, result_graph, rate
    elif (
        (last_2 * 2.0 > 100)
        & (last >= last_Boundary)
        & (last > last_2)
        & ((last - last_2) > 5)
    ):
        print(f"{period_str} 급상승 키워드 발견: {table_graph.columns[0]}")

        return result_graph, result_graph, rate
    else:
        return None, None, None


def create_result_graph(result_tmp, result_tmp_gph, today, mode):
    """
    검색 결과와 관련 데이터를 바탕으로 결과 데이터 프레임을 생성하는 함수.

    Parameters:
    - result_tmp: 원본 검색 결과 데이터 프레임.
    - result_tmp_gph: 그래프용 검색 결과 데이터 프레임.
    - formatted_today: 기준일자 문자열.
    - mode: 검색 유형 문자열.

    Returns:
    - result_graph: 생성된 결과 데이터 프레임.
    """
    mode_str = "일별"
    result_graph = pd.DataFrame()
    result_graph["검색일자"] = result_tmp_gph.index
    result_graph["기준일자"] = formatted_today
    result_graph["유형"] = f"{mode_str}급상승"
    result_graph["연관검색어"] = result_tmp_gph.columns[0]
    result_graph["검색량"] = result_tmp_gph.values
    result_graph = result_graph[
        ["기준일자", "유형", "연관검색어", "검색일자", "검색량"]
    ]
    return result_graph


def get_today_date():
    today = datetime.now(timezone("Asia/Seoul"))
    formatted_today = today.strftime("%Y-%m-%d")
    day = today.strftime("%y%m%d")
    return formatted_today, day


formatted_today, day = get_today_date()

if __name__ == "__main__":
    # 검색 기준일
    standard_time = datetime.now()
    params = {
        "search_keywords": [
            "율식당",
            "꿀곱창",
            "IKH몽골식당",
            "범일동맛집",
        ],
        "id": get_secret("clients")["id_1"]["client_id"],
        "pw": get_secret("clients")["id_1"]["client_secret"],
        "api_url": "https://openapi.naver.com/v1/datalab/search",
        "name": "name",
    }

    # api 아이디비번 가져오기
    tasks = []
    # API 요청 URL
    api_url = "https://openapi.naver.com/v1/datalab/search"
    start = time.time()
    clients = get_secret("clients")
    results = asyncio.run(trend_maincode(params, clients, api_url))

    kk = "daily"

    for df in results:
        print(df)
        a, b, c = select_keyword(df, day, kk)
        print(a, b, c)

    print(time.time() - start)
