from datetime import date, timedelta, datetime
import requests
import json

def writeData():
    today = date.today()
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday_today = today.weekday()  # 월요일 0 일요일 6
    file_weekday = ["mon", "tue", "wed", "thu", "fri"]

    date_url = "https://www.daelim.ac.kr/ajaxf/FrBistroSvc/BistroDateInfo.do"

    current_week_monday = requests.get(date_url).json()["data"][0]["CURRENT_WEEK_MON_DAY"]
    current_week_friday = requests.get(date_url).json()["data"][0]["CURRENT_WEEK_FRI_DAY"]

    student_url = f"https://www.daelim.ac.kr/ajaxf/FrBistroSvc/BistroCarteInfo.do?pageNo=1&MENU_ID=1470&BISTRO_SEQ=1&START_DAY={current_week_monday}&END_DAY={current_week_friday}"
    student_menu = requests.get(student_url).json()["data"]

    def output(title, msg):
        return {
            "version": "1.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "date": ''.join(title),
                            "text": ''.join(msg)
                        }
                    }
                ]
            }
        }

    for i in range(1, 8):  # 1에서 7까지
        day = datetime.strptime(current_week_monday, '%Y.%m.%d') + timedelta(days=(i - 1))

        student_message = []
        student_title = []
        student_title.append(f"[{day.year}년 {day.month}월 {day.day}일 {days[i - 1]}]\n")

        if student_menu == "" or i > 5:
            student_message.append("메뉴가 없습니다.\n\n")
        else:
            blank = 0
            for j in range(1, 10):  # 1에서 9까지
                if (student_menu[f"CCT{i}{j}"] != "") and (student_menu[f"CCT{i}{j}"] is not None):
                    student_message.append("[{}]\n".format(student_menu[f"CNM1{j}"]))
                    student_message.append("{}".format(student_menu[f"CCT{i}{j}"]).replace("\r", "").rstrip("\n") + "\n\n")
                else:
                    blank = blank + 1

            if blank >= 9:
                student_message.append("메뉴가 없습니다.\n\n")

        if i < 6:
            with open(f"./out/student/m_student_{file_weekday[i - 1]}.json", 'w', encoding='utf-8') as outfile:
                json.dump(output(student_title, student_message), outfile, ensure_ascii=False)
        if (i - 1) == weekday_today:
            with open(f"./out/student/m_student_today.json", 'w', encoding='utf-8') as outfile:
                json.dump(output(student_title, student_message), outfile, ensure_ascii=False)