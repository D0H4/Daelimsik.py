import json

from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

option = Options()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome("./webdriver/chromedriver", chrome_options=option)
driver.get('https://www.daelim.ac.kr/cms/FrCon/index.do?MENU_ID=460')
sleep(3)
bus = driver.page_source
driver.quit()  # 웹드라이버 종료

soup = BeautifulSoup(bus, 'html.parser')


def output(msg, quickreplies):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": ''.join(msg)
                    }
                }
            ],
            "quickReplies": quickreplies
        }
    }


def quickreply(label, blockid):
    return {
        "action": "block",
        "messageText": label,
        "label": label,
        "blockId": blockid
    }


def station_to_school(loc, message):
    for tr in loc:
        if ((tr.select_one('td:nth-child(1)').get_text()) in ["휴게시간", "", " ", "&nbsp;", " "]):
            pass
        elif (((tr.select_one('td:nth-child(1)').get_text())[1].isdigit() == False) and (
                (tr.select_one('td:nth-child(2)').get_text() in ["", " ", "&nbsp;", " "]))):
            pass
        elif (tr.select_one('td:nth-child(1)').get_text())[1].isdigit() == True:
            if (tr.select_one('td:nth-child(1)').get_text() in ["", " ", "&nbsp;", " "]):
                pass
            else:
                message.append("- ")
                message.append(tr.select_one('td:nth-child(1)').get_text() + " ")
                if (tr.select_one('td:nth-child(3)').get_text() in ["해당시간", "", " ", "&nbsp;", " "]):
                    message.append("\n")
                else:
                    message.append(
                        "(배차간격: {})\n".format(tr.select_one('td:nth-child(3)').get_text()))
        elif (tr.select_one('td:nth-child(1)').get_text())[1].isdigit() == False:
            if (tr.select_one('td:nth-child(2)').get_text() in ["", " ", "&nbsp;", " "]):
                pass
            else:
                message.append("- ")
                message.append(tr.select_one('td:nth-child(2)').get_text() + " ")
                if (tr.select_one('td:nth-child(4)').get_text() in ["해당시간", "", " ", "&nbsp;", " "]):
                    message.append("\n")
                else:
                    message.append(
                        "(배차간격: {})\n".format(tr.select_one('td:nth-child(4)').get_text()))


def school_to_station(loc, message):
    for tr in loc:
        if ((tr.select_one('td:nth-child(1)').get_text()) == "휴게시간") or (
                tr.select_one('td:nth-child(1)[colspan]')):
            pass
        elif (tr.select_one('td:nth-child(1)').get_text() in ["", " ", "&nbsp;", " "]) or (
                (tr.select_one('td:nth-child(1)').get_text())[1].isdigit() == True):
            if (tr.select_one('td:nth-child(2)').get_text() in ["", " ", "&nbsp;", " "]):
                pass
            else:
                message.append("- ")
                message.append(tr.select_one('td:nth-child(2)').get_text() + " ")
                if (tr.select_one('td:nth-child(3)').get_text() in ["해당시간", "", " ", "&nbsp;", " "]):
                    message.append("\n")
                else:
                    message.append(
                        "(배차간격: {})\n".format(tr.select_one('td:nth-child(3)').get_text()))
        elif (tr.select_one('td:nth-child(1)').get_text())[1].isdigit() == False:
            if (tr.select_one('td:nth-child(3)').get_text() in ["", " ", "&nbsp;", " "]):
                pass
            else:
                message.append("- ")
                message.append(tr.select_one('td:nth-child(3)').get_text() + " ")
                if (tr.select_one('td:nth-child(4)').get_text() in ["해당시간", "", " ", "&nbsp;", " "]):
                    message.append("\n")
                else:
                    message.append(
                        "(배차간격: {})\n".format(tr.select_one('td:nth-child(4)').get_text()))


######################################### 안양역 #########################################

anyang_tr = soup.select_one('.lineTop_tbArea > table > tbody').select('tr')

### 안양역에서 학교 ###

anyang_to_school = []

anyang_to_school.append("[대림식 알림]\n")
anyang_to_school.append("\n")
anyang_to_school.append("안양역에서 학교로 이동하는 셔틀버스 안내입니다.\n")
anyang_to_school.append("\n")

station_to_school(anyang_tr, anyang_to_school)

anyang_to_school.append("\n※ 교통 혼잡 및 신호대기로 인해 운행시간이 변동될 수 있습니다.")

with open("./out/schoolbus/m_anyang_to_school.json", 'w') as outfile:
    json.dump(output(anyang_to_school, [quickreply("🚌 전체 셔틀버스 배차시간", "633e69ddca1fd2777db9a2a8"), quickreply("🚏 안양역 정류장", "64eb29d7e4f55f6afe21492f")]), outfile,
              ensure_ascii=False)

### 학교에서 안양역 ###

school_to_anyang = []

school_to_anyang.append("[대림식 알림]\n")
school_to_anyang.append("\n")
school_to_anyang.append("학교에서 안양역으로 이동하는 셔틀버스 안내입니다.\n")
school_to_anyang.append("\n")

school_to_station(anyang_tr, school_to_anyang)

school_to_anyang.append("\n※ 교통 혼잡 및 신호대기로 인해 운행시간이 변동될 수 있습니다.")

with open("./out/schoolbus/m_school_to_anyang.json", 'w') as outfile:
    json.dump(output(school_to_anyang, [quickreply("🚌 전체 셔틀버스 배차시간", "633e69ddca1fd2777db9a2a8"), quickreply("🚏 안양역 정류장", "64eb29d7e4f55f6afe21492f")]), outfile,
              ensure_ascii=False)

######################################### 범계역 #########################################

beomgye_tr = soup.select_one('.mT30 > table > tbody').select('tr')

### 범계역에서 학교 ###

beomgye_to_school = []

beomgye_to_school.append("[대림식 알림]\n")
beomgye_to_school.append("\n")
beomgye_to_school.append("범계역에서 학교로 이동하는 셔틀버스 안내입니다.\n")
beomgye_to_school.append("\n")

station_to_school(beomgye_tr, beomgye_to_school)

beomgye_to_school.append("\n※ 교통 혼잡 및 신호대기로 인해 운행시간이 변동될 수 있습니다.")

with open("./out/schoolbus/m_beomgye_to_school.json", 'w') as outfile:
    json.dump(output(beomgye_to_school, [quickreply("🚌 전체 셔틀버스 배차시간", "633e69ddca1fd2777db9a2a8"), quickreply("🚏 범계역 정류장", "64eb29e9e4f55f6afe214935")]), outfile,
              ensure_ascii=False)

### 학교에서 범계역 ###

school_to_beomgye = []

school_to_beomgye.append("[대림식 알림]\n")
school_to_beomgye.append("\n")
school_to_beomgye.append("학교에서 범계역으로 이동하는 셔틀버스 안내입니다.\n")
school_to_beomgye.append("\n")

school_to_station(beomgye_tr, school_to_beomgye)

school_to_beomgye.append("\n※ 교통 혼잡 및 신호대기로 인해 운행시간이 변동될 수 있습니다.")

with open("./out/schoolbus/m_school_to_beomgye.json", 'w') as outfile:
    json.dump(output(school_to_beomgye, [quickreply("🚌 전체 셔틀버스 배차시간", "633e69ddca1fd2777db9a2a8"), quickreply("🚏 범계역 정류장", "64eb29e9e4f55f6afe214935")]), outfile,
              ensure_ascii=False)


######################################### 정류장 #########################################

def helpoutput(info, alttext):
    if info:
        text = ""
        if info.find('ul').find("li"):
            location = info.find('ul').find("li")
            if location.find("b"):
                location.find("b").decompose()
            if location.find(string=lambda text: isinstance(text, Comment)):
                location.find(string=lambda text: isinstance(text, Comment)).extract()
            text = location.get_text().replace("\n", "").rstrip()
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleImage": {
                            "imageUrl": f"https://www.daelim.ac.kr{info.find('img').get('src')}",
                            "altText": alttext
                        }
                    },
                    {
                        "simpleText": {
                            "text": text
                        }
                    }
                ],
            }
        }


anyang_info = soup.select_one('.comewayDiv')
beomgye_info = soup.select_one('.mT70')

with open("./out/schoolbus/m_help_anyang.json", 'w') as outfile:
    json.dump(helpoutput(anyang_info, "안양역 정류장"), outfile, ensure_ascii=False)
with open("./out/schoolbus/m_help_beomgye.json", 'w') as outfile:
    json.dump(helpoutput(beomgye_info, "범계역 정류장"), outfile, ensure_ascii=False)
