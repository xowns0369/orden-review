from flask import Flask, render_template, abort, request, redirect, url_for, send_from_directory
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISIT_FILE = "visits.json"

# -------------------------------
# 방문자 수 관련 함수
# -------------------------------
def get_today_date():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

def load_visits():
    if os.path.exists(VISIT_FILE):
        with open(VISIT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                today = get_today_date()
                if data.get("date") != today:
                    return {"count": 0, "date": today}
                return data
            except json.JSONDecodeError:
                return {"count": 0, "date": get_today_date()}
    return {"count": 0, "date": get_today_date()}

def save_visits(data):
    with open(VISIT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@app.before_request
def count_visit():
    data = load_visits()
    data["count"] = data.get("count", 0) + 1
    data["date"] = data.get("date", get_today_date())
    save_visits(data)

def get_visit_count():
    return load_visits().get("count", 0)


# -------------------------------
# 병원 데이터
# -------------------------------
hospitals = [
    #{"name": "","category":"","gu":"", "region": "", "address": "", "keywords": ["",""], "rating": 0,"website": ""},
    # 검단구 정형외과
    {"name": "온누리병원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 완정로 192 베스트프라자3층", "keywords": ["종합병원","응급실",'척추센터','인공관절센터',"수술","입원실","물리치료", "도수치료"], "rating": 0,"website": "https://www.onnurihosp.com/"},
    {"name": "검단바로본365의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로178길", "keywords": ["도수치료","주말진료",'통증클리닉','자율신경클리닉','영양수액'], "rating": 0,"website": "https://kbrb365.co.kr/"},
    {"name": "착한마디병원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 180", "keywords": ["수술", "입원실",'관절센터','척추센터','재활센터','도수치료','물리치료'], "rating": 0,"website": "http://goodmadi.co.kr/"},
    {"name": "공감 마취통증의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 172 서주빌딩 3층", "keywords": ["주사치료", "통증클리닉",'물리치료'], "rating": 0,"website": "http://www.xn--439azqz10e1fh.com/"},
    {"name": "윤재활의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 172 4층", "keywords": ["척추통증",'관절통증',"재활운동", "도수교정"], "rating": 0,"website": "https://yoonpmrclinic-mo.imweb.me/"},
    {"name": "정정형외과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 왕길동 638-4", "keywords": ["물리치료", "도수치료"], "rating": 0,"website": ""},
    {"name": "위풍당당정형외과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 검단로 480 3층", "keywords": ["척추클리닉",'관절클리닉',"주사치료", "도수교정"], "rating": 0,"website": "http://xn--ok1ba505m9xm.com/"},
    {"name": "미래안마취통증의학과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 검단로 469 선명타운 3층", "keywords": ["척추통증클리닉", "관절통증클리닉"], "rating": 0,"website": ""},
    {"name": "이정형외과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 35", "keywords": ["물리치료", "통증클리닉"], "rating": 0,"website": ""},
    {"name": "오케이마취통증의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 원당대로", "keywords": ["척추클리닉","관절클리닉","도수치료클리닉"], "rating": 0,"website": "http://okane.whost.co.kr/"},
    {"name": "검단연합의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 660", "keywords": ["도수치료", "통증클리닉"], "rating": 0,"website": ""},
    {"name": "바로튼튼정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 서곶로 837 3~4층", "keywords": ["영양수액","도수치료", "물리치료"], "rating": 0,"website": "https://barotuntun.medisay.co.kr/"},
    {"name": "검단탑병원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 청마로19번길 5", "keywords": ["종합병원","응급실", "관절센터","척추센터", "입원실", "수술"], "rating": 0,"website": "https://tophospital.co.kr/main/main.html?"},
    {"name": "원재활의학과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 850 3층", "keywords": ["통증클리닉", "재활클리닉","영양수액","재활필라테스"], "rating": 0,"website": "http://xn--vb0bu30cxlazkq79cmnb.com/"},
    {"name": "골드정형외과의원","category":"정형외과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 221 엠파이어빌딩 701~705호", "keywords": ["디스크","오십견","관절염"], "rating": 0,"website": ""},
    {"name": "하늘본튼튼의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 856 3층", "keywords": ["척추클리닉","관절클리닉","주사치료"], "rating": 0,"website": "http://xn--wh1bu0rv9ra054a.com/#section8"},
    {"name": "원당연세정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 866 5층, 6층", "keywords": ["통증클리닉","재활클리닉"], "rating": 0,"website": "http://coconutz.kr/13388"},
    {"name": "검단본정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 3로 112 4층", "keywords": ["통증클리닉", "시술클리닉","도수치료"], "rating": 0,"website": "https://www.xn--c79a6ix0no4lp2l1kc262b.com/"},
    {"name": "검단바른정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 서로3로 104 2층", "keywords": ["일요일진료","디스크클리닉", "관절클리닉","힘줄재생클리닉","주사클리닉","도수치료"], "rating": 0,"website": "http://gdbareunos.com/"},
    {"name": "검단EM365의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음5로 30 2층,3층", "keywords": ["365일","통증치료","도수치료","물리치료"], "rating": 0,"website": "https://www.gdem365.com/"},
    {"name": "검단정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 7층", "keywords": ["척추관절클리닉","재활클리닉"], "rating": 0,"website": "http://geomdanos.com/"},
    {"name": "서울정석정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 388 ABM타워 4층", "keywords": ["척추클리닉","통증클리닉","도수치료"], "rating": 0,"website": "https://blog.naver.com/dnrpdyd53444"},
    {"name": "연세마디윌의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 392 메트로시티 6층", "keywords": ["관절클리닉", "통증클리닉"], "rating": 0,"website": "https://www.madiwill.com/"},
    {"name": "검단더굿정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 392 5층", "keywords": ["척추클리닉","관절클리닉","통증클리닉","도수치료"], "rating": 0,"website": "http://thegoodgd.co.kr/index.php"},
    {"name": "검단이화연합의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음5로 80 검단퍼스트 5층", "keywords": ["일요일진료","통증클리닉","도수치료"], "rating": 0,"website": "https://blog.naver.com/gumdanewha"},
    {"name": "365마디팔팔의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음1로 386 6층", "keywords": ["365일진료","척추클리닉","관절클리닉","도수치료"], "rating": 0,"website": "http://365madi88.com/"},
    {"name": "서울바른정형외과의원","category":"정형외과","gu":"검단구","region": "불로동", "address": "인천 서구 검단로 768번길2 2층", "keywords": ["척추클리닉","관절클리닉","수술","입원"], "rating": 0,"website": "http://www.barunseoulos.co.kr/"},
    #검단구 치과
    {"name": "이정우치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 187 마전메디컬센터 5층", "keywords": ["임플란트","차아교정","신경치료"], "rating": 0,"website": ""},
    {"name": "검단가온치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 178번길 1 검단빌딩 2층", "keywords": ["소아진료","틀니클리닉","사랑니클리닉","심미클리닉"], "rating": 0,"website": "https://www.gd-gaondental.com/"},
    {"name": "미소드림치과의원","category":"치과","gu":"검단구", "region": "오류동", "address": "인천 서구 보듬5로 5 오덕프라자 3층 303호", "keywords": ["스케일링","임플란트"], "rating": 0,"website": "https://blog.naver.com/misodreamdental_"},
    {"name": "송앤정치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 단봉로 107 성우프라자 302호", "keywords": ["임플란트","보철치료","충치치료","잇몸치료"], "rating": 0,"website": "https://www.instagram.com/songandjungdentalclinic/#"},
    {"name": "서울현대치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 179 검단메디컬 303호", "keywords": ["임플란트","투명교정"], "rating": 0,"website": "https://www.omydentist.com/"},
    {"name": "검단서울치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 검단로 469 선명타운 2층", "keywords": ["임플란트","서울대출신"], "rating": 0,"website": ""},
    {"name": "우수치과의원검단","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 172 3층", "keywords": ["사랑니","충치치료","치아교정센터"], "rating": 0,"website": "http://www.woo-soo.co.kr/"},
    {"name": "열린치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 170 광성빌딩", "keywords": ["야간진료","충치치료"], "rating": 0,"website": ""},
    {"name": "행복담은샘치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 검단로 480 리치웰프라자 4층", "keywords": ["임플란트","충치치료","신경치료"], "rating": 0,"website": ""},
    {"name": "스마일365치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 485 2,3층", "keywords": ["임플란트","치아교정","심미치료","치아관리","특화치료"], "rating": 0,"website": "http://www.smile365dc.com/"},
    {"name": "보스톤클래식치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 486 2층", "keywords": ["치아교정","보철치료","보존치료","치주치료","소아치료"], "rating": 0,"website": "https://www.bostonclassic.co.kr/"},
    {"name": "김준영치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 160", "keywords": ["스케일링","충치치료"], "rating": 0,"website": ""},
    {"name": "검단어린이치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 153 이레메디칼센타 6층", "keywords": ["소아치과","영유아검진","소아교정"], "rating": 0,"website": "https://blog.naver.com/gumdancdc"},
    {"name": "미추홀치과","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 500", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "미담치과","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 502번길 1", "keywords": ["야간진료","치아검진"], "rating": 0,"website": ""},
    {"name": "나은미소치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 508 이지준프라자 4층", "keywords": ["임플란트","교정치료","틀니"], "rating": 0,"website": "http://naeunmisodental.co.kr/"},
    {"name": "마전미소치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 마전로115번길 2-6 2-1", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "불로치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 764", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "이사랑부부치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 834 퀸스타운 신명아파트 상가", "keywords": ["보철치료","임플란트","소아치료"], "rating": 0,"website": ""},
    {"name": "미래치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 842 월드메가마트 219호", "keywords": ["야간진료","치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "검단일등치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 동화시로 112 JS프라자2 2층", "keywords": ["소아치료","턱관절","신경치료","임플란트"], "rating": 0,"website": "https://xn--c79a6ix0nt9be62bcnj.com/"},
    {"name": "검단브라이트치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 221 엠파이어빌딩 503~507호", "keywords": ["턱관절","사랑니","임플란트","라미네이트"], "rating": 0,"website": "https://blog.naver.com/brightdentclinic"},
    {"name": "타임치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 841 골든벨프라자", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "다정한치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 고산후로 95번길 20 힘찬프라자 4층", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "루브르치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 861 원당프라자 3층", "keywords": ["임플란트","교정치료","사랑니"], "rating": 0,"website": "https://blog.naver.com/lvrdent"},
    {"name": "신동근치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 866 4층 402호", "keywords": ["틀니","임플란트","심미보철"], "rating": 0,"website": ""},
    {"name": "이튼치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 865 대산프라자 3층 304호", "keywords": ["임플란트","소아치료","치주치료","보철치료"], "rating": 0,"website": ""},
    {"name": "바른공감치과의원검단점","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서로3로 104 신화프라자 3층", "keywords": ["소아치료","임플란트","사랑니"], "rating": 0,"website": "http://bagongdental.com/"},
    {"name": "치과로와치과의원검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 발산로 6 아인시티주차타워 306호", "keywords": ["고난이도임플란트","의식하진정치료","턱관절치료","충치치료"], "rating": 0,"website": "https://www.rowadental.com/"},
    {"name": "예온치과병원인천검단365점","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 이음4로 6 KR법조타워 5층", "keywords": ["임플란트","교정치료","소아치료","일요일진료"], "rating": 0,"website": "https://gd365.ye-on.com/"},
    {"name": "이플러스치과의원검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 30 301~303호", "keywords": ["임플란트","사랑니","보철치료"], "rating": 0,"website": "http://eplusdentistry.com/"},
    {"name": "나아라치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 36 더원타워 5층 501~503호", "keywords": ["임플란트","자연치아살리기","심미클리닉"], "rating": 0,"website": "https://xn--vb0bl2ehzhgnpbwk.com/"},
    {"name": "검단센트럴치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 이음대로 479 CS메디컬프라자 2층", "keywords": ["임플란트","사랑니","턱관절"], "rating": 0,"website": "인천 서구 이음대로 479 CS메디컬프라자 2층"},
    {"name": "연세꿈꾸는아이치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 7층", "keywords": ["소아치료","수면치료","성장교정"], "rating": 0,"website": "http://www.ysdreami.com/"},
    {"name": "서울바로치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 3층", "keywords": ["임플란트","교정치료","소아치료"], "rating": 0,"website": "https://svdc.kr/#;"},
    {"name": "서울더블유치과교정과치과의원 검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 384 서영아너시티플러스 2층", "keywords": ["교정치료","임플란트"], "rating": 0,"website": "http://seoulwdent.co.kr/"},
    {"name": "연세검단치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 388 ABM타워 5층 503~509호", "keywords": ["임플란트","치아교정","수면무통마취"], "rating": 0,"website": "https://xn--c79a6ix0ny8qtrf94n.kr/"},
    {"name": "이앤백치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 392 4층", "keywords": ["치아교정","임플란트"], "rating": 0,"website": "https://lnbdental.com/"},
    {"name": "연세앤치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 60 JS프라자 5층", "keywords": ["임플란트","치주치료","소아치료","투명교정"], "rating": 0,"website": "https://ysannedent.qshop.ai/"},
    {"name": "이보다구강악안면외과치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 바리미로 17 4층", "keywords": ["의식하진정법","임플란트","사랑니","턱관절","수술치료"], "rating": 0,"website": "http://www.evodaoms.co.kr/"},
    {"name": "피어나치과교정과치과의원 검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 62 정인프라자 4층", "keywords": ["성장기교정","성인교정","치아미백"], "rating": 0,"website": "https://bloomortho.co.kr/"},
    {"name": "검단퍼스트치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 80 검단퍼스트프라자 3층", "keywords": ["자연치아살리기","임플란트","심미보철","턱관절"], "rating": 0,"website": "https://geomdanfirst.imweb.me/"},
    {"name": "플란치과의원 인천 검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 1045 6층", "keywords": ["임플란트","통증케어"], "rating": 0,"website": "https://geomdan.implan.co.kr/"},
    {"name": "검단뉴욕치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 1045 4층 404호~407호", "keywords": ["구강근기능훈련","소아교정","투명교정","심미보철"], "rating": 0,"website": "http://xn--c79a6ix8linao62fwkk.com/"},
    {"name": "지오웰치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 원당대로 581 롯데마트 검단점 2층", "keywords": ["일요일진료","구강검진","충치치료","임플란트"], "rating": 0,"website": ""},
    {"name": "브라이트치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 70 2층", "keywords": ["심미보철","임플란트","치주치료"], "rating": 0,"website": ""},
    {"name": "파스텔치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 61", "keywords": ["임플란트","사랑니","신경치료"], "rating": 0,"website": "https://blog.naver.com/goodpastel"},
    {"name": "이안치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 60 정안빌딩", "keywords": ["치아검진","스케일링"], "rating": 0,"website": ""},
    {"name": "검단다온치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 54 두영프라자 2층 202호", "keywords": ["소아치료","임플란트","신경치료"], "rating": 0,"website": "https://blog.naver.com/daondc2875"},
    {"name": "노블치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 35 대운프라자", "keywords": ["턱관절","잇몸치료"], "rating": 0,"website": "https://blog.naver.com/omahun2001"},
    {"name": "연세조아치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 36", "keywords": ["임플란트","예방치료","구강건강교육","치아미백","충치치료"], "rating": 0,"website": "https://sites.google.com/view/yonseijoa/"},
    {"name": "참조은박치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 31 동아프라자302호", "keywords": ["임플란트","치아교정","치아성형","치아미백"], "rating": 0,"website": "https://blog.naver.com/tweed2008"},
    {"name": "부치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 18", "keywords": ["임플란트","소아치료","심미치료","치아성형"], "rating": 0,"website": ""},
    {"name": "검단탑병원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로7번길 2 2층", "keywords": ["임플란트","보철치료","스케일링"], "rating": 0,"website": "https://tophospital.co.kr/main/main.html?"},
    {"name": "연세튼튼치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로19번길 20 203호", "keywords": ["임플란트","심미보철","충치치료","사랑니","치주치료"], "rating": 0,"website": "https://blog.naver.com/ysttdc"},
    {"name": "강플란트치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 660 영프라자 10층 1001호", "keywords": ["임플란트","보철치료","치주치료"], "rating": 0,"website": "http://www.kangplant.co.kr/"},
    {"name": "드림라인치과교정과치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 660 영프라자 5층", "keywords": ["성장기교정","성인교정","인비절라인"], "rating": 0,"website": "https://blog.naver.com/dldent"},
    {"name": "연세세브란스치과의원 검단","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 서곶로 866 3층", "keywords": ["수면치료","구강악안면외과","자연치아살리기","임플란트"], "rating": 0,"website": "http://yonsev.com/"},
    {"name": "서울더탑치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 원당대로 663 한종프라자 3층", "keywords": ["임플란트","치아교정","심미치료","소아치료"], "rating": 0,"website": "https://www.seoulthetop.com/"},
    {"name": "당하치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로167번길 8", "keywords": ["임플란트","턱관절","심미보철","치주치료"], "rating": 0,"website": "https://blog.naver.com/dentistjeon"},
    {"name": "위드치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로 171 청석빌딩 3층 1호", "keywords": ["스케일링","소아치료"], "rating": 0,"website": ""},
    {"name": "이앤미치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로 163", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "데일리치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서곶로 788 2층 데일리치과", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "미플러스치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서곶로 754 당하 이마트", "keywords": ["무통치료","임플란트","사랑니"], "rating": 0,"website": ""},
    {"name": "바른수치과의원","category":"치과","gu":"검단구", "region": "백석동", "address": "인천 서구 한들로 74 한들타워1차 4층", "keywords": ["임플란트","치아성형","자연치아살리기","소아교정"], "rating": 0,"website": "http://bareunsu.com/"},
# 서구 정형외과
    {"name": "정우정형외과의원","category":"정형외과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 501", "keywords": ["일요일진료","물리치료"], "rating": 0,"website": ""},
    {"name": "마디튼튼마취통증의학과의원","category":"정형외과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 507 장한프라자 2, 3층 201, 202, 301호", "keywords": ["척추클리닉","관절클리닉","도수치료"], "rating": 0,"website": "http://xn--2z1b52gu10aa.com/"},
    {"name": "인천연세병원","category":"정형외과","gu":"서구", "region": "연희동", "address": "인천 서구 승학로 320", "keywords": ["도수치료","디스크"], "rating": 0,"website": "https://m.icys.kr/"},
    {"name": "서인천현대정형외과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 45 현대메디칼 2층", "keywords": ["척추클리닉","통증클리닉"], "rating": 0,"website": ""},
    {"name": "모두탑365정형외과의원 인천서구점","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 293 우민빌딩 2층, 4층", "keywords": ["일요일진료","물리치료","비수술클리닉"], "rating": 0,"website": "http://modutop-icsg.co.kr/"},
    {"name": "자혜정형외과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 281 자혜정형외과", "keywords": ["척추클리닉","골절수술","물리치료"], "rating": 0,"website": ""},
    {"name": "더본마취통증의학과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 293 5층 502호", "keywords": ["주사치료","척추클리닉","도수치료"], "rating": 0,"website": ""},
    {"name": "서울아산마디척의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 300 401호", "keywords": ["비수술치료","재활운동치료"], "rating": 0,"website": "https://www.asanmadichuk.com/"},
    {"name": "가톨릭관동대학교 국제성모병원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로100번길 25 가톨릭관동대학교 국제성모병원", "keywords": ["대학병원","수술","입원","응급실"], "rating": 0,"website": "https://www.ish.or.kr/main/"},
    {"name": "세로척정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 90 2층 201-204호", "keywords": ["척추클리닉","관절클리닉","소아정형"], "rating": 0,"website": "https://xn--2o2b15nzyj.com/"},
    {"name": "청라이엠365의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로100번길 24 202~205, 301~305호", "keywords": ["주말진료","야간진료","도수치료"], "rating": 0,"website": "https://cnem365.co.kr/ "},
    {"name": "제대로정형외과마취통증의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로 78 4층", "keywords": ["척추클리닉","입원","도수치료","필라테스"], "rating": 0,"website": ""},
    {"name": "청라우리정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로74번길 31 월드프라자 2층", "keywords": ["물리치료","도수치료"], "rating": 0,"website": ""},
    {"name": "진정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 264 403~404호", "keywords": ["비수술치료","혈관영양치료","성장클리닉"], "rating": 0,"website": ""},
    {"name": "드림재활의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588", "keywords": ["도수치료","디스크"], "rating": 0,"website": "http://dreamrm.com/"},
    {"name": "청라코끼리마취통증의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 594 406~408호", "keywords": ["통증클리닉","도수치료"], "rating": 0,"website": "https://kkrpain.co.kr/"},
    {"name": "청라성모정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71 진영메디피아3층", "keywords": ["특수치료","시술치료","비수술치료"], "rating": 0,"website": "http://www.xn--vb0b32rvpcgujb5g1qcdtmsst.com/"},
    {"name": "청라바른정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 65 라임타워 5층", "keywords": ["일요일진료","척추관절센터","성장클리닉","도수치료"], "rating": 0,"website": "http://cheongrabarun.co.kr/default/"},
    {"name": "청라국제병원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로102번길 8 2층, 4층", "keywords": ["365일진료","척추센터","관절센터","통증치료"], "rating": 0,"website": "https://jsjhospital.co.kr:9003/main/main.php"},
    {"name": "가정성모의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 청중로 486 부일프라자 3, 4층", "keywords": ["통증클리닉","교정클리닉","도수치료센터"], "rating": 0,"website": "http://gajeongsm.co.kr/"},
    {"name": "서울정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로 468 드림타워 7층, 801호, 802호", "keywords": ["특수건강검진","척추클리닉","관절클리닉","시술클리닉","도수치료"], "rating": 0,"website": "https://osyang0501.dothome.co.kr/HOME"},
    {"name": "고려재활의학과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로464번길 15 쓰리엠타워 5층", "keywords": ["입원치료","물리치료","연골주사"], "rating": 0,"website": "https://blog.naver.com/korearehab"},
    {"name": "바로서구병원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정동 196-3", "keywords": ["양방향척추내시경","황금인공관절","성장클리닉"], "rating": 0,"website": "https://www.baroseogu.com/default/"},
    {"name": "아이언정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오대로 255 4층", "keywords": ["척추관절클리닉","스포츠재활클리닉"], "rating": 0,"website": "http://ironos.co.kr/"},
    {"name": "서구연세정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로394번길 1 백천빌딩", "keywords": ["체외충격파","척추클리닉","관절클리닉","일료일진료"], "rating": 0,"website": "https://blog.naver.com/seoguos"},
    {"name": "새힘정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 375", "keywords": ["도수치료","영양수액","1인치료실"], "rating": 0,"website": ""},
    {"name": "아나파나마취통증의학과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 375 금강아미움 303호", "keywords": ["통증클리닉","신경차단술","비수술적치료"], "rating": 0,"website": "https://anapanapainclinic.medisay.co.kr/"},
    {"name": "튼튼마취통증의학과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 372 4층~5층", "keywords": ["비수술치료","도수치료","재활치료"], "rating": 0,"website": "https://www.instagram.com/teunteun_pain_clinic/"},
    {"name": "가정신현 탑본 정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 369 서경백화점 3층 304호 가정신현 탑본 정형외과의원", "keywords": ["척추통증센터","관절클리닉","비수술클리닉","도수치료"], "rating": 0,"website": "http://www.topbone.co.kr/"},
    {"name": "엄기영정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 363 그린빌딩", "keywords": ["정형외과","신경외과","물리치료"], "rating": 0,"website": ""},
    {"name": "바로본365의원 본원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 309 3,4층", "keywords": ["통증클리닉","영양수액클리닉","자율신경클리닉","365진료"], "rating": 0,"website": "https://brb365.co.kr/"},
    {"name": "정재운정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 316 인정빌딩 2층", "keywords": ["척추클리닉","성장클리닉","재활치료","관절클리닉"], "rating": 0,"website": ""},
    {"name": "연세제일정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 287-1", "keywords": ["물리치료"], "rating": 0,"website": ""},
    {"name": "노송병원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 280 노송병원", "keywords": ["관절센터","척추센터","도수재활센터"], "rating": 0,"website": "https://nohsong.co.kr/"},
    {"name": "뉴성민병원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 신석로 70 뉴성민병원 1관", "keywords": ["수지외상센터","관절센터","척추센터","재활치료센터"], "rating": 0,"website": "http://www.smgh.co.kr/smgh/main2/index"},
    {"name": "세일정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 213", "keywords": ["물리치료"], "rating": 0,"website": ""},
    {"name": "팔팔마취통증의학과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 212 6층", "keywords": ["통증클리닉","비수술치료","도수치료","체외충격파치료"], "rating": 0,"website": "https://palpalpain.co.kr/"},
    {"name": "성모퍼스트정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 120 인성프라자 202호, 203호", "keywords": ["척추관절클리닉","하지정맥클리닉","수부상지수술","일요일진료"], "rating": 0,"website": "http://www.stmaryfirst.co.kr/"},
    {"name": "가좌신경외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 103", "keywords": ["정형외과","신경외과"], "rating": 0,"website": ""},
    {"name": "인하마취통증의학과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 100 가좌로얄프라자", "keywords": ["신경차단술","압통점치료","특수치료"], "rating": 0,"website": ""},
    {"name": "가좌정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 96 고려의원", "keywords": ["물리치료","신경외과","정형외과"], "rating": 0,"website": ""},
    {"name": "한길정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 85 우신프라자 2층", "keywords": ["물리치료","산재","입원"], "rating": 0,"website": ""},
    {"name": "가좌연세정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로337번길 7 3층 가좌연세정형외과", "keywords": ["입원실","척추관절클리닉","도수치료","수액클리닉"], "rating": 0,"website": "https://gajwaysos.imweb.me/"},
    {"name": "나은병원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 23", "keywords": ["종합병원","인공관절수술","입원실"], "rating": 0,"website": "https://blog.naver.com/naeun4119"},
#서구 치과
    {"name": "미소담치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 587 로얄프라자", "keywords": ["화목야간진료","치아검진"], "rating": 0,"website": ""},
    {"name": "검암웰치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 577 장은프라자", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "수서울치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 567 제일빌딩", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "세계로치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 서곶로 543 살리텍빌딩", "keywords": ["치아교정전문","소아교정"], "rating": 0,"website": ""},
    {"name": "서울리더스치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 497", "keywords": ["소아치과","치아교정","임플란트","턱관절"], "rating": 0,"website": ""},
    {"name": "검암우리치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 491", "keywords": ["화목야간진료","치아검진"], "rating": 0,"website": ""},
    {"name": "검암연세치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 498", "keywords": ["임플란트","보존치료","소아치과"], "rating": 0,"website": ""},
    {"name": "검암본플란트치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 477 201호", "keywords": ["임플란트","치아살리기"], "rating": 0,"website": "http://ga-bonplant.kr/"},
    {"name": "아이비치과의원","category":"치과","gu":"서구", "region": "경서동", "address": "인천 서구 경서로69번길 12", "keywords": ["임플란트","교정치료"], "rating": 0,"website": ""},
    {"name": "연세연희치과의원","category":"치과","gu":"서구", "region": "연희동", "address": "인천 서구 승학로 320", "keywords": ["임플란트","심미보철","치아교정"], "rating": 0,"website": ""},
    {"name": "연희수치과의원","category":"치과","gu":"서구", "region": "연희동", "address": "인천 서구 간촌로 4", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "조은내일치과병원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 승학로 250", "keywords": ["치과병원","임플란트","치아교정"], "rating": 0,"website": "http://gt-den.co.kr/"},
    {"name": "현치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 37 우리타워", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "연희보스톤치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 55 SM스카이빌", "keywords": ["목요일야간진료","임플란트"], "rating": 0,"website": ""},
    {"name": "웰치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로49번길 1", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "이&김치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 293", "keywords": ["임플란트","치아교정","심미보철"], "rating": 0,"website": ""},
    {"name": "연세림치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 281 자혜정형외과빌딩 3층", "keywords": ["치아검진"], "rating": 0,"website": ""},
    {"name": "서곶이좋은치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 300 엄지빌딩 202호", "keywords": ["임플란트","치아성형","보철"], "rating": 0,"website": ""},
    {"name": "미치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로 135 대동아파트상가 207호", "keywords": ["보철치료","심미치료","치주치료"], "rating": 0,"website": ""},
    {"name": "가톨릭관동대학교 국제성모병원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로100번길 25 가톨릭관동대학교 국제성모병원", "keywords": ["대학병원","임플란트","보철치료","보존치료"], "rating": 0,"website": "https://www.ish.or.kr/main/"},
    {"name": "늘치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라동 83-1", "keywords": ["소아치료","자연치아보존"], "rating": 0,"website": ""},
    {"name": "서울샤인치과의원 인천청라","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 24 3층", "keywords": ["수면치료","임플란트","투명교정"], "rating": 0,"website": "http://seoulshinedc.com/"},
    {"name": "청라퍼스널치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 90 청라MKVIEW 403호, 404호", "keywords": ["수면임플란트","잇몸치료","사랑니발치"], "rating": 0,"website": ""},
    {"name": "청라아이비치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 110 청라파이낸스센터 I, 2층", "keywords": ["자연치아살리기","네이게이션임플란트"], "rating": 0,"website": "http://cheongnaivy.co.kr/"},
    {"name": "바라던치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로100번길 24 쓰리엠파크2 3층", "keywords": ["임플란트","턱관절","틀니"], "rating": 0,"website": "http://baradundental.co.kr/"},
    {"name": "청라리더스치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 82", "keywords": ["임플란트","턱관절",""], "rating": 0,"website": "http://www.cheongnaleaders.com/"},
    {"name": "맑은미소치과의원 청라","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 86 2층", "keywords": ["임플란트","사랑니","교정치료"], "rating": 0,"website": "http://www.malgunmiso.com/"},
    {"name": "청라미래치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라루비로 99 3층", "keywords": ["임플란트","소아치료","치아교정"], "rating": 0,"website": "https://blog.naver.com/miraedent00"},
    {"name": "청라다온치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라루비로 93", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "http://daondent.com/"},
    {"name": "청라치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로74번길 31 월드프라자 5층", "keywords": ["임플란트","소아치료","교정치료"], "rating": 0,"website": "https://www.cheongnadental.co.kr/"},
    {"name": "서울클리어치과교정과치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 280 청라골든프라자 2층", "keywords": ["치아교정","성장기교정","비수술교정","덧니교정","주걱턱교정"], "rating": 0,"website": "https://seoulclear-cn.com/"},
    {"name": "청라퍼스트치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 264 5층", "keywords": ["자연치아살리기","임플란트"], "rating": 0,"website": "http://www.firstdent1.com/"},
    {"name": "미유치과의원 청라점","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로288번길 10 더스페이스타워 4층 401호, 402호", "keywords": ["임프란트","소아치과","충치치료"], "rating": 0,"website": "http://miudentalclinic.com/"},
    {"name": "연세예쁜미소치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로260번길 11 4층 연세예쁜미소치과 (다이소 건물)", "keywords": ["교정전문","소아교정"], "rating": 0,"website": "https://blog.naver.com/ysprettysmile"},
    {"name": "연세별치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로260번길 27", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "http://www.yonseibyeol.com/"},
    {"name": "모드니치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 587", "keywords": ["임플란트","신경치료","충치치료","잇몸치료"], "rating": 0,"website": "https://blog.naver.com/ljyilj"},
    {"name": "청라우림치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 610", "keywords": ["임플란트","치아검진"], "rating": 0,"website": ""},
    {"name": "청라이플란트치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 602 청라여성병원 1층", "keywords": ["임플란트","심미치료","충치치료"], "rating": 0,"website": "http://www.cneplant.co.kr/"},
    {"name": "이바른치과교정과치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 602 청라여성병원 1층", "keywords": ["교정전문","턱관절"], "rating": 0,"website": "https://ebarundental.com/"},
    {"name": "파랑새플란트 치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 594 5층 파랑새플란트치과", "keywords": ["임플란트","충치치료","일요일진료"], "rating": 0,"website": "http://www.bluebirddental.co.kr/"},
    {"name": "연세어린이치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588 청라센트럴프라자 401호", "keywords": ["수면치료","성장기교정","소아치료"], "rating": 0,"website": "http://yschild.co.kr/index.asp"},
    {"name": "서울원누리치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로586번길 9-4 쓰리엠타워 4층", "keywords": ["자연치아살리기","임플란트"], "rating": 0,"website": "http://wonnuridental.co.kr/"},
    {"name": "청라꾸러기치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로612번길 10-16 청라마르씨엘 5F", "keywords": ["소아치료","진정치료","충치치료"], "rating": 0,"website": "https://blog.naver.com/cheongnadent"},
    {"name": "닥터케어스치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로612번길 10-17 309호", "keywords": ["잇몸치료","임플란트","스케일링"], "rating": 0,"website": "https://blog.naver.com/ukyos"},
    {"name": "서울갤러리치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71", "keywords": ["임플란트","치아교정","심미보철"], "rating": 0,"website": "https://blog.naver.com/seoulgall"},
    {"name": "예미담치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71", "keywords": ["임플란트","치아교정","자연치아살리기"], "rating": 0,"website": "https://cnyemidam.com/"},
    {"name": "청라오치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 65 라임타워 4층 403호", "keywords": ["임플란트","사랑니","소아치료"], "rating": 0,"website": "https://blog.naver.com/0h_clinic"},
    {"name": "안앤정치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 51 에일린의 뜰 2층 우리은행 건물", "keywords": ["충치치료","임플란트","치아교정","레이저미백","보철치료"], "rating": 0,"website": "https://blog.naver.com/anjdental1"},
    {"name": "청라탑치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로586번길 22", "keywords": ["임플란트","치아교정","소아치료","사랑니"], "rating": 0,"website": "http://topbest.co.kr/"},
    {"name": "행복드림치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로102번길 8 5층", "keywords": ["임플란트","치아교정"], "rating": 0,"website": ""},
    {"name": "청라365클리어치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로 94 2층 (204,205,206호)", "keywords": ["일료일진료","네비게이션임플란트","급속교정","인비절라인"], "rating": 0,"website": "https://clear365.co.kr/home/index.php"},
    {"name": "한결치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로 78 제301, 302호", "keywords": ["임플란트","앞니급속교정"], "rating": 0,"website": "https://blog.naver.com/kjr3275"},
    {"name": "맑은미소치과의원 가정점","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 40", "keywords": ["임플란트","사랑니","치아교정"], "rating": 0,"website": "https://blog.naver.com/mmgajung"},
    {"name": "더바른치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 44 명문프라자 3층", "keywords": ["임플란트","치아발치"], "rating": 0,"website": "https://blog.naver.com/thebarundent"},
    {"name": "가정21세기치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로498번안길 16-1 퍼스트프라자 3층 301, 302호", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "https://blog.naver.com/21cdent_gajeong"},
    {"name": "연세센텀치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 90", "keywords": ["즉시임플란트","보존치료"], "rating": 0,"website": "https://blog.naver.com/yscentum"},
    

    



]

# -------------------------------
# gu별 행정구역
# -------------------------------
region_dict = {
    "서구": ["검암동","경서동","가좌동","가정동","공촌동","심곡동","신현동","석남동","시천동","연희동","원창동","청라동"],
    "검단구": ["금곡동","대곡동","당하동","마전동","백석동","불로동","오류동","왕길동","원당동"]
}

# -------------------------------
# 리뷰 로드 및 평균 계산
# -------------------------------
def load_reviews():
    with open('reviews.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_average_rating(hospital_name, reviews):
    ratings = [r["rating"] for r in reviews if r["hospital_name"] == hospital_name]
    if ratings:
        return round(sum(ratings) / len(ratings), 2)
    return None

# -------------------------------
# 라우트: 메인 페이지
# -------------------------------
@app.route('/')
def index():
    gu = request.args.get("gu", "")
    category = request.args.get("category", "")
    region = request.args.get("region", "")

    # 선택한 gu에 맞는 행정구역 목록
    regions = region_dict.get(gu, [])

    # 리뷰 불러오기
    reviews = load_reviews()

    # 평균 평점 계산
    for hospital in hospitals:
        avg = calculate_average_rating(hospital["name"], reviews)
        hospital["rating"] = avg if avg is not None else None

    # 병원 필터링
    filtered_hospitals = []
    for h in hospitals:
        if gu and h["gu"] != gu:
            continue
        if category and category not in h["category"]:
            continue
        if region and h["region"] != region:
            continue
        filtered_hospitals.append(h)
    
     # ✅ 가나다 순 정렬
    filtered_hospitals.sort(key=lambda x: x["name"])

        

    # 평점 없는 병원 처리
    for h in filtered_hospitals:
        if h["rating"] is None:
            h["rating"] = "평점 없음"

    visit_count = get_visit_count()
    return render_template(
        'index.html',
        hospitals=filtered_hospitals,
        region_dict=region_dict,
        visit_count=visit_count,
        selected_gu=gu,
        selected_category=category,
        selected_region=region,
        regions=regions
    )

# -------------------------------
# 라우트: 병원 상세 페이지
# -------------------------------
@app.route('/hospital/<name>')
def hospital_detail(name):
    hospital = next((h for h in hospitals if h["name"] == name), None)
    if not hospital:
        abort(404)
    reviews = load_reviews()
    hospital_reviews = [r for r in reviews if r["hospital_name"] == name]
    avg = calculate_average_rating(name, reviews)
    hospital["rating"] = avg if avg is not None else "평점 없음"
    visit_count = get_visit_count()
    return render_template('hospital_detail.html', hospital=hospital, reviews=hospital_reviews, visit_count=visit_count)


# -------------------------------
# 기타 라우트
# -------------------------------
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(BASE_DIR, "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return send_from_directory(BASE_DIR, "robots.txt")

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('.', 'ads.txt', mimetype='text/plain')


# -------------------------------
# 앱 실행
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
