import requests
import json
from datetime import date, datetime

today = date.today()
days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
weekday_number = today.weekday() # 월요일 0 일요일 6

m_weather = open("./out/weather/m_weather.json", 'w')

m_weather.write('{"version": "2.0","template": {"outputs": [{"simpleText": {"text": "')
m_weather.write("[대림식 알림]\\n")
m_weather.write("\\n")
m_weather.write("대림대학교 날씨를 알려드릴게요.\\n")
m_weather.write("\\n")

API_key = ""
lat = "37.40397108077262"
lon = "126.93068557182605"

openweathermap = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric".format(lat, lon, API_key))
if(openweathermap.status_code != 200):
    m_weather.write("날씨 정보를 불러오는 중 실패하였습니다: {}", openweathermap.status_code)
else:
    m_weather.write("{}년 {}월 {}일 {}시 기준\\n".format(today.year, today.month, today.day, str(datetime.now().hour).zfill(2)))
    m_weather.write("3시간 뒤에는...\\n")
    weather_json = json.loads(openweathermap.text)

    weather_main = weather_json["list"][1]["weather"][0]["main"]
    weather_temp = weather_json["list"][1]["main"]["temp"]
    weather_temp_feels_like = weather_json["list"][1]["main"]["feels_like"]
    weather_temp_min = weather_json["list"][1]["main"]["temp_min"]
    weather_temp_max = weather_json["list"][1]["main"]["temp_max"]
    weather_humidity = weather_json["list"][1]["main"]["humidity"]
    weather_pop = weather_json["list"][1]["pop"]

    # 뇌우
    if(weather_main == "Thunderstorm"):
        m_weather.write("뇌우가 칠 예정이에요!\\n")
        m_weather.write("외출 시 우산 잊지 마시고, 아끼는 옷과 신발은 자제해주세요!\\n")
    # 맑음
    elif(weather_main == "Clear"):
        m_weather.write("맑은 날씨가 예정되어있어요!\\n")
        m_weather.write("날씨가 좋다고 자체휴강은 학점에 안 좋아요!\\n")
    # 비
    elif(weather_main == "Rain"):
        m_weather.write("비가 내릴 예정이에요!\\n")
        m_weather.write("외출 시 우산 잊지 마세요!\\n")
    # 흐림
    elif(weather_main == "Clouds"):
        m_weather.write("흐린 날씨가 예정되어있어요!\\n")
    # 눈
    elif(weather_main == "Snow"):
        m_weather.write("눈이 내릴 예정이에요!\\n")
        m_weather.write("빙판길 조심하세요!\\n")
    # 이슬비
    elif(weather_main == "Drizzle"):
        m_weather.write("이슬비가 내릴 예정이에요!\\n")
    # 안개
    elif(weather_main == "Mist" or "Haze" or "Fog"):
        m_weather.write("안개가 낄 예정이에요!\\n")
        m_weather.write("특히 운전하시는 분들은 안전에 유의하세요!\\n")
    # 황사
    elif(weather_main == "Dust" or "Sand"):
        m_weather.write("황사가 낄 예정이에요!\\n")
        m_weather.write("황사마스크 혹은 미세먼지 마스크 잊지마세요!\\n")
    # 스모크
    elif(weather_main == "Smoke"):
        m_weather.write("연기(스모크)로 자욱할 예정이에요!\\n")
        m_weather.write("안전에 유의하세요!\\n")
    # 화산재
    elif(weather_main == "Ash"):
        m_weather.write("화산재로 자욱할 예정이에요!\\n")
        m_weather.write("안전에 유의하세요!\\n")
    # 돌풍
    elif(weather_main == "Squall"):
        m_weather.write("돌풍이 불 예정이에요!\\n")
        m_weather.write("날아가지 않도록 유의하세요!\\n")
    # 토네이도 혹은 태풍
    elif(weather_main == "Tornado"):
        m_weather.write("태풍이 올 예정이에요!\\n")
        m_weather.write("강의 후 되도록이면 실내에 피신하세요!\\n")
    # ???
    else:
        m_weather.write("알 수 없는 이유로 인해 날씨를 못 불러왔어요...\\n")

m_weather.write("\\n")
m_weather.write("기온: {}°C\\n".format(int(weather_temp)))
m_weather.write("습도: {}%\\n".format(int(weather_humidity)))
m_weather.write("체감 온도: {}°C\\n".format(int(weather_temp_feels_like)))
m_weather.write("\\n")
m_weather.write("최저 기온: {}°C\\n".format(int(weather_temp_min)))
m_weather.write("최고 기온: {}°C\\n".format(int(weather_temp_max)))
m_weather.write("강수 확률: {}%".format(int(weather_pop * 100)))

if(weather_main == "Thunderstorm" or weather_main == "Rain"):
    m_weather.write("\\n")
    m_weather.write("\\n")
    weather_rain = weather_json["list"][1]["rain"]["3h"]
    m_weather.write("강수량: {}mm".format(round(weather_rain)))
elif(weather_main == "Snow"):
    m_weather.write("\\n")
    m_weather.write("\\n")
    weather_snow = weather_json["list"][1]["snow"]["3h"]
    m_weather.write("강설량: {}mm".format(round(weather_snow)))
elif(weather_main == "Squall" or weather_main == "Tornado"):
    m_weather.write("\\n")
    m_weather.write("\\n")
    weather_wind = weather_json["list"][1]["wind"]["speed"]
    m_weather.write("풍속: {}m/sec".format(round(weather_wind)))

if(int(weather_temp_feels_like) >= 35):
    m_weather.write("\\n")
    m_weather.write("\\n")
    m_weather.write("체감 온도가 35도 이상이에요!\\n")
    m_weather.write("건강의 유의하여 주시고, 수분 보충을 꾸준히 해주세요!")
elif(int(weather_temp_feels_like) <= -18):
    m_weather.write("\\n")
    m_weather.write("\\n")
    m_weather.write("체감 온도가 -18도 이하에요!\\n")
    m_weather.write("감기와 동상의 유의하고, 체온에 신경써주세요!")

m_weather.write('"}}]}}')
m_weather.close()