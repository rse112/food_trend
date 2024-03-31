import requests
import pandas as pd

# API 키 및 URL 설정
api_key = "AIzaSyDGo7v_t8bl1GZKU0MuX6UMsVJVSAeHgMk"  # 여기에 실제 API 키 입력
query = "restaurants in Gwangjin-gu Seoul"
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

# API 요청
response = requests.get(url)
restaurants = response.json()

# 음식점 데이터를 DataFrame으로 변환
restaurants_df = pd.DataFrame(
    {
        "Name": [restaurant["name"] for restaurant in restaurants["results"]],
        "Address": [
            restaurant.get("formatted_address", "No address provided")
            for restaurant in restaurants["results"]
        ],
        "Types": [
            ", ".join(restaurant["types"])  # 'types' 필드의 배열을 문자열로 변환
            for restaurant in restaurants["results"]
        ],
        "Latitude": [
            restaurant["geometry"]["location"]["lat"]
            for restaurant in restaurants["results"]
        ],
        "Longitude": [
            restaurant["geometry"]["location"]["lng"]
            for restaurant in restaurants["results"]
        ],
    }
)

# CSV 파일로 저장
restaurants_df.to_csv("restaurants_in_gwangjin_gu_seoul.csv", index=False)
print("CSV 파일이 저장되었습니다.")
