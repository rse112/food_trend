import requests
import pandas as pd
import time
from models.utils import get_secret

# API 키 및 URL 설정
api_key = get_secret("google_api_key")  # 여기에 실제 API 키 입력

query = "restaurants in Gwangjin-gu Seoul"
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

restaurants = []  # 모든 결과를 저장할 리스트

while True:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"요청 실패: 상태 코드 {response.status_code}")
        break  # 상태 코드가 200이 아니면 루프 중단

    json_response = response.json()
    
    # API 응답의 상태 필드 확인
    if json_response["status"] != "OK":
        print(f"API 요청 실패: {json_response.get('error_message', '알 수 없는 오류')}")
        break  # API 상태가 'OK'가 아니면 루프 중단

    # 현재 페이지의 결과를 리스트에 추가
    restaurants.extend(json_response["results"])
    
    # next_page_token이 있으면, 다음 페이지 요청을 준비
    page_token = json_response.get("next_page_token")
    if page_token:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={page_token}&key={api_key}"
        
        # Google 문서에 따르면, 다음 페이지의 결과가 준비되기까지 몇 초의 지연이 필요할 수 있음
        time.sleep(2)  # 2초 대기
    else:
        break  # 더 이상 페이지가 없으면 루프 종료

if restaurants:
    # 음식점 데이터를 DataFrame으로 변환
    restaurants_df = pd.DataFrame(
        {
            "Name": [restaurant["name"] for restaurant in restaurants],
            "Address": [restaurant.get("formatted_address", "No address provided") for restaurant in restaurants],
            "Types": [", ".join(restaurant["types"]) for restaurant in restaurants],
            "Latitude": [restaurant["geometry"]["location"]["lat"] for restaurant in restaurants],
            "Longitude": [restaurant["geometry"]["location"]["lng"] for restaurant in restaurants],
        }
    )

    # CSV 파일로 저장
    restaurants_df.to_csv("restaurants_in_gwangjin_gu_seoul_extended.csv", index=False)
    print("확장된 CSV 파일이 저장되었습니다.")
else:
    print("API로부터 음식점 데이터를 수집하지 못했습니다.")
