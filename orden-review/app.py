
from flask import Flask, render_template, request, abort, send_from_directory, url_for
import json, os
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISIT_FILE = os.path.join(BASE_DIR, "visit.json")
REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")

# -------------------------------
# 병원 데이터 (원본 유지)
# -------------------------------
hospitals =[
    #{"name": "","category":"","gu":"", "region": "", "address": "", "keywords": ["",""], "rating": 0,"website": "","commercial_level":, "specialty": [] } 1=고관절,2=무릎 ,3=척추 ,4=어깨
    # 검단구 정형외과
    {"name": "온누리병원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 완정로 192 베스트프라자3층", "keywords": ["종합병원","수술"], "rating": 0,"website": "https://www.onnurihosp.com/","commercial_level": 1 ,"specialty": [] },
    {"name": "검단바로본365의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로178길", "keywords": ["순천향대 출신 대표원장","응급의학과 전문의","대학병원 교수 출신","척추클리닉","수액클리닉"], "rating": 0,"website": "https://kbrb365.co.kr/","commercial_level": 2 , "specialty": [] },
    {"name": "착한마디병원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 180", "keywords": ["관절센터","척추센터"], "rating": 0,"website": "http://goodmadi.co.kr/","commercial_level": 1 , "specialty": [] },
    {"name": "공감 마취통증의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 172 서주빌딩 3층", "keywords": ["인제대 출신 원장","척추질환","관절질환"], "rating": 0,"website": "http://www.xn--439azqz10e1fh.com/","commercial_level": 1 , "specialty": [] },
    {"name": "윤재활의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 172 4층", "keywords": ["재활의학과 전문의","시술 및 관절치료 40,000례 ","척추통증","도수교정"], "rating": 0,"website": "https://yoonpmrclinic-mo.imweb.me/","commercial_level": 1 , "specialty": [] },
    {"name": "정정형외과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 왕길동 638-4", "keywords": ["정형외과 전문의","물리치료"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "위풍당당정형외과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 검단로 480 3층", "keywords": ["경희대 출신 원장","척추,관절클리닉","도수교정"], "rating": 0,"website": "http://xn--ok1ba505m9xm.com/","commercial_level": 1 , "specialty": [2] },
    {"name": "미래안마취통증의학과의원","category":"정형외과","gu":"검단구","region": "왕길동", "address": "인천 서구 검단로 469 선명타운 3층", "keywords": ["마취통증의학과 전문의","허리,목디스크","오십견"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "이정형외과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 완정로 35", "keywords": ["정형외과 전문의","목,허리디스크","오십견"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "오케이마취통증의학과의원","category":"정형외과","gu":"검단구","region": "마전동", "address": "인천 서구 원당대로", "keywords": ["경희대 출신 원장","마취통증의학과 전문의","시술 및 차단술 20,000례","척추,관절클리닉","도수치료클리닉"], "rating": 0,"website": "http://okane.whost.co.kr/","commercial_level": 1 , "specialty": [] },
    {"name": "검단연합의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 660", "keywords": ["통증클리닉","물리치료"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "바로튼튼정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 서곶로 837 3~4층", "keywords": ["경희대 출신 원장","대학병원 교수 출신","척추클리닉","도수치료"], "rating": 0,"website": "https://barotuntun.medisay.co.kr/","commercial_level": 1 , "specialty": [3] },
    {"name": "검단탑병원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 청마로19번길 5", "keywords": ["종합병원","수술","입원실"], "rating": 0,"website": "https://tophospital.co.kr/main/main.html?","commercial_level": 2 , "specialty": [] },
    {"name": "원재활의학과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 850 3층", "keywords": ["경희대 출신 원장","대학병원 교수 출신","재활클리닉","재활필라테스"], "rating": 0,"website": "http://xn--vb0bu30cxlazkq79cmnb.com/","commercial_level": 1 , "specialty": [] },
    {"name": "골드정형외과의원","category":"정형외과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 221 엠파이어빌딩 701~705호", "keywords": ["인하대 출신 원장","대학병원 교수 출신","수술 10,000례","어깨관절"], "rating": 0,"website": "","commercial_level": 2 , "specialty": [4] },
    {"name": "하늘본튼튼의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 856 3층", "keywords": ["인하대 출신 원장","시술,차단술 30,000례","척추,관절클리닉","주사치료"], "rating": 0,"website": "http://xn--wh1bu0rv9ra054a.com/#section8","commercial_level": 2 , "specialty": [] },
    {"name": "원당연세정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 원당대로 866 5층, 6층", "keywords": ["연세대 출신 원장","통증클리닉"], "rating": 0,"website": "http://coconutz.kr/13388","commercial_level": 1 , "specialty": [] },
    {"name": "검단본정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 3로 112 4층", "keywords": ["정형외과 전문의","비수술진료","통증클리닉"], "rating": 0,"website": "https://www.xn--c79a6ix0no4lp2l1kc262b.com/","commercial_level": 2 , "specialty": [4] },
    {"name": "검단바른정형외과의원","category":"정형외과","gu":"검단구","region": "당하동", "address": "인천 서구 서로3로 104 2층", "keywords": ["한양대 출신 원장","대학병원 출신","척추,디스크클리닉","관절,힘줄재생클리닉"], "rating": 0,"website": "http://gdbareunos.com/","commercial_level": 2 , "specialty": [] },
    {"name": "검단이엠365의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음5로 30 2층,3층", "keywords": ["응급의학과 전문의","통증치료","주사치료"], "rating": 0,"website": "https://www.gdem365.com/","commercial_level": 1 , "specialty": [] },
    {"name": "검단정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 7층", "keywords": ["인하대 출신 원장","대학병원 출신","척추,관절클리닉","비수술치료"], "rating": 0,"website": "http://geomdanos.com/","commercial_level": 2 , "specialty": [2] },
    {"name": "서울정석정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 388 ABM타워 4층", "keywords": ["서울대 출신 원장","척추클리닉","통증클리닉"], "rating": 0,"website": "https://blog.naver.com/dnrpdyd53444","commercial_level": 2 , "specialty": [] },
    {"name": "연세마디윌의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 392 메트로시티 6층", "keywords": ["연세대 출신 원장","물리치료","주사치료"], "rating": 0,"website": "https://www.madiwill.com/","commercial_level": 2 , "specialty": [] },
    {"name": "검단더굿정형외과의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음대로 392 5층", "keywords": ["정형외과 전문의","척추,관절클리닉","도수치료","통증클리닉"], "rating": 0,"website": "http://thegoodgd.co.kr/index.php","commercial_level": 2 , "specialty": [] },
    {"name": "검단이화연합의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음5로 80 검단퍼스트 5층", "keywords": ["이화여대 출신 원장","주사치료"], "rating": 0,"website": "https://blog.naver.com/gumdanewha","commercial_level": 1, "specialty": [] },
    {"name": "365마디팔팔의원","category":"정형외과","gu":"검단구","region": "원당동", "address": "인천 서구 이음1로 386 6층", "keywords": ["정형외과 전문의","대학병원 출신","척추,관절클리닉","비수술클리닉","도수치료"], "rating": 0,"website": "http://365madi88.com/","commercial_level": 2 , "specialty": [] },
    {"name": "서울바른정형외과의원","category":"정형외과","gu":"검단구","region": "불로동", "address": "인천 서구 검단로 768번길2 2층", "keywords": ["정형외과 전문의","발목","척추,관절통증"], "rating": 0,"website": "http://www.barunseoulos.co.kr/","commercial_level": 2 , "specialty": [] },
    {"name": "검단연세정형외과의원","category":"정형외과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 222 푸리마더타워 605~613호 (불로동)", "keywords": ["연세대 출신 원장","척추,관절질환","비수술클리닉","도수치료"], "rating": 0,"website": "https://www.geomdanyonsei.com/","commercial_level": 2 , "specialty": [] },
    #검단구 치과
    {"name": "이정우치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 187 마전메디컬센터 5층", "keywords": ["임플란트","차아교정","신경치료"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "검단가온치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 178번길 1 검단빌딩 2층", "keywords": ["소아진료","틀니클리닉","사랑니클리닉","심미클리닉"], "rating": 0,"website": "https://www.gd-gaondental.com/","commercial_level": 2 , "specialty": [] },
    {"name": "미소드림치과의원","category":"치과","gu":"검단구", "region": "오류동", "address": "인천 서구 보듬5로 5 오덕프라자 3층 303호", "keywords": ["스케일링","임플란트"], "rating": 0,"website": "https://blog.naver.com/misodreamdental_","commercial_level": 1 , "specialty": [] },
    {"name": "송앤정치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 단봉로 107 성우프라자 302호", "keywords": ["임플란트","보철치료","충치치료","잇몸치료"], "rating": 0,"website": "https://www.instagram.com/songandjungdentalclinic/#","commercial_level": 1 , "specialty": [] },
    {"name": "서울현대치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 179 검단메디컬 303호", "keywords": ["임플란트","투명교정"], "rating": 0,"website": "https://www.omydentist.com/","commercial_level": 1 , "specialty": [] },
    {"name": "검단서울치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 검단로 469 선명타운 2층", "keywords": ["임플란트","서울대출신"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "우수치과의원검단","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 172 3층", "keywords": ["사랑니","충치치료","치아교정센터"], "rating": 0,"website": "http://www.woo-soo.co.kr/","commercial_level": 1 , "specialty": [] },
    {"name": "열린치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 170 광성빌딩", "keywords": ["야간진료","충치치료"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "행복담은샘치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 검단로 480 리치웰프라자 4층", "keywords": ["임플란트","충치치료","신경치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "스마일365치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 485 2,3층", "keywords": ["임플란트","치아교정","심미치료","치아관리","특화치료"], "rating": 0,"website": "http://www.smile365dc.com/","commercial_level": 1, "specialty": [] },
    {"name": "보스톤클래식치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 486 2층", "keywords": ["치아교정","보철치료","보존치료","치주치료","소아치료"], "rating": 0,"website": "https://www.bostonclassic.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "김준영치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 160", "keywords": ["스케일링","충치치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검단어린이치과의원","category":"치과","gu":"검단구", "region": "왕길동", "address": "인천 서구 완정로 153 이레메디칼센타 6층", "keywords": ["소아치과","영유아검진","소아교정"], "rating": 0,"website": "https://blog.naver.com/gumdancdc","commercial_level": 1, "specialty": [] },
    {"name": "미추홀치과","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 500", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "미담치과","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 502번길 1", "keywords": ["야간진료","치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "나은미소치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 검단로 508 이지준프라자 4층", "keywords": ["임플란트","교정치료","틀니"], "rating": 0,"website": "http://naeunmisodental.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "마전미소치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 마전로115번길 2-6 2-1", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "불로치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 764", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "이사랑부부치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 834 퀸스타운 신명아파트 상가", "keywords": ["보철치료","임플란트","소아치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "미래치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 검단로 842 월드메가마트 219호", "keywords": ["야간진료","치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검단일등치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 동화시로 112 JS프라자2 2층", "keywords": ["소아치료","턱관절","신경치료","임플란트"], "rating": 0,"website": "https://xn--c79a6ix0nt9be62bcnj.com/","commercial_level": 2, "specialty": [] },
    {"name": "검단브라이트치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 221 엠파이어빌딩 503~507호", "keywords": ["턱관절","사랑니","임플란트","라미네이트"], "rating": 0,"website": "https://blog.naver.com/brightdentclinic","commercial_level": 2, "specialty": [] },
    {"name": "검단쥬니어치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 221 6층 606호, 607호", "keywords": ["소아치료","치아교정","치아검진"], "rating": 0,"website": "http://xn--c79a6io7mwdn61hf9ec1j.com/","commercial_level": 2, "specialty": [] },
    {"name": "타임치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 841 골든벨프라자", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "다정한치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 고산후로 95번길 20 힘찬프라자 4층", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "루브르치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 861 원당프라자 3층", "keywords": ["임플란트","교정치료","사랑니"], "rating": 0,"website": "https://blog.naver.com/lvrdent","commercial_level": 1, "specialty": [] },
    {"name": "신동근치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 866 4층 402호", "keywords": ["틀니","임플란트","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "이튼치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 865 대산프라자 3층 304호", "keywords": ["임플란트","소아치료","치주치료","보철치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "바른공감치과의원검단점","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서로3로 104 신화프라자 3층", "keywords": ["소아치료","임플란트","사랑니"], "rating": 0,"website": "http://bagongdental.com/","commercial_level": 2, "specialty": [] },
    {"name": "치과로와치과의원검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 발산로 6 아인시티주차타워 306호", "keywords": ["고난이도임플란트","의식하진정치료","턱관절치료","충치치료"], "rating": 0,"website": "https://www.rowadental.com/","commercial_level": 2, "specialty": [] },
    {"name": "예온치과병원인천검단365점","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 이음4로 6 KR법조타워 5층", "keywords": ["임플란트","교정치료","소아치료","일요일진료"], "rating": 0,"website": "https://gd365.ye-on.com/","commercial_level": 2, "specialty": [] },
    {"name": "이플러스치과의원검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 30 301~303호", "keywords": ["임플란트","사랑니","보철치료"], "rating": 0,"website": "http://eplusdentistry.com/","commercial_level": 1, "specialty": [] },
    {"name": "나아라치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 36 더원타워 5층 501~503호", "keywords": ["임플란트","자연치아살리기","심미클리닉"], "rating": 0,"website": "https://xn--vb0bl2ehzhgnpbwk.com/","commercial_level": 2, "specialty": [] },
    {"name": "검단센트럴치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 이음대로 479 CS메디컬프라자 2층", "keywords": ["임플란트","사랑니","턱관절"], "rating": 0,"website": "인천 서구 이음대로 479 CS메디컬프라자 2층","commercial_level": 2, "specialty": [] },
    {"name": "연세꿈꾸는아이치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 7층", "keywords": ["소아치료","수면치료","성장교정"], "rating": 0,"website": "http://www.ysdreami.com/","commercial_level": 2, "specialty": [] },
    {"name": "서울바로치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 378 로뎀타워 3층", "keywords": ["임플란트","교정치료","소아치료"], "rating": 0,"website": "https://svdc.kr/#;","commercial_level": 1, "specialty": [] },
    {"name": "서울더블유치과교정과치과의원 검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 384 서영아너시티플러스 2층", "keywords": ["교정치료","임플란트"], "rating": 0,"website": "http://seoulwdent.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "연세검단치과의원 인천검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 388 ABM타워 5층 503~509호", "keywords": ["임플란트","치아교정","수면무통마취"], "rating": 0,"website": "https://xn--c79a6ix0ny8qtrf94n.kr/","commercial_level": 2, "specialty": [] },
    {"name": "이앤백치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음대로 392 4층", "keywords": ["치아교정","임플란트"], "rating": 0,"website": "https://lnbdental.com/","commercial_level": 1, "specialty": [] },
    {"name": "연세앤치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 60 JS프라자 5층", "keywords": ["임플란트","치주치료","소아치료","투명교정"], "rating": 0,"website": "https://ysannedent.qshop.ai/","commercial_level": 1, "specialty": [] },
    {"name": "더보다 구강악안면외과 치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 바리미로 17 4층", "keywords": ["의식하진정법","임플란트","사랑니","턱관절","수술치료"], "rating": 0,"website": "http://www.evodaoms.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "피어나치과교정과치과의원 검단","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 62 정인프라자 4층", "keywords": ["성장기교정","성인교정","치아미백"], "rating": 0,"website": "https://bloomortho.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "검단퍼스트치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 이음5로 80 검단퍼스트프라자 3층", "keywords": ["자연치아살리기","임플란트","심미보철","턱관절"], "rating": 0,"website": "https://geomdanfirst.imweb.me/","commercial_level": 2, "specialty": [] },
    {"name": "플란치과의원 인천 검단점","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 1045 6층", "keywords": ["임플란트","통증케어"], "rating": 0,"website": "https://geomdan.implan.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "검단뉴욕치과의원","category":"치과","gu":"검단구", "region": "원당동", "address": "인천 서구 원당대로 1045 4층 404호~407호", "keywords": ["구강근기능훈련","소아교정","투명교정","심미보철"], "rating": 0,"website": "http://xn--c79a6ix8linao62fwkk.com/","commercial_level": 2, "specialty": [] },
    {"name": "마전웰치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 70 2층 205호", "keywords": ["임플란트","충치치료","신경치료","치아미백","소아치료"], "rating": 0,"website": "https://blog.naver.com/well_dentalclinic","commercial_level": 2, "specialty": [] },
    {"name": "지오웰치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 원당대로 581 롯데마트 검단점 2층", "keywords": ["일요일진료","구강검진","충치치료","임플란트"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "브라이트치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 70 2층", "keywords": ["심미보철","임플란트","치주치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "파스텔치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 61", "keywords": ["임플란트","사랑니","신경치료"], "rating": 0,"website": "https://blog.naver.com/goodpastel","commercial_level": 1, "specialty": [] },
    {"name": "이안치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 60 정안빌딩", "keywords": ["치아검진","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검단다온치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 54 두영프라자 2층 202호", "keywords": ["소아치료","임플란트","신경치료"], "rating": 0,"website": "https://blog.naver.com/daondc2875","commercial_level": 2, "specialty": [] },
    {"name": "노블치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 35 대운프라자", "keywords": ["턱관절","잇몸치료"], "rating": 0,"website": "https://blog.naver.com/omahun2001","commercial_level": 1, "specialty": [] },
    {"name": "연세조아치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 36", "keywords": ["임플란트","예방치료","구강건강교육","치아미백","충치치료"], "rating": 0,"website": "https://sites.google.com/view/yonseijoa/","commercial_level": 1, "specialty": [] },
    {"name": "참조은박치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 31 동아프라자302호", "keywords": ["임플란트","치아교정","치아성형","치아미백"], "rating": 0,"website": "https://blog.naver.com/tweed2008","commercial_level": 1, "specialty": [] },
    {"name": "부치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 완정로 18", "keywords": ["임플란트","소아치료","심미치료","치아성형"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검단탑병원 치과","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로7번길 2 2층", "keywords": ["임플란트","보철치료","스케일링"], "rating": 0,"website": "https://tophospital.co.kr/main/main.html?","commercial_level": 1, "specialty": [] },
    {"name": "연세튼튼치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로19번길 20 203호", "keywords": ["임플란트","심미보철","충치치료","사랑니","치주치료"], "rating": 0,"website": "https://blog.naver.com/ysttdc","commercial_ level": 1, "specialty": [] },
    {"name": "강플란트치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 660 영프라자 10층 1001호", "keywords": ["임플란트","보철치료","치주치료"], "rating": 0,"website": "http://www.kangplant.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "드림라인치과교정과치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 원당대로 660 영프라자 5층", "keywords": ["성장기교정","성인교정","인비절라인"], "rating": 0,"website": "https://blog.naver.com/dldent","commercial_level": 1, "specialty": [] },
    {"name": "연세세브란스치과의원 검단","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 서곶로 866 3층", "keywords": ["수면치료","구강악안면외과","자연치아살리기","임플란트"], "rating": 0,"website": "http://yonsev.com/","commercial_level": 2, "specialty": [] },
    {"name": "서울더탑치과의원","category":"치과","gu":"검단구", "region": "마전동", "address": "인천 서구 원당대로 663 한종프라자 3층", "keywords": ["임플란트","치아교정","심미치료","소아치료"], "rating": 0,"website": "https://www.seoulthetop.com/","commercial_level": 2, "specialty": [] },
    {"name": "당하치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로167번길 8", "keywords": ["임플란트","턱관절","심미보철","치주치료"], "rating": 0,"website": "https://blog.naver.com/dentistjeon","commercial_level": 1, "specialty": [] },
    {"name": "위드치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로 171 청석빌딩 3층 1호", "keywords": ["스케일링","소아치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "이앤미치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 청마로 163", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "데일리치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서곶로 788 2층 데일리치과", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "미플러스치과의원","category":"치과","gu":"검단구", "region": "당하동", "address": "인천 서구 서곶로 754 당하 이마트", "keywords": ["무통치료","임플란트","사랑니"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "바른수치과의원","category":"치과","gu":"검단구", "region": "백석동", "address": "인천 서구 한들로 74 한들타워1차 4층", "keywords": ["임플란트","치아성형","자연치아살리기","소아교정"], "rating": 0,"website": "http://bareunsu.com/","commercial_level": 2 , "specialty": [] },
    {"name": "검단중앙치과의원","category":"치과","gu":"검단구", "region": "불로동", "address": "인천 서구 고산후로 222 푸리마더타워 4층", "keywords": ["무통마취","뼈이식임플란트재수술","턱관절"], "rating": 0,"website": "https://gdjungang.com/","commercial_level": 2, "specialty": [] },
# 서구 정형외과
    {"name": "정우정형외과의원","category":"정형외과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 501", "keywords": ["정형외과 전문의","일요일진료","물리치료"], "rating": 0,"website": "","commercial_level": 1 , "specialty": [] },
    {"name": "마디튼튼마취통증의학과의원","category":"정형외과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 507 장한프라자 2, 3층 201, 202, 301호", "keywords": ["충남대 출신 원장","신경차단술 40,000례","척추클리닉","관절클리닉","도수치료"], "rating": 0,"website": "http://xn--2z1b52gu10aa.com/","commercial_level": 2, "specialty": [] },
    {"name": "인천연세병원","category":"정형외과","gu":"서구", "region": "연희동", "address": "인천 서구 승학로 320", "keywords": ["연세대 출신 원장","무지외반증","도수치료","디스크"], "rating": 0,"website": "https://m.icys.kr/","commercial_level": 2, "specialty": [] },
    {"name": "서인천현대정형외과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 45 현대메디칼 2층", "keywords": ["정형외과 전문의","척추클리닉","통증클리닉"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "모두탑365정형외과의원 인천서구점","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 293 우민빌딩 2층, 4층", "keywords": ["경희대 출신 원장","척추,관절클리닉","비수술클리닉"], "rating": 0,"website": "http://modutop-icsg.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "자혜정형외과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 281 자혜정형외과", "keywords": ["정형외과 전문의","척추클리닉","관절염","물리치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "더본마취통증의학과의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 가정로 451 가정역 4번 출구 벨라미센텀시티 4층 448~454호", "keywords": ["주사치료","척추클리닉","도수치료"], "rating": 0,"website": "https://blog.naver.com/thebonepain","commercial_level": 1, "specialty": [] },
    {"name": "서울아산마디척의원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 300 401호", "keywords": ["비수술치료","재활운동치료"], "rating": 0,"website": "https://www.asanmadichuk.com/","commercial_level": 2, "specialty": [] },
    {"name": "가톨릭관동대학교 국제성모병원","category":"정형외과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로100번길 25 가톨릭관동대학교 국제성모병원", "keywords": ["대학병원","수술","입원","응급실"], "rating": 0,"website": "https://www.ish.or.kr/main/","commercial_level": 1, "specialty": [] },
    {"name": "세로척정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 90 2층 201-204호", "keywords": ["정형외과 전문의","척추클리닉","관절클리닉","소아정형"], "rating": 0,"website": "https://xn--2o2b15nzyj.com/","commercial_level": 2, "specialty": [] },
    {"name": "청라이엠365의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로100번길 24 202~205, 301~305호", "keywords": ["가정의학과 전문의","주말진료","야간진료","도수치료"], "rating": 0,"website": "https://cnem365.co.kr/ ","commercial_level": 1, "specialty": [] },
    {"name": "제대로정형외과마취통증의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로 78 4층", "keywords": ["정형외과 전문의","척추클리닉","입원","도수치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "청라우리정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로74번길 31 월드프라자 2층", "keywords": ["정형외과 전문의","물리치료","도수치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "진정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 264 403~404호", "keywords": ["정형외과 전문의","비수술치료","혈관영양치료","성장클리닉"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "드림재활의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588", "keywords": ["재활의학과 전문의","도수치료","디스크"], "rating": 0,"website": "http://dreamrm.com/","commercial_level": 1, "specialty": [] },
    {"name": "청라코끼리마취통증의학과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 594 406~408호", "keywords": ["단국대 출신 원장","통증클리닉","도수치료"], "rating": 0,"website": "https://kkrpain.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "청라성모정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71 진영메디피아3층", "keywords": ["가톨릭대 출신 원장","특수치료","시술치료","비수술치료"], "rating": 0,"website": "http://www.xn--vb0b32rvpcgujb5g1qcdtmsst.com/","commercial_level": 1, "specialty": [] },
    {"name": "청라바른정형외과의원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 65 라임타워 5층", "keywords": ["정형외과 전문의","일요일진료","척추관절센터","성장클리닉","도수치료"], "rating": 0,"website": "http://cheongrabarun.co.kr/default/","commercial_level": 1, "specialty": [] },
    {"name": "청라국제병원","category":"정형외과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로102번길 8 2층, 4층", "keywords": ["중앙대 출신 원장","365일진료","척추센터","관절센터","통증치료"], "rating": 0,"website": "https://jsjhospital.co.kr:9003/main/main.php","commercial_level": 1, "specialty": [] },
    {"name": "가정성모의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 청중로 486 부일프라자 3, 4층", "keywords": ["통증클리닉","교정클리닉","도수치료센터"], "rating": 0,"website": "http://gajeongsm.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "서울정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로 468 드림타워 7층, 801호, 802호", "keywords": ["서울대 출신 원장","척추클리닉","관절클리닉","시술클리닉","도수치료"], "rating": 0,"website": "https://osyang0501.dothome.co.kr/HOME","commercial_level": 1, "specialty": [] },
    {"name": "고려재활의학과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로464번길 15 쓰리엠타워 5층", "keywords": ["재활의학과 전문의","입원치료","물리치료","연골주사"], "rating": 0,"website": "https://blog.naver.com/korearehab","commercial_level": 1, "specialty": [] },
    #####
    {"name": "바로서구병원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정동 196-3", "keywords": ["신경외과,정형외과 전문의","세브란스병원 조교수","양방향척추내시경","황금인공관절","성장클리닉"], "rating": 0,"website": "https://www.baroseogu.com/default/","commercial_level": 2, "specialty": [] },
    {"name": "아이언정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오대로 255 4층", "keywords": ["스포츠의학,정형외과 전문의","척추관절클리닉","스포츠재활클리닉"], "rating": 0,"website": "http://ironos.co.kr/","commercial_level": 2, "specialty": [4] },
    {"name": "서구연세정형외과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로394번길 1 백천빌딩", "keywords": ["정형외과 전문의","체외충격파","척추클리닉","관절클리닉","일료일진료"], "rating": 0,"website": "https://blog.naver.com/seoguos","commercial_level": 1, "specialty": [] },
    {"name": "새힘정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 375", "keywords": ["정형외과 전문의","도수치료","영양수액","1인치료실"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "아나파나마취통증의학과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 375 금강아미움 303호", "keywords": ["마취통증의학과 전문의","통증클리닉","신경차단술","비수술적치료"], "rating": 0,"website": "https://anapanapainclinic.medisay.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "튼튼마취통증의학과의원","category":"정형외과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 372 4층~5층", "keywords": ["마취통증의학과 전문의","척추클리닉","비수술치료","도수치료","재활치료"], "rating": 0,"website": "https://www.instagram.com/teunteun_pain_clinic/","commercial_level": 1, "specialty": [] },
    {"name": "가정신현 탑본 정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 369 서경백화점 3층 304호 가정신현 탑본 정형외과의원", "keywords": ["고려대 출신 원장","척추통증센터","관절클리닉","비수술클리닉","도수치료"], "rating": 0,"website": "http://www.topbone.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "엄기영정형외과의원","category":"정형외과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 363 그린빌딩", "keywords": ["정형외과 전문의","물리치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "바로본365의원 본원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 309 3,4층", "keywords": ["순천향대 출신 원장","통증클리닉","영양수액클리닉","자율신경클리닉","365진료"], "rating": 0,"website": "https://brb365.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "강남의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 308 석남프라자 301호", "keywords": ["응급의학과 전문의","통증의학과","통증클리닉","영양클리닉"], "rating": 0,"website": "","commercial_level":1, "specialty": [] },
    {"name": "정재운정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 316 인정빌딩 2층", "keywords": ["정형외과 전문의","척추클리닉","성장클리닉","재활치료","관절클리닉"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연세제일정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 287-1", "keywords": ["정형외과 전문의","물리치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "노송병원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 280 노송병원", "keywords": ["대학병원 교수 출신","관절센터","척추센터","도수재활센터"], "rating": 0,"website": "https://nohsong.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "뉴성민병원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 신석로 70 뉴성민병원 1관", "keywords": ["고려대 출신 센터장","수지외상센터","관절센터","척추센터","재활치료센터"], "rating": 0,"website": "http://www.smgh.co.kr/smgh/main2/index","commercial_level": 1, "specialty": [] },
    {"name": "세일정형외과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 213", "keywords": ["정형외과 전문의","물리치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "팔팔마취통증의학과의원","category":"정형외과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 212 6층", "keywords": ["서울대 출신 원장","통증클리닉","비수술치료","도수치료","체외충격파치료"], "rating": 0,"website": "https://palpalpain.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "성모퍼스트정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 120 인성프라자 202호, 203호", "keywords": ["가톨릭대 출신 원장","대학병원 교수 출신","척추관절클리닉","하지정맥클리닉","수부상지수술","일요일진료"], "rating": 0,"website": "http://www.stmaryfirst.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "가좌신경외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 103", "keywords": ["정형외과","신경외과"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "인하마취통증의학과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 100 가좌로얄프라자", "keywords": ["마취통증의학과 전문의","신경차단술","압통점치료","특수치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "가좌정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 96 고려의원", "keywords": ["정형외과 전문의","물리치료","신경외과","정형외과"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "한길정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 85 우신프라자 2층", "keywords": ["물리치료","산재","입원"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "가좌연세정형외과의원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로337번길 7 3층 가좌연세정형외과", "keywords": ["연세대 출신 원장","입원실","척추관절클리닉","도수치료","수액클리닉"], "rating": 0,"website": "https://gajwaysos.imweb.me/","commercial_level": 1, "specialty": [] },
    {"name": "나은병원","category":"정형외과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 23", "keywords": ["종합병원","인공관절수술","입원실"], "rating": 0,"website": "https://blog.naver.com/naeun4119","commercial_level": 1, "specialty": [] },
#서구 치과
    {"name": "미소담치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 587 로얄프라자", "keywords": ["화목야간진료","치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검암웰치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 577 장은프라자", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "수서울치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 567 제일빌딩", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "세계로치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 서곶로 543 살리텍빌딩", "keywords": ["치아교정전문","소아교정"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울리더스치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 497", "keywords": ["소아치과","치아교정","임플란트","턱관절"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검암우리치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 491", "keywords": ["화목야간진료","치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검암연세치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 498", "keywords": ["임플란트","보존치료","소아치과"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "검암본플란트치과의원","category":"치과","gu":"서구", "region": "검암동", "address": "인천 서구 승학로 477 201호", "keywords": ["임플란트","치아살리기"], "rating": 0,"website": "http://ga-bonplant.kr/","commercial_level": 2, "specialty": [] },
    {"name": "아이비치과의원","category":"치과","gu":"서구", "region": "경서동", "address": "인천 서구 경서로69번길 12", "keywords": ["임플란트","교정치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연세연희치과의원","category":"치과","gu":"서구", "region": "연희동", "address": "인천 서구 승학로 320", "keywords": ["임플란트","심미보철","치아교정"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연희수치과의원","category":"치과","gu":"서구", "region": "연희동", "address": "인천 서구 간촌로 4", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "조은내일치과병원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 승학로 250", "keywords": ["치과병원","임플란트","치아교정"], "rating": 0,"website": "http://gt-den.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "현치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 37 우리타워", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연희보스톤치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 탁옥로 55 SM스카이빌", "keywords": ["목요일야간진료","임플란트"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "웰치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로49번길 1", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "이&김치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 293", "keywords": ["임플란트","치아교정","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연세림치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 281 자혜정형외과빌딩 3층", "keywords": ["치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서곶이좋은치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 서곶로 300 엄지빌딩 202호", "keywords": ["임플란트","치아성형","보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "미치과의원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로 135 대동아파트상가 207호", "keywords": ["보철치료","심미치료","치주치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "가톨릭관동대학교 국제성모병원","category":"치과","gu":"서구", "region": "심곡동", "address": "인천 서구 심곡로100번길 25 가톨릭관동대학교 국제성모병원", "keywords": ["대학병원","임플란트","보철치료","보존치료"], "rating": 0,"website": "https://www.ish.or.kr/main/", "commercial_level": 1, "specialty": [] },
    {"name": "늘치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라동 83-1", "keywords": ["소아치료","자연치아보존"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울샤인치과의원 인천청라","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 24 3층", "keywords": ["수면치료","임플란트","투명교정"], "rating": 0,"website": "http://seoulshinedc.com/","commercial_level": 2, "specialty": [] },
    {"name": "청라퍼스널치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 90 청라MKVIEW 403호, 404호", "keywords": ["수면임플란트","잇몸치료","사랑니발치"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "청라아이비치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로 110 청라파이낸스센터 I, 2층", "keywords": ["자연치아살리기","네이게이션임플란트"], "rating": 0,"website": "http://cheongnaivy.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "바라던치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라한내로100번길 24 쓰리엠파크2 3층", "keywords": ["임플란트","턱관절","틀니"], "rating": 0,"website": "http://baradundental.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "청라리더스치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 82", "keywords": ["임플란트","턱관절"], "rating": 0,"website": "http://www.cheongnaleaders.com/","commercial_level": 1, "specialty": [] },
    {"name": "맑은미소치과의원 청라","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 솔빛로 86 2층", "keywords": ["임플란트","사랑니","교정치료"], "rating": 0,"website": "http://www.malgunmiso.com/","commercial_level": 2, "specialty": [] },
    {"name": "청라미래치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라루비로 99 3층", "keywords": ["임플란트","소아치료","치아교정"], "rating": 0,"website": "https://blog.naver.com/miraedent00","commercial_level": 1, "specialty": [] },
    {"name": "청라다온치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라루비로 93", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "http://daondent.com/","commercial_level": 1, "specialty": [] },
    {"name": "청라치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 크리스탈로74번길 31 월드프라자 5층", "keywords": ["임플란트","소아치료","교정치료"], "rating": 0,"website": "https://www.cheongnadental.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "서울클리어치과교정과치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 280 청라골든프라자 2층", "keywords": ["치아교정","성장기교정","비수술교정","덧니교정","주걱턱교정"], "rating": 0,"website": "https://seoulclear-cn.com/","commercial_level": 1, "specialty": [] },
    {"name": "청라퍼스트치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로 264 5층", "keywords": ["자연치아살리기","임플란트"], "rating": 0,"website": "http://www.firstdent1.com/","commercial_level": 1, "specialty": [] },
    {"name": "미유치과의원 청라점","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로288번길 10 더스페이스타워 4층 401호, 402호", "keywords": ["임프란트","소아치과","충치치료"], "rating": 0,"website": "http://miudentalclinic.com/","commercial_level": 1, "specialty": [] },
    {"name": "연세예쁜미소치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로260번길 11 4층 연세예쁜미소치과 (다이소 건물)", "keywords": ["교정전문","소아교정"], "rating": 0,"website": "https://blog.naver.com/ysprettysmile","commercial_level": 1, "specialty": [] },
    {"name": "연세별치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라커낼로260번길 27", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "http://www.yonseibyeol.com/","commercial_level": 2, "specialty": [] },
    {"name": "모드니치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 587", "keywords": ["임플란트","신경치료","충치치료","잇몸치료"], "rating": 0,"website": "https://blog.naver.com/ljyilj","commercial_level": 1, "specialty": [] },
    {"name": "청라우림치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 610", "keywords": ["임플란트","치아검진"], "rating": 0,"website": "","commercial_level": 2, "specialty": [] },
    {"name": "청라이플란트치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 602 청라여성병원 1층", "keywords": ["임플란트","심미치료","충치치료"], "rating": 0,"website": "http://www.cneplant.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "이바른치과교정과치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 602 청라여성병원 1층", "keywords": ["교정전문","턱관절"], "rating": 0,"website": "https://ebarundental.com/","commercial_level": 1, "specialty": [] },
    {"name": "파랑새플란트 치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 594 5층 파랑새플란트치과", "keywords": ["임플란트","충치치료","일요일진료"], "rating": 0,"website": "http://www.bluebirddental.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "연세어린이치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588 청라센트럴프라자 401호", "keywords": ["수면치료","성장기교정","소아치료"], "rating": 0,"website": "http://yschild.co.kr/index.asp","commercial_level": 1, "specialty": [] },
    {"name": "서울삼성치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588 3층 303, 304, 305호", "keywords": ["임플란트","치아교정","사랑니","라미네이트","수면치료"], "rating": 0,"website": "https://seoulsamsungdent.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "청라아트치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로 588 9층 청라아트치과", "keywords": ["임플란트","충치치료","턱관절","사랑니"], "rating": 0,"website": "https://blog.naver.com/art-dental","commercial_level": 1, "specialty": [] },
    {"name": "서울원누리치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로586번길 9-4 쓰리엠타워 4층", "keywords": ["자연치아살리기","임플란트"], "rating": 0,"website": "http://wonnuridental.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "청라꾸러기치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로612번길 10-16 청라마르씨엘 5F", "keywords": ["소아치료","진정치료","충치치료"], "rating": 0,"website": "https://blog.naver.com/cheongnadent","commercial_level": 1, "specialty": [] },
    {"name": "닥터케어스치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로612번길 10-17 309호", "keywords": ["잇몸치료","임플란트","스케일링"], "rating": 0,"website": "https://blog.naver.com/ukyos","commercial_level": 1, "specialty": [] },
    {"name": "서울갤러리치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71", "keywords": ["임플란트","치아교정","심미보철"], "rating": 0,"website": "https://blog.naver.com/seoulgall","commercial_level": 1},
    {"name": "예미담치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 71", "keywords": ["임플란트","치아교정","자연치아살리기"], "rating": 0,"website": "https://cnyemidam.com/","commercial_level": 1, "specialty": [] },
    {"name": "청라오치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 65 라임타워 4층 403호", "keywords": ["임플란트","사랑니","소아치료"], "rating": 0,"website": "https://blog.naver.com/0h_clinic","commercial_level": "", "specialty": [] },
    {"name": "안앤정치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라라임로 51 에일린의 뜰 2층 우리은행 건물", "keywords": ["충치치료","임플란트","치아교정","레이저미백","보철치료"], "rating": 0,"website": "https://blog.naver.com/anjdental1","commercial_level": 1, "specialty": [] },
    {"name": "청라탑치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 중봉대로586번길 22", "keywords": ["임플란트","치아교정","소아치료","사랑니"], "rating": 0,"website": "http://topbest.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "행복드림치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로102번길 8 5층", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "청라365클리어치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로 94 2층 (204,205,206호)", "keywords": ["일료일진료","네비게이션임플란트","급속교정","인비절라인"], "rating": 0,"website": "https://clear365.co.kr/home/index.php","commercial_level": 2, "specialty": [] },
    {"name": "한결치과의원","category":"치과","gu":"서구", "region": "청라동", "address": "인천 서구 청라에메랄드로 78 제301, 302호", "keywords": ["임플란트","앞니급속교정"], "rating": 0,"website": "https://blog.naver.com/kjr3275","commercial_level": 1, "specialty": [] },
    {"name": "맑은미소치과의원 가정점","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 40", "keywords": ["임플란트","사랑니","치아교정"], "rating": 0,"website": "https://blog.naver.com/mmgajung","commercial_level": 1, "specialty": [] },
    {"name": "더바른치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 44 명문프라자 3층", "keywords": ["임플란트","치아발치"], "rating": 0,"website": "https://blog.naver.com/thebarundent","commercial_level": 2, "specialty": [] },
    {"name": "가정21세기치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로498번안길 16-1 퍼스트프라자 3층 301, 302호", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "https://blog.naver.com/21cdent_gajeong","commercial_level": 1, "specialty": [] },
    {"name": "연세센텀치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오재3로 90", "keywords": ["즉시임플란트","보존치료"], "rating": 0,"website": "https://blog.naver.com/yscentum","commercial_level": 2, "specialty": [] },
    {"name": "굿닥터신치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로 468 드림타워 4층 405호, 406호", "keywords": ["임플란트","일반진료","소아치료"], "rating": 0,"website": "https://blog.naver.com/gooddrshin","commercial_level": 1, "specialty": [] },
    {"name": "루원치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로464번길 7 (가정동) 성도메디피아 3층", "keywords": ["임플란트","턱관절"], "rating": 0,"website": "https://blog.naver.com/lu1dental","commercial_level": 2, "specialty": [] },
    {"name": "루원하다소아치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 염곡로464번길 15 쓰리엠타워 3층", "keywords": ["소아치료","진정치료","예방치료","구강검진"], "rating": 0,"website": "https://hadakids.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "서울이자라는치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 451 벨라미 센텀시티 4층 서울이자라는치과", "keywords": ["임플란트","보철치료","치아교정"], "rating": 0,"website": "https://growingteeth.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "연세미시간치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 451 벨라미센텀시티2차 5층 551~555호", "keywords": ["임플란트","틀니","교정치료"], "rating": 0,"website": "https://ysmcdental.com/","commercial_level": 1, "specialty": [] },
    {"name": "인천맥치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오대로 255 3층", "keywords": ["임플란트","신경치료","투명교정"], "rating": 0,"website": "https://xn--vb0bv8v3rko4eqnc.com/","commercial_level": 1, "specialty": [] },
    {"name": "루원퍼스트치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 서곶로 50 루원시티 대성베르힐 더 센트로 2층", "keywords": ["충치치료","신경치료","임플란트","치아미백"], "rating": 0,"website": "http://www.toothfirstden.com/","commercial_level": 2, "specialty": [] },
    {"name": "루원닥터유치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 봉오대로 270 302동 116, 117호", "keywords": ["임플란트","구강검진"], "rating": 0,"website": "https://blog.naver.com/lu1dryoo","commercial_level": 2, "specialty": [] },
    {"name": "리더탑치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 437 SK 리더스뷰 상가 B/ 301동 310, 311호", "keywords": ["임플란트","보존치료","잇몸치료","심미치료"], "rating": 0,"website": "https://xn--vb0b83jgyf33xo0c.com/","commercial_level": 2, "specialty": [] },
    {"name": "프라임치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 437 301동 2층 208~209호", "keywords": ["임플란트","충치치료","신경치료","보철치료"], "rating": 0,"website": "http://prime-dent.kr/","commercial_level": 1, "specialty": [] },
    {"name": "루원미소치과교정과치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 406 A동 3층 308호", "keywords": ["치아교정","충치치료","소아성장교정","투명교정"], "rating": 0,"website": "https://blog.naver.com/luwonmiso","commercial_level": 2, "specialty": [] },
    {"name": "유니콘어린이치과의원 루원시티점","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 406 B동 2층 221~223호", "keywords": ["구강검진","충치치료","성장기교정"], "rating": 0,"website": "https://blog.naver.com/unicon_kids_dentist","commercial_level": 2, "specialty": [] },
    {"name": "올바른치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로394번길 1 백천빌딩 3층", "keywords": ["보존치료","신경치료","충치치료"], "rating": 0,"website": "https://blog.naver.com/kamo_s","commercial_level": 1, "specialty": [] },
    {"name": "오승훈치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 388", "keywords": ["치아검진","스케일링","충치치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "가정백세플란트치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 386 3층", "keywords": ["임플란트","재수술","치아교정","보철치료"], "rating": 0,"website": "https://100seplant.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "예은치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 382 201호", "keywords": ["임플란트","보철치료","치아보존"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울탑프란트치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 379", "keywords": ["수면치료","임플란트",""], "rating": 0,"website": "http://www.seoultopplant.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "신현굿모닝치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 석곶로 7-2", "keywords": ["스케일링","치아검진"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "바른윤치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 375 309호 (신현동, 금강아미움)", "keywords": [], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "닥터함치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 374", "keywords": ["수면임플란트"], "rating": 0,"website": "https://blog.naver.com/drhamden","commercial_level": 2, "specialty": [] },
    {"name": "뉴욕리더스치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 372 2층 뉴욕리더스치과", "keywords": ["임플란트","심미치료","소아치료"], "rating": 0,"website": "http://www.nyleaders.co.kr/","commercial_level": 1, "specialty": [] },
    {"name": "서울가족치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 369 서경백화점 3층 303호", "keywords": ["자연치아살리기","임플란트","교정클리닉"], "rating": 0,"website": "http://www.familydent.co.kr/","commercial_level": 2, "specialty": [] },
    {"name": "스마트치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 370 가정빌딩 3층", "keywords": ["임플란트","치아교정"], "rating": 0,"website": "https://blog.naver.com/smart2275","commercial_level":1 , "specialty": [] },
    {"name": "신현윤치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 원창로 174", "keywords": ["임플란트","심미보철","잇몸치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "플러스치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 363 그린빌딩", "keywords": ["치주치료","보철","심미치료","임플란트"], "rating": 0,"website": "","commercial_level":1 , "specialty": []  },
    {"name": "정순민치과의원","category":"치과","gu":"서구", "region": "가정동", "address": "인천 서구 가정로 364-1 창대빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "오세건치과의원","category":"치과","gu":"서구", "region": "신현동", "address": "인천 서구 가정로 359 아빈빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "인치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 율도로 32", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level":1 , "specialty": [] },
    {"name": "신석치과","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 317", "keywords": ["30년","일반진료"], "rating": 0,"website": "","commercial_level":1 , "specialty": [] },
    {"name": "서인천연합치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 서달로149번길 12-11 노란빌딩3층", "keywords": ["무통마취","임플란트","치주수술","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서인천뉴욕치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 309", "keywords": ["임플란트","치아미백","심미치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "강남치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 308 석남프라자", "keywords": ["임플란트","교정치료","보철치료","심미치료","충치치료","신경치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "참플란트치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로308번길 2 3층 참플란트치과의원", "keywords": ["자연치아살리기","심미보철","임플란트","치아교정"], "rating": 0,"website": "https://blog.naver.com/champlant","commercial_level":1 , "specialty": [] },
    {"name": "새하늘치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 서달로 151 하남빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level":1 , "specialty": [] },
    {"name": "이편한치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 신석로 79 무한빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "인천센터치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 280 6층", "keywords": ["임플란트","보철치료"], "rating": 0,"website": "http://www.icenterdental.co.kr/","commercial_level":2 , "specialty": [] },
    {"name": "사랑의치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 서달로123번길 3", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "이사랑치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 길주로 90 소매점", "keywords": ["임플란트","심미보철","치아교정","잇몸치료","사랑니"], "rating": 0,"website": "","commercial_level":1 , "specialty": [] },
    {"name": "이엔수석치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 212 5층", "keywords": ["임플란트","보철치료"], "rating": 0,"website": "http://www.xn--vb0bs59arvai3ioncr4q.kr/","commercial_level": 2, "specialty": [] },
    {"name": "굿모닝치과 인천서구점","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 거북로 89 기업은행", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "장인호치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 208", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울휴플러스치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 거북로 99 금정빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "석남서울치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 204", "keywords": ["임플란트","스케일링"], "rating": 0,"website": "https://www.instagram.com/seoknam_seoul_dentalclinic/#","commercial_level": 1, "specialty": [] },
    {"name": "석남치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 201-1 두일빌딩", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "승치과의원","category":"치과","gu":"서구", "region": "석남동", "address": "인천 서구 가정로 202 3층", "keywords": ["임플란트","심미보철","치주치료","충치치료"], "rating": 0,"website": "https://blog.naver.com/sdental1861","commercial_level": 1, "specialty": [] },
    {"name": "모아치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 가정로151번길 11", "keywords": ["임플란트","치아교정","심미치료"], "rating": 0,"website": "https://gajwamore.creatorlink.net/","commercial_level": 1, "specialty": [] },
    {"name": "플랜트치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 가정로 123", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "참고은치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 가정로 127", "keywords": ["임플란트","치아미백","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "국제플란트치과의원","category":"치과","gu":"서구", "region": "원창동", "address": "인천 서구 북항로32번안길 41 건원프라자 206~208호", "keywords": ["임플란트","보철치료","보존치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "연세플러스치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 102-2", "keywords": ["임플란트","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "박윤현치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 99", "keywords": ["임플란트","치아교정","치아미백"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "두치과","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 100", "keywords": ["스케일링","치아교정","임플란트","심미보철"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "미소담은치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 96 3층 미소담은치과", "keywords": ["일반진료","스케일링","레진치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "정영달치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 85 우신프라자", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울보스톤치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로 102-2", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "세이프치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로100번길 24 신라빌딩 2층", "keywords": ["임플란트","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "한솔치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 원적로96번길 26 가좌프라자쇼핑", "keywords": ["임플란트","심미보철","사각턱교정","치아미백"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "건플란트치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로337번길 18-3", "keywords": ["임플란트","야간진료","자연치아"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "사과치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로337번길 16 가좌한신 휴아파트 상가 3층", "keywords": ["임플란트","보철치료","충치치료","스케일링","무통치료"], "rating": 0,"website": "https://blog.naver.com/apple-dental","commercial_level": 1, "specialty": [] },
    {"name": "서울미소치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로337번길 13 진주아파트 5단지 상가 2층", "keywords": ["임플란트","심미보철","치아교정","충치치료"], "rating": 0,"website": "","commercial_level": 2, "specialty": [] },
    {"name": "연세해맑은치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 장고개로 277-1 청운프라자", "keywords": ["임플란트","심미보철","치아교정","차아성형","돌출입","신경치료"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "원치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 고래울로 4 연세내과의원", "keywords": ["일반진료","스케일링"], "rating": 0,"website": "","commercial_level": 1, "specialty": [] },
    {"name": "서울온건치과의원","category":"치과","gu":"서구", "region": "가좌동", "address": "인천 서구 건지로 375 2층", "keywords": ["자연치아살리기","임플란트","심미치료","사랑니","턱관절"], "rating": 0,"website": "https://seoulogdental.co.kr/","commercial_level": 1, "specialty": [] }

]

region_dict = {
    "서구": ["검암동","경서동","가좌동","가정동","공촌동","심곡동","신현동","석남동","시천동","연희동","원창동","청라동"],
    "검단구": ["금곡동","대곡동","당하동","마전동","백석동","불로동","오류동","왕길동","원당동"]
}

# -------------------------------
# 유틸리티 함수
# -------------------------------
def get_today_date():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")

def load_reviews():
    if not os.path.exists(REVIEWS_FILE):
        return []
    with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def calculate_average_rating(hospital_name, reviews):
    ratings = [r["rating"] for r in reviews if r["hospital_name"] == hospital_name]
    if ratings:
        return round(sum(ratings) / len(ratings), 2)
    return None

def load_visits():
    if not os.path.exists(VISIT_FILE):
        return {"count": 0, "date": get_today_date()}
    with open(VISIT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if data.get("date") != get_today_date():
                return {"count": 0, "date": get_today_date()}
            return data
        except json.JSONDecodeError:
            return {"count": 0, "date": get_today_date()}

def save_visits(data):
    os.makedirs(os.path.dirname(VISIT_FILE), exist_ok=True)
    with open(VISIT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@app.before_request
def count_visit():
    if request.path.startswith("/static") or request.path.endswith("favicon.ico"):
        return
    data = load_visits()
    data["count"] = data.get("count", 0) + 1
    save_visits(data)

def get_visit_count():
    return load_visits().get("count", 0)

# -------------------------------
# 3중 정밀 코멘트 데이터베이스 
# -------------------------------
PRECISION_COMMENTS = {
    "10~20대": {
        "목": {
            "사무직": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 모니터 높이를 잘 맞춰두는 것이 평생의 목 건강을 결정합니다. 모니터가 낮으면 목 근육이 피가 안 통할 정도로 꽉 뭉쳐서 낫지 않는 통증이 생겨요. 모니터 윗부분을 눈높이에 맞추고, 키보드를 몸쪽으로 당겨 어깨가 안쪽으로 말리지 않게 펴주는 것이 중요합니다.",
            "현장직": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 무거운 짐을 들거나 아래를 보며 일할 때 목 관절이 흔들리기 쉽습니다. 고개만 까딱하며 숙이지 말고, 무릎과 골반을 함께 굽혀서 몸 전체로 하중을 나누어 들어야 목 디스크를 지킬 수 있습니다. 일을 시작하기 전에는 가벼운 스트레칭으로 목 근육을 충분히 부드럽게 만들어주세요.",
            "운동선수": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 무거운 무게를 들 때 숨을 멈추고 억지로 힘을 주면 목 안쪽 압력이 급격히 높아집니다. 겉 근육만 키우기보다 목 안쪽에서 뼈를 지탱하는 힘을 길러야 충돌 사고가 나도 크게 다치지 않습니다. 자세가 무너진 상태에서의 운동은 오히려 목 건강을 갉아먹으니 주의하세요.",
            "학생": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 고개를 푹 숙이고 공부하면 목뼈의 정상적인 곡선이 반대로 꺾이게 됩니다. 이는 단순히 목만 아픈 게 아니라 머리로 가는 피의 흐름을 방해해 집중력을 떨어뜨려요. 반드시 독서대를 사용해 고개를 들고, 50분마다 벽에 등을 대고 똑바로 서서 목 위치를 바로잡아 주세요.",
            "주부/은퇴": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 젊은 나이여도 살림을 할 때 고개를 숙이는 시간이 길면 목 노화가 빨리 옵니다. 설거지나 요리를 할 때 작업대를 높이거나 발판을 써서 최대한 허리와 목이 굽지 않게 하세요. 잘 때는 목의 굴곡을 편안하게 받쳐주는 베개를 써서 낮 동안 지친 목 인대가 쉴 수 있게 해줘야 합니다."
        },
        "허리": {
            "사무직": "허리는 앉아 있을 때 서 있을 때보다 2배 이상의 압박을 받습니다. 신입사원 시절 장시간 앉아 있는 습관은 허리 디스크의 원인이 됩니다. 의자 깊숙이 엉덩이를 넣고 허리 받침대를 사용하여 정상적인 곡선을 유지하세요. 1시간마다 일어나서 골반을 돌려주는 것만으로도 큰 부상을 막을 수 있습니다.",
            "현장직": "허리는 앉아 있을 때 서 있을 때보다 2배 이상의 압박을 받습니다. 현장에서 무거운 물건을 들 때 허리만 숙이는 동작은 매우 위험합니다. 반드시 무릎을 굽혀 물건을 몸쪽으로 바짝 붙여 들어 올리세요. 허리의 힘이 아닌 하체의 힘을 이용해야 척추뼈 사이의 압력을 줄이고 디스크를 보호할 수 있습니다.",
            "운동선수": "허리는 앉아 있을 때 서 있을 때보다 2배 이상의 압박을 받습니다. 고중량 운동 시 허리가 굽어지는 것은 척추에 시한폭탄을 심는 것과 같습니다. 복압을 유지하는 호흡법을 익히고, 겉 근육보다 허리를 지탱하는 속 근육(코어) 강화에 집중하세요. 통증을 참고 하는 훈련은 기량 향상이 아닌 은퇴를 앞당길 뿐입니다.",
            "학생": "허리는 앉아 있을 때 서 있을 때보다 2배 이상의 압박을 받습니다. 공부할 때 구부정하게 앉거나 다리를 꼬는 습관은 척추측만증과 허리 통증의 주범입니다. 책상과 의자 높이를 조절하여 무릎이 골반보다 약간 낮게 위치하도록 하고, 쉬는 시간마다 기지개를 켜서 눌려 있는 척추 마디마디를 늘려주세요.",
            "주부/은퇴": "허리는 앉아 있을 때 서 있을 때보다 2배 이상의 압박을 받습니다. 젊은 층의 가사 노동 중 엎드려 걸레질하거나 쪼그려 앉는 자세는 허리에 치명적입니다. 가급적 서서 일하는 도구를 사용하고, 무거운 짐을 옮길 때는 가족의 도움을 받거나 나누어서 옮기세요. 평소 걷기 운동을 통해 허리 주변 근육을 튼튼하게 유지하는 것이 중요합니다."
            },
        
        "어깨": {
            "사무직": "어깨는 무거운 물체를 강한 힘으로 갑자기 들 때 가장 쉽게 손상됩니다. 평소 컴퓨터 작업으로 굳어 있는 상태에서 갑자기 무거운 비품을 들거나 팔을 뻗는 동작은 위험합니다. 물건을 들기 전에는 어깨를 가볍게 돌려 예열하고, 최대한 몸에 바짝 붙여 어깨 힘줄에 가해지는 장력을 줄여주세요.",
            "현장직": "어깨는 무거운 물체를 강한 힘으로 갑자기 들 때 가장 쉽게 손상됩니다. 충분히 몸이 풀리지 않은 상태에서 무거운 장비를 확 잡아채는 동작은 어깨 힘줄 파열의 주원인입니다. 모든 물건은 반동을 이용하지 말고 천천히 들어 올리며, 어깨 위로 물건을 드는 작업 시에는 반드시 보조 도구를 활용하세요.",
            "운동선수": "어깨는 무거운 물체를 강한 힘으로 갑자기 들 때 가장 쉽게 손상됩니다. 본 운동 전 가벼운 무게로 관절의 온도를 충분히 높이지 않고 바로 고중량에 도전하는 것은 매우 위험합니다. 한 번의 무리한 욕심이 어깨 관절 수명을 깎아먹을 수 있으니, 감당 가능한 범위 내에서 통제된 힘을 사용하는 훈련이 필요합니다.",
            "학생": "어깨는 무거운 물체를 강한 힘으로 갑자기 들 때 가장 쉽게 손상됩니다. 무거운 책가방을 멘 채로 갑자기 뛰거나 친구와 장난치며 팔을 세게 휘두르는 동작은 어깨 관절에 큰 충격을 줍니다. 어깨 근육이 유연해지도록 틈틈이 스트레칭을 하고, 가방은 양쪽 어깨로 나누어 메어 하중을 고르게 분산하세요.",
            "주부/은퇴": "어깨는 무거운 물체를 강한 힘으로 갑자기 들 때 가장 쉽게 손상됩니다. 높은 곳에 있는 무거운 냄비를 내리거나 젖은 빨래 뭉치를 한꺼번에 들어 올리는 동작을 주의해야 합니다. 무거운 물체는 한 번에 들지 말고 나누어서 옮기며, 어깨의 힘보다는 몸 전체의 반동을 줄이고 천천히 움직이는 습관을 들이세요."
            },
         
        "무릎": {
            "사무직": "무릎은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 일어날 때 , 빠르게 방향을 전환할 때 쉽게 손상됩니다. 장시간 의자에 앉아 있다가 갑자기 급하게 일어나면 무릎 연골에 큰 충격이 가해집니다. 일어날 때는 손으로 책상을 짚어 하중을 분산하고, 틈틈이 다리를 쭉 펴서 무릎 관절 내부의 압력을 낮춰주는 것이 좋습니다.",
            "현장직": "무릎은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 일어날 때 , 빠르게 방향을 전환할 때 쉽게 손상됩니다. 무거운 자재를 든 채로 쪼그려 앉거나 갑자기 방향을 트는 동작은 무릎 인대에 치명적입니다. 가급적 무릎을 굽히는 각도를 줄이고, 무거운 물건을 들고 이동할 때는 보폭을 작게 하여 무릎 관절의 흔들림을 최소화하세요.",
            "운동선수": "무릎은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 일어날 때 , 빠르게 방향을 전환할 때 쉽게 손상됩니다. 충분한 예열 없이 고중량 스쿼트를 하거나 착지 시 무릎이 안쪽으로 꺾이는 동작은 연골판 파열의 주원인입니다. 허벅지 근육을 골고루 단련하여 무릎 관절을 단단히 고정하고, 감당하기 어려운 무게로 반동을 주어 운동하지 않도록 주의하세요.",
            "학생": "무릎은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 일어날 때 , 빠르게 방향을 전환할 때 쉽게 손상됩니다. 쉬는 시간에 갑자기 뛰어 나가거나 계단을 두세 칸씩 급하게 뛰어오르는 동작은 무릎 앞쪽 뼈에 과도한 압력을 줍니다. 평소 의자에 앉을 때 다리를 꼬거나 의자 밑으로 깊숙이 넣는 습관을 버려야 무릎 연골이 변형되는 것을 막을 수 있습니다.",
            "주부/은퇴": "무릎은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 일어날 때 , 빠르게 방향을 전환할 때 쉽게 손상됩니다. 젊은 나이여도 바닥에 쪼그려 앉아 집안일을 하거나 무거운 장바구니를 들고 가파른 계단을 오르는 것은 무릎 노화를 앞당깁니다. 모든 작업은 의자에 앉아서 하고, 무거운 물건을 들 때는 무릎의 반동보다는 주변 지지대를 활용해 천천히 움직이세요."
            }, 
        "손목손가락": {
            "사무직": "손목과 손가락은 무거운 물체를 강한 힘으로 쥐거나 비트는 동작을 반복할 때 가장 쉽게 손상됩니다. 장시간 마우스와 키보드를 사용하며 손목이 꺾인 상태를 유지하면 신경이 눌려 저림 증상이 나타납니다. 손목 받침대를 사용해 수평을 유지하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주세요.",
            "현장직": "손목과 손가락은 무거운 물체를 강한 힘으로 쥐거나 비트는 동작을 반복할 때 가장 쉽게 손상됩니다. 무거운 공구를 꽉 쥐고 장시간 진동을 견디거나 무리하게 힘을 주어 비트는 동작은 인대 염증을 유발합니다. 손바닥 전체로 도구를 감싸 쥐어 하중을 분산하고, 보호 장갑을 착용해 관절에 가해지는 충격을 흡수해야 합니다.",
            "운동선수": "손목과 손가락은 무거운 물체를 강한 힘으로 쥐거나 비트는 동작을 반복할 때 가장 쉽게 손상됩니다. 본인의 악력을 넘어선 고중량을 억지로 버티거나 손목이 뒤로 꺾인 채로 하중을 견디는 것은 매우 위험합니다. 손목 보호대를 적절히 활용하고, 운동 전후로 손가락 마디마디를 부드럽게 풀어주는 예열 과정을 거치세요.",
            "학생": "손목과 손가락은 무거운 물체를 강한 힘으로 쥐거나 비트는 동작을 반복할 때 가장 쉽게 손상됩니다. 펜을 너무 꽉 쥐고 글씨를 쓰거나 스마트폰을 한 손으로 들고 엄지손가락만 과하게 사용하는 습관은 관절 변형을 일으킵니다. 필기 시 힘을 빼는 연습을 하고, 스마트폰은 양손으로 나누어 사용하여 특정 관절에만 무리가 가지 않게 하세요.",
            "주부/은퇴": "손목과 손가락은 무거운 물체를 강한 힘으로 쥐거나 비트는 동작을 반복할 때 가장 쉽게 손상됩니다. 무거운 냄비를 한 손으로 들거나 젖은 세탁물을 강하게 비틀어 짜는 동작은 손목 인대를 늘어나게 만듭니다. 물건을 들 때는 두 손을 모두 사용하고, 병뚜껑을 따거나 걸레를 짤 때는 보조 도구를 활용해 손가락 마디의 부담을 줄여주세요."
            },
        "발목발가락": {
            "사무직": "발목과 발가락은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 방향을 틀 때 가장 쉽게 손상됩니다. 딱딱한 구두나 꽉 끼는 운동화는 발가락 변형과 발바닥 통증의 원인이 됩니다. 평소 아킬레스건을 늘려주는 스트레칭을 생활화하고, 발가락을 웅크렸다 펴는 '발가락 가위바위보' 운동을 통해 발 주변 근육의 유연성을 길러주세요.",
            "현장직": "발목과 발가락은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 방향을 틀 때 가장 쉽게 손상됩니다. 딱딱한 구두나 꽉 끼는 운동화는 발가락 변형과 발바닥 통증의 원인이 됩니다. 평소 아킬레스건을 늘려주는 스트레칭을 생활화하고, 발가락을 웅크렸다 펴는 '발가락 가위바위보' 운동을 통해 발 주변 근육의 유연성을 길러주세요.",
            "운동선수": "발목과 발가락은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 방향을 틀 때 가장 쉽게 손상됩니다. 딱딱한 구두나 꽉 끼는 운동화는 발가락 변형과 발바닥 통증의 원인이 됩니다. 평소 아킬레스건을 늘려주는 스트레칭을 생활화하고, 발가락을 웅크렸다 펴는 '발가락 가위바위보' 운동을 통해 발 주변 근육의 유연성을 길러주세요.",
            "학생": "발목과 발가락은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 방향을 틀 때 가장 쉽게 손상됩니다. 딱딱한 구두나 꽉 끼는 운동화는 발가락 변형과 발바닥 통증의 원인이 됩니다. 평소 아킬레스건을 늘려주는 스트레칭을 생활화하고, 발가락을 웅크렸다 펴는 '발가락 가위바위보' 운동을 통해 발 주변 근육의 유연성을 길러주세요.",
            "주부/은퇴": "발목과 발가락은 무거운 체중이 실린 상태에서 강한 힘으로 갑자기 방향을 틀 때 가장 쉽게 손상됩니다. 딱딱한 구두나 꽉 끼는 운동화는 발가락 변형과 발바닥 통증의 원인이 됩니다. 평소 아킬레스건을 늘려주는 스트레칭을 생활화하고, 발가락을 웅크렸다 펴는 '발가락 가위바위보' 운동을 통해 발 주변 근육의 유연성을 길러주세요."
            },
        "고관절": {
            "사무직": "고관절은 상체와 하체를 잇는 핵심 관절로, 체중을 분산하고 다리의 가동 범위를 결정하는 중요한 역할을 합니다. 장시간 의자에 앉아 있으면 고관절 앞쪽 근육이 짧아져 '골반 씹힘' 현상이 생기기 쉬우며, 이는 신입사원 시기 골반 불균형의 주범이 됩니다. 1시간마다 일어나 엉덩이 근육을 자극하고, 무릎이 골반보다 높지 않게 의자 높이를 조절하는 것이 중요합니다.",
            "현장직": "고관절은 상체와 하체를 잇는 핵심 관절로, 체중을 분산하고 다리의 가동 범위를 결정하는 중요한 역할을 합니다. 무거운 짐을 들고 이동할 때 고관절이 제대로 회전하지 않으면 그 하중이 고스란히 허리로 전달되어 부상을 유발합니다. 무릎만 쓰지 말고 고관절을 접어 사용하는 '힙힌지' 자세를 익히고, 퇴근 후에는 서혜부(사타구니) 주변을 부드럽게 마사지해 피로를 풀어주세요.",
            "운동선수": "고관절은 상체와 하체를 잇는 핵심 관절로, 체중을 분산하고 다리의 가동 범위를 결정하는 중요한 역할을 합니다. 폭발적인 방향 전환이나 과도한 유연성 훈련은 비구순 파열의 원인이 될 수 있으며, 통증을 단순 근육통으로 치부해 무리하게 스트레칭만 하는 것은 위험합니다. 관절을 잡아주는 심부 근육 강화와 충분한 휴식을 병행하여 관절 수명을 관리해야 합니다.",
            "학생": "고관절은 상체와 하체를 잇는 핵심 관절로, 체중을 분산하고 다리의 가동 범위를 결정하는 중요한 역할을 합니다. 공부할 때 의자 끝에 걸터앉거나 양반다리를 하는 습관은 고관절 비대칭과 척추측만증을 유발할 수 있으므로 10대 성장기에 특히 주의가 필요합니다. 50분마다 '개구리 자세' 스트레칭을 통해 긴장을 완화하고, 골반에서 소리가 난다면 근육 불균형을 의심해봐야 합니다.",
            "주부/은퇴": "고관절은 상체와 하체를 잇는 핵심 관절로, 체중을 분산하고 다리의 가동 범위를 결정하는 중요한 역할을 합니다. 젊은 나이여도 아이를 한쪽 골반으로 받쳐 드는 자세는 고관절 충돌 증후군을 유발하는 치명적인 습관입니다. 무게 중심을 양발에 고르게 분산하고, 무거운 짐은 카트를 사용하는 등 고관절에 가해지는 편중된 하중을 의식적으로 줄여주는 노력이 필요합니다."
        },
        "팔꿈치": {
            "사무직": "팔꿈치는 손목과 어깨를 잇는 지렛대 역할을 하며, 미세한 반복 동작만으로도 주변 힘줄에 과부하가 걸리기 쉬운 부위입니다. 사무직의 경우 마우스를 잡을 때 팔꿈치가 공중에 떠 있거나 책상 모서리에 눌리는 자세가 지속되면 '테니스 엘보'와 유사한 통증이 발생할 수 있습니다. 팔꿈치를 책상 위에 편안하게 지지하고, 손목뿐만 아니라 팔 전체를 사용하여 마우스를 움직이는 습관을 들이세요.",
            "현장직": "팔꿈치는 손목과 어깨를 잇는 지렛대 역할을 하며, 미세한 반복 동작만으로도 주변 힘줄에 과부하가 걸리기 쉬운 부위입니다. 무거운 공구를 반복적으로 들어 올리거나 나사를 강하게 조이는 동작은 팔꿈치 안쪽과 바깥쪽 인대에 미세한 파열을 유발할 수 있습니다. 장비를 사용하기 전 충분한 전완근 스트레칭을 실시하고, 보호대를 착용하여 관절에 가해지는 충격을 분산시켜야 합니다.",
            "운동선수": "팔꿈치는 손목과 어깨를 잇는 지렛대 역할을 하며, 미세한 반복 동작만으로도 주변 힘줄에 과부하가 걸리기 쉬운 부위입니다. 투구나 라켓 스포츠처럼 팔을 강하게 휘두르는 동작은 팔꿈치 관절 내부의 압력을 급격히 높여 연골 손상이나 인대 변형을 초래할 수 있습니다. 기술적인 폼 교정과 함께 근육의 회복 시간을 철저히 보장해야 하며, 통증이 시작되면 즉시 훈련 강도를 조절해야 합니다.",
            "학생": "팔꿈치는 손목과 어깨를 잇는 지렛대 역할을 하며, 미세한 반복 동작만으로도 주변 힘줄에 과부하가 걸리기 쉬운 부위입니다. 공부할 때 턱을 괴거나 팔꿈치를 책상에 강하게 누르는 습관은 팔꿈치 터널 증후군(신경 눌림)을 유발해 손가락 저림으로 이어질 수 있습니다. 필기 시 과도한 힘을 빼고, 쉬는 시간마다 팔을 쭉 펴서 눌려 있던 신경과 근육의 긴장을 풀어주는 것이 필요합니다.",
            "주부/은퇴": "팔꿈치는 손목과 어깨를 잇는 지렛대 역할을 하며, 미세한 반복 동작만으로도 주변 힘줄에 과부하가 걸리기 쉬운 부위입니다. 젊은 층이라도 무거운 프라이팬을 한 손으로 들거나 빨래를 짜는 등 팔꿈치를 비트는 동작을 반복하면 인대에 무리가 가기 쉽습니다. 무거운 물건은 두 손으로 나누어 들고, 가사 노동 시에는 팔꿈치 가동 범위를 최소화하여 근육의 피로도를 낮추는 노력이 중요합니다."
        },
        "등/날개뼈": {
            "사무직": "등과 날개뼈 주변 근육은 흉추를 지지하고 올바른 상체 자세를 유지하는 핵심적인 역할을 수행합니다. 사무직의 경우 모니터에 집중하며 어깨를 앞으로 말면 날개뼈 사이 근육이 과하게 늘어나 피로해지고, 이는 등 전체의 뻐근함으로 이어집니다. 의식적으로 가슴을 펴 날개뼈를 등 가운데로 모아주는 동작을 반복하고, 등받이에 날개뼈 아래쪽까지 밀착하여 앉는 습관을 들여야 합니다.",
            "현장직": "등과 날개뼈 주변 근육은 흉추를 지지하고 올바른 상체 자세를 유지하는 핵심적인 역할을 수행합니다. 현장에서 무거운 물건을 들 때 견갑골(날개뼈)이 고정되지 않으면 어깨 관절에 과한 부담이 실려 회전근개 손상까지 유발할 수 있습니다. 물건을 들기 전 날개뼈를 안정적으로 하강시켜 고정하는 법을 익히고, 작업 후에는 폼롤러 등을 이용해 흉추 주변의 뭉친 근육을 반드시 이완시켜주세요.",
            "운동선수": "등과 날개뼈 주변 근육은 흉추를 지지하고 올바른 상체 자세를 유지하는 핵심적인 역할을 수행합니다. 등 근육의 유연성이 부족하면 어깨나 허리가 그 가동 범위를 대신 보상하게 되어 부상 위험이 급격히 높아집니다. 견갑골의 움직임을 통제하는 전거근과 능형근을 강화하여 안정성을 확보하고, 상체 근력 운동 전 흉추의 회전 가동성을 확보하는 예열 과정을 필수적으로 거쳐야 합니다.",
            "학생": "등과 날개뼈 주변 근육은 흉추를 지지하고 올바른 상체 자세를 유지하는 핵심적인 역할을 수행합니다. 책상에 엎드리듯 공부하거나 무거운 가방을 한쪽으로만 메면 날개뼈의 높낮이가 달라지며 척추가 휘는 원인이 될 수 있습니다. 주기적으로 기지개를 켜 눌려 있던 등 근육을 펴주고, 양쪽 날개뼈가 등 뒤에서 서로 만난다는 느낌으로 어깨를 뒤로 넘겨 긴장을 풀어주는 것이 중요합니다.",
            "주부/은퇴": "등과 날개뼈 주변 근육은 흉추를 지지하고 올바른 상체 자세를 유지하는 핵심적인 역할을 수행합니다. 젊은 시기라도 장시간 고개를 숙이고 재료를 손질하거나 아이를 안는 동작은 날개뼈 주변 근육의 긴장도를 높여 만성적인 등 통증을 유발합니다. 작업 중간중간 어깨를 크게 돌려 견갑골의 움직임을 만들어주고, 잘 때는 등을 곧게 펼 수 있는 적절한 경도의 매트리스를 사용하는 것이 좋습니다."
        },
    },
    "30~40대": { 
        "목": {
            "사무직": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 거북목 자세로 인해 경추 디스크의 수분이 빠지고 퇴행이 본격화되는 시기입니다. 단순히 근육이 뭉친 것을 넘어 목뼈 사이 간격이 좁아지면 만성 두통과 팔 저림이 시작될 수 있습니다. 이제는 습관 교정을 넘어, 업무 중 수시로 턱을 당기는 맥켄지 운동을 통해 경추의 C자 곡선을 강제로라도 만들어줘야 합니다.",
            "현장직": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 반복되는 상하 작업과 무거운 장비 사용으로 인해 목 관절 면의 마모가 가속화되는 시기입니다. 젊을 때처럼 근육의 힘으로만 버티다가는 목 인대가 두꺼워져 신경 통로가 좁아질 위험이 큽니다. 작업 시 목만 까딱하기보다 몸 전체를 활용해 시선을 이동하고, 일과 후에는 목 주변 열감을 식히는 냉찜질로 염증 반응을 다스려야 합니다.",
            "운동선수": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 고강도 훈련이 누적된 목은 주변 인대가 비후되어 있거나 경추 불안정증을 겪을 확률이 매우 높습니다. 무리하게 목 근육을 강화하려다 오히려 신경을 압박할 수 있으니, 흉추(등뼈)의 가동성을 확보해 목에 쏠리는 하중을 분산시키는 전략이 필요합니다. 통증이 있다면 훈련 강도를 즉시 낮추고 관절의 회복 시간을 최우선으로 확보하세요.",
            "학생": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 자격증이나 고시 공부로 책상에 앉게 되면, 이미 약해진 경추 인대가 고정된 자세를 견디지 못하고 역C자 변형을 일으키기 쉽습니다. 이는 뇌 혈류량을 저하시켜 집중력을 갉아먹는 주범이 됩니다. 반드시 독서대를 사용해 시선을 높이고, 쉬는 시간마다 벽에 뒤통수를 밀착해 목 위치를 리셋하는 동작을 '생존 스트레칭'이라 생각하고 실천하세요.",
            "주부/은퇴": "고개를 15도만 숙여도 목은 12kg의 하중을 견뎌야 합니다. 오랜 육아와 가사로 인해 목뼈가 일자로 굳어버리 쉬운 시기입니다. 집안일을 할 때 목에 가해지는 하중은 나이가 들수록 디스크 돌출로 이어질 확률이 급격히 높아집니다. 작업대를 최대한 높여 고개를 숙이는 각도를 줄이고, 잘 때는 경추 전만을 지지해주는 기능성 베개를 사용해 밤사이 목의 긴장을 반드시 풀어줘야 합니다."
        },
        "허리": {
            "사무직": "앉아 있을 때 허리가 받는 압력은 서 있을 때의 2배, 구부정할 땐 3배까지 치솟습니다. 30~40대 사무직의 고질병인 허리 디스크는 대부분 의자 끝에 걸터앉는 습관에서 시작됩니다. 엉덩이를 의자 깊숙이 밀착시키고, 무너진 허리 곡선을 살려주는 기능성 쿠션을 활용하세요. 1시간마다 반드시 일어나 1~2분간 제자리 걷기를 하여 척추 마디의 압력을 분산해야 합니다.",
            "현장직": "앉아 있을 때 허리가 받는 압력은 서 있을 때의 2배, 구부정할 땐 3배까지 치솟습니다. 무거운 자재를 들 때 허리 힘에만 의존하면 척추 뼈 사이의 연골이 갑작스러운 압력을 견디지 못하고 돌출될 수 있습니다. 반드시 복대에 의지하기보다 복부에 힘을 주는 법을 익히고, 물건을 들 때는 무릎을 굽혀 하체의 힘을 이용하는 '스쿼트 자세'를 습관화해야 합니다.",
            "운동선수": "앉아 있을 때 허리가 받는 압력은 서 있을 때의 2배, 구부정할 땐 3배까지 치솟습니다. 선수 생활의 연장은 강력한 기립근과 코어 근육에 달려 있습니다. 고중량 훈련 시 허리가 말리는 '버트 윙크' 현상을 철저히 배제하고, 통증이 느껴질 때는 단순 근육통으로 치부하지 말고 신경 압박 여부를 반드시 확인하세요. 무리한 반동은 척추 분리증으로 이어질 수 있습니다.",
            "학생": "앉아 있을 때 허리가 받는 압력은 서 있을 때의 2배, 구부정할 땐 3배까지 치솟습니다. 늦은 나이에 공부를 병행하는 30~40대라면 체력이 떨어져 자세가 무너지기 쉽습니다. 엎드리거나 다리를 꼬는 자세는 골반을 틀어지게 해 결국 허리 통증을 유발합니다. 책상 높이를 조절해 상체가 앞으로 숙여지지 않게 하고, 틈틈이 엎드려서 상체를 들어 올리는 '맥켄지 운동'을 권장합니다.",
            "주부/은퇴": "앉아 있을 때 허리가 받는 압력은 서 있을 때의 2배, 구부정할 땐 3배까지 치솟습니다. 아이를 안거나 무거운 장바구니를 반복적으로 드는 동작은 허리에 미세한 손상을 누적시킵니다. 바닥에 앉는 좌식 생활보다는 의자에 앉는 입식 생활로 환경을 개선하고, 가사 노동 중간중간 허리를 뒤로 젖혀 굽어있는 척추를 반대로 펴주는 동작을 수시로 반복하세요."
            },
       "어깨": {
            "사무직": "어깨는 척추 정렬이 무너진 상태에서 무거운 물건을 급하게 들거나 팔을 빠르게 휘두를 때 가장 쉽게 손상됩니다. 굽은 등과 거북목은 어깨 관절 사이를 좁게 만들어, 작은 반동에도 힘줄이 끼여 파열될 수 있습니다. 평소 날개뼈를 바르게 정렬하는 습관을 들여 어깨 공간을 확보하고, 갑작스러운 상체 움직임보다는 천천히 근육을 예열한 뒤 움직이세요.",
            "현장직": "어깨는 척추 정렬이 무너진 상태에서 무거운 물건을 급하게 들거나 팔을 빠르게 휘두를 때 가장 쉽게 손상됩니다. 30~40대는 관절의 유연성이 떨어지는 시기이므로, 등이 굽은 채로 무거운 도구를 확 잡아채는 동작은 매우 위험합니다. 가슴을 펴 척추를 바로 세우고, 물건을 들 때는 반동을 이용하지 말고 몸에 밀착시켜 천천히 힘을 쓰는 것이 어깨를 지키는 길입니다.",
            "운동선수": "어깨는 척추 정렬이 무너진 상태에서 무거운 물건을 급하게 들거나 팔을 빠르게 휘두를 때 가장 쉽게 손상됩니다. 견갑골의 안정성이 확보되지 않은 상태에서의 폭발적인 투구구나 스윙, 고중량 리프팅은 어깨 관절에 시한폭탄을 심는 것과 같습니다. 흉추의 가동성을 높여 척추 정렬을 바로잡고, 감당 가능한 속도와 무게 범위 내에서만 관절을 제어하며 훈련해야 합니다.",
            "학생": "어깨는 척추 정렬이 무너진 상태에서 무거운 물건을 급하게 들거나 팔을 빠르게 휘두를 때 가장 쉽게 손상됩니다. 장시간 고개를 숙인 자세는 어깨 힘줄을 팽팽하게 긴장시켜, 기지개를 켜거나 가방을 멜 때의 작은 충격에도 염증을 유발할 수 있습니다. 독서대를 써서 목과 등을 바로 세우고, 굳어있는 어깨를 갑자기 쓰기 전에 충분히 돌려주는 예열 습관을 가지세요.",
            "주부/은퇴": "어깨는 척추 정렬이 무너진 상태에서 무거운 물건을 급하게 들거나 팔을 빠르게 휘두를 때 가장 쉽게 손상됩니다. 등이 굽은 자세로 높은 곳의 물건을 급히 꺼내거나 무거운 냄비를 확 들어 올리는 동작은 어깨 충돌 증후군의 주원인입니다. 허리와 가슴을 먼저 펴서 척추가 팔의 하중을 받쳐주게 하고, 모든 가사 노동은 반동 없이 부드럽게 움직이는 것이 중요합니다."
            },
        "무릎": {
            "사무직": "무릎은 허벅지 근육이 약해진 상태에서 갑작스러운 하중이 실리거나 방향을 틀 때 가장 쉽게 손상됩니다. 온종일 앉아 일하며 허벅지 힘이 빠진 상태에서 급하게 몸을 돌려 일어나거나 계단을 내려가는 동작은 무릎 연골판에 비틀리는 충격을 줍니다. 일어서기 전 무릎을 가볍게 움직여 예열하고, 방향을 바꿀 때는 발을 먼저 움직여 무릎이 뒤틀리지 않도록 주의하세요.",
            "현장직": "무릎은 허벅지 근육이 약해진 상태에서 갑작스러운 하중이 실리거나 방향을 틀 때 가장 쉽게 손상됩니다. 무거운 자재를 들고 발은 고정한 채 상체만 급하게 돌리는 동작은 무릎 인대 파열의 주원인입니다. 물건을 들 때는 발바닥 전체로 지면을 단단히 딛고, 방향을 전환할 때는 몸 전체가 함께 회전하도록 보폭을 조절해 무릎에 가해지는 회전 부하를 줄여야 합니다.",
            "운동선수": "무릎은 허벅지 근육이 약해진 상태에서 갑작스러운 하중이 실리거나 방향을 틀 때 가장 쉽게 손상됩니다. 30대 이후부터는 근육의 반응 속도가 떨어지므로, 급제동이나 급회전 시 무릎이 안쪽으로 꺾이지 않도록 둔근과 하체 정렬에 더욱 집중해야 합니다. 훈련 전후로 관절의 회전 가동 범위를 체크하고, 하체 근력이 뒷받침되지 않은 상태에서의 폭발적인 방향 전환은 지양하세요.",
            "학생": "무릎은 허벅지 근육이 약해진 상태에서 갑작스러운 하중이 실리거나 방향을 틀 때 가장 쉽게 손상됩니다. 근력이 떨어진 상태에서 무거운 가방을 메고 급하게 뛰거나 방향을 바꾸는 것은 무릎 앞쪽 관절에 과부하를 줍니다. 틈틈이 허벅지 근육을 강화하는 운동과 스트레칭을 하고, 이동 시에는 무릎에 무리가 가지 않도록 여유 있게 움직이는 습관을 갖는 것이 중요합니다.",
            "주부/은퇴": "무릎은 허벅지 근육이 약해진 상태에서 갑작스러운 하중이 실리거나 방향을 틀 때 가장 쉽게 손상됩니다. 허벅지 힘이 빠진 상태에서 급하게 몸을 돌려 일어나거나 계단을 내려가는 동작은 무릎 연골판에 비틀리는 충격을 줍니다. 무거운 것을 들 때는 항상 정면을 바라보고 천천히 움직이며, 평소 빠르게  걷기 운동을 통해 무릎을 대신해 무게를 버텨줄 허벅지 근육을 길러야 합니다."
            },
        "손목손가락": {
            "사무직": "손목과 손가락은 관절이 꺾인 상태에서 무거운 물건을 들거나 강한 힘으로 반복해서 쥘 때 가장 쉽게 손상됩니다. 30~40대는 힘줄의 탄력이 떨어지기 시작하므로, 손목이 위아래로 꺾인 채 장시간 스마트폰이나 키보드를 사용하면 신경이 눌려 만성적인 통증으로 이어집니다. 힘을 쓰기 전에는 반드시 손목을 수평으로 정렬하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주는 것이 중요합니다.",
            "현장직": "손목과 손가락은 관절이 꺾인 상태에서 무거운 물건을 들거나 강한 힘으로 반복해서 쥘 때 가장 쉽게 손상됩니다. 30~40대는 힘줄의 탄력이 떨어지기 시작하므로, 손목이 위아래로 꺾인 채 장시간 스마트폰이나 키보드를 사용하면 신경이 눌려 만성적인 통증으로 이어집니다. 힘을 쓰기 전에는 반드시 손목을 수평으로 정렬하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주는 것이 중요합니다.",
            "운동선수": "손목과 손가락은 관절이 꺾인 상태에서 무거운 물건을 들거나 강한 힘으로 반복해서 쥘 때 가장 쉽게 손상됩니다. 30~40대는 힘줄의 탄력이 떨어지기 시작하므로, 손목이 위아래로 꺾인 채 장시간 스마트폰이나 키보드를 사용하면 신경이 눌려 만성적인 통증으로 이어집니다. 힘을 쓰기 전에는 반드시 손목을 수평으로 정렬하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주는 것이 중요합니다.",
            "학생": "손목과 손가락은 관절이 꺾인 상태에서 무거운 물건을 들거나 강한 힘으로 반복해서 쥘 때 가장 쉽게 손상됩니다. 30~40대는 힘줄의 탄력이 떨어지기 시작하므로, 손목이 위아래로 꺾인 채 장시간 스마트폰이나 키보드를 사용하면 신경이 눌려 만성적인 통증으로 이어집니다. 힘을 쓰기 전에는 반드시 손목을 수평으로 정렬하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주는 것이 중요합니다.",
            "주부/은퇴": "손목과 손가락은 관절이 꺾인 상태에서 무거운 물건을 들거나 강한 힘으로 반복해서 쥘 때 가장 쉽게 손상됩니다. 30~40대는 힘줄의 탄력이 떨어지기 시작하므로, 손목이 위아래로 꺾인 채 장시간 스마트폰이나 키보드를 사용하면 신경이 눌려 만성적인 통증으로 이어집니다. 힘을 쓰기 전에는 반드시 손목을 수평으로 정렬하고, 틈틈이 손가락을 쫙 펴는 스트레칭으로 내부 압력을 낮춰주는 것이 중요합니다."
            },
        "발목발가락": {
            "사무직": "발목과 발가락은 늘어난 체중과 줄어든 유연성으로 인해 갑작스러운 방향 전환이나 지면 충격에 가장 취약해집니다. 30~40대부터는 아킬레스건이 뻣뻣해지기 시작하므로, 준비운동 없이 갑자기 뛰거나 불편한 신발을 신고 오래 걷는 것만으로도 족저근막염이나 염좌가 발생할 수 있습니다. 발목을 수시로 돌려 관절의 가동 범위를 확보하고, 발바닥 전체로 체중을 고르게 분산하여 걷는 습관을 들이세요.",
            "현장직": "발목과 발가락은 늘어난 체중과 줄어든 유연성으로 인해 갑작스러운 방향 전환이나 지면 충격에 가장 취약해집니다. 30~40대부터는 아킬레스건이 뻣뻣해지기 시작하므로, 준비운동 없이 갑자기 뛰거나 불편한 신발을 신고 오래 걷는 것만으로도 족저근막염이나 염좌가 발생할 수 있습니다. 발목을 수시로 돌려 관절의 가동 범위를 확보하고, 발바닥 전체로 체중을 고르게 분산하여 걷는 습관을 들이세요.",
            "운동선수": "발목과 발가락은 늘어난 체중과 줄어든 유연성으로 인해 갑작스러운 방향 전환이나 지면 충격에 가장 취약해집니다. 30~40대부터는 아킬레스건이 뻣뻣해지기 시작하므로, 준비운동 없이 갑자기 뛰거나 불편한 신발을 신고 오래 걷는 것만으로도 족저근막염이나 염좌가 발생할 수 있습니다. 발목을 수시로 돌려 관절의 가동 범위를 확보하고, 발바닥 전체로 체중을 고르게 분산하여 걷는 습관을 들이세요.",
            "학생": "발목과 발가락은 늘어난 체중과 줄어든 유연성으로 인해 갑작스러운 방향 전환이나 지면 충격에 가장 취약해집니다. 30~40대부터는 아킬레스건이 뻣뻣해지기 시작하므로, 준비운동 없이 갑자기 뛰거나 불편한 신발을 신고 오래 걷는 것만으로도 족저근막염이나 염좌가 발생할 수 있습니다. 발목을 수시로 돌려 관절의 가동 범위를 확보하고, 발바닥 전체로 체중을 고르게 분산하여 걷는 습관을 들이세요.",
            "주부/은퇴": "발목과 발가락은 늘어난 체중과 줄어든 유연성으로 인해 갑작스러운 방향 전환이나 지면 충격에 가장 취약해집니다. 30~40대부터는 아킬레스건이 뻣뻣해지기 시작하므로, 준비운동 없이 갑자기 뛰거나 불편한 신발을 신고 오래 걷는 것만으로도 족저근막염이나 염좌가 발생할 수 있습니다. 발목을 수시로 돌려 관절의 가동 범위를 확보하고, 발바닥 전체로 체중을 고르게 분산하여 걷는 습관을 들이세요."
            },
        "고관절": {
            "사무직": "고관절은 척추 정렬이 무너진 상태에서 갑자기 하중을 싣거나 다리를 비틀어 방향을 틀 때 가장 크게 손상됩니다. 장시간 앉아 지내며 고관절 주변 근육이 짧아진 상태에서 갑자기 일어나거나 무거운 짐을 드는 동작은 관절 내부의 연골판을 찝히게 만듭니다. 의자에서 일어날 때는 상체를 곧게 펴서 엉덩이 근육에 먼저 힘을 주고, 수시로 고관절 앞쪽 근육을 늘려주는 스트레칭이 필수적입니다.",
            "현장직": "고관절은 척추 정렬이 무너진 상태에서 갑자기 하중을 싣거나 다리를 비틀어 방향을 틀 때 가장 크게 손상됩니다. 무거운 물건을 든 채로 발은 고정하고 상체만 급하게 돌리는 동작은 고관절 비구순 파열의 주원인입니다. 물건을 들 때는 가슴을 펴 척추 정렬을 유지하고, 방향을 전환할 때는 반드시 발을 함께 움직여 고관절에 가해지는 회전 부하를 분산시켜야 합니다.",
            "운동선수": "고관절은 척추 정렬이 무너진 상태에서 갑자기 하중을 싣거나 다리를 비틀어 방향을 틀 때 가장 크게 손상됩니다. 30~40대는 고관절 가동 범위가 줄어들기 시작하므로, 무리하게 고중량을 다루거나 급격한 방향 전환 시 관절에 가해지는 충격을 근육이 다 흡수하지 못할 수 있습니다. 둔근의 활성화를 통해 관절을 단단히 지지하고, 훈련 전 흉추와 골반의 정렬을 맞추는 예열 과정에 집중하세요.",
            "학생": "고관절은 척추 정렬이 무너진 상태에서 갑자기 하중을 싣거나 다리를 비틀어 방향을 틀 때 가장 크게 손상됩니다.  장시간 다리를 꼬거나 구부정한 자세를 유지하면 골반이 틀어지며 고관절에 미세한 통증이 시작됩니다. 무거운 가방을 메고 급하게 계단을 오르내릴 때 관절에 과부하가 걸리지 않도록 턱을 당기고 허리를 세우는 올바른 보행 자세를 유지해야 합니다.",
            "주부/은퇴": "고관절은 척추 정렬이 무너진 상태에서 갑자기 하중을 싣거나 다리를 비틀어 방향을 틀 때 가장 크게 손상됩니다. 아이를 안거나 무거운 짐을 든 상태에서 갑자기 방향을 바꾸는 동작은 고관절에 수직 하중과 회전 부하를 동시에 주어 매우 위험합니다. 모든 가사 노동 시 허리와 가슴을 곧게 펴고, 무거운 물체는 몸에 최대한 붙여서 고관절이 받는 지렛대 압력을 줄여주는 것이 중요합니다."
            },
        "팔꿈치": {
            "사무직": "팔꿈치는 어깨와 손목의 정렬이 무너진 상태에서 무거운 물체를 들거나 손가락에 강한 힘을 반복해서 줄 때 손상됩니다. 키보드 사용 시 팔꿈치가 공중에 떠 있거나 어깨가 말려 있으면 팔꿈치 힘줄에 과도한 긴장이 유발되어 염증이 생기기 쉽습니다. 팔꿈치를 받침대에 고정해 어깨 하중을 분산하고, 마우스를 쥘 때 손가락의 힘을 빼서 팔꿈치로 이어지는 장력을 줄여주세요.",
            "현장직": "팔꿈치는 어깨와 손목의 정렬이 무너진 상태에서 무거운 물체를 들거나 손가락에 강한 힘을 반복해서 줄 때 손상됩니다. 등이 굽은 채로 무거운 도구를 사용하거나 반동을 주어 물건을 잡아채는 동작은 팔꿈치 힘줄 파열의 주원인입니다. 가슴을 펴서 어깨의 지지력을 확보하고, 무거운 것을 들 때는 손가락 끝의 힘보다는 전완근 전체와 몸의 반동을 줄인 절제된 힘을 사용해야 합니다.",
            "운동선수": "팔꿈치는 어깨와 손목의 정렬이 무너진 상태에서 무거운 물체를 들거나 손가락에 강한 힘을 반복해서 줄 때 손상됩니다. 30대 이후 선수는 어깨 가동성이 줄어들면 그 보상 작용으로 팔꿈치를 과하게 쓰게 되어 내외측 상과염이 빈번해집니다. 날개뼈의 안정성을 먼저 확보하여 팔꿈치로 가는 부하를 덜어주고, 라켓이나 바벨을 쥘 때 손목이 꺾이지 않도록 정렬에 각별히 유의하세요.",
            "학생": "팔꿈치는 어깨와 손목의 정렬이 무너진 상태에서 무거운 물체를 들거나 손가락에 강한 힘을 반복해서 줄 때 손상됩니다. 장시간 턱을 괴거나 책상에 팔꿈치를 딱딱하게 고정하고 공부하는 습관은 주변 신경을 압박해 팔 저림을 유발합니다. 독서대를 써서 척추를 바로 세우고, 필기 시에는 펜을 가볍게 쥐어 손가락에서 팔꿈치로 전달되는 누적 피로도를 최소화하는 것이 중요합니다.",
            "주부/은퇴": "팔꿈치는 어깨와 손목의 정렬이 무너진 상태에서 무거운 물체를 들거나 손가락에 강한 힘을 반복해서 줄 때 손상됩니다. 무거운 프라이팬을 한 손으로 들거나 빨래를 비틀어 짜는 등 손가락과 손목에 과한 힘을 주는 동작이 팔꿈치 통증의 시작입니다. 허리와 가슴을 펴서 팔 전체의 가동 범위를 넓히고, 무거운 물건은 두 손으로 나누어 들어 팔꿈치 인대에 가해지는 편중된 압력을 분산하세요."
            },
       "등/날개뼈": {
            "사무직": "등과 날개뼈는 척추 정렬이 무너진 상태에서 무거운 물건을 들거나 팔을 빠르게 뻗을 때 가장 쉽게 손상됩니다. 온종일 구부정한 자세로 일하면 날개뼈 주변 근육이 늘어나 약해지며, 이 상태에서 갑자기 힘을 쓰면 등에 '담'이 걸리는 급성 근막통증이 발생합니다. 모니터 높이를 눈높이에 맞추고, 수시로 날개뼈를 가운데로 모아 등을 펴주는 동작으로 척추의 지지력을 회복해야 합니다.",
            "현장직": "등과 날개뼈는 척추 정렬이 무너진 상태에서 무거운 물건을 들거나 팔을 빠르게 뻗을 때 가장 쉽게 손상됩니다. 등이 굽은 채로 무거운 자재를 반동을 주어 잡아채면 그 충격이 척추 마디마디와 날개뼈 인대에 고스란히 전달됩니다. 무거운 것을 들기 전 반드시 가슴을 펴서 등을 곧게 세우고, 팔의 힘보다는 날개뼈를 몸 뒤쪽으로 단단히 고정하는 힘을 먼저 사용하세요.",
            "운동선수": "등과 날개뼈는 척추 정렬이 무너진 상태에서 무거운 물건을 들거나 팔을 빠르게 뻗을 때 가장 쉽게 손상됩니다.  흉추(등뼈)의 가동성이 떨어지면 어깨와 허리에 과부하가 집중되어 치명적인 부상으로 이어집니다. 훈련 전 흉추를 회전시키는 예열 운동을 통해 정렬을 바로잡고, 날개뼈가 흔들리지 않도록 등 근육의 안정성을 확보한 상태에서 폭발적인 힘을 써야 합니다.",
            "학생": "등과 날개뼈는 척추 정렬이 무너진 상태에서 무거운 물건을 들거나 팔을 빠르게 뻗을 때 가장 쉽게 손상됩니다. 장시간 고개를 숙이고 공부하면 등이 둥글게 말리면서 날개뼈 사이 근육이 만성적으로 긴장하게 됩니다. 이 상태에서 무거운 가방을 갑자기 메거나 상체를 비틀면 통증이 심해지므로, 독서대를 활용해 척추 정렬을 세우고 틈틈이 기지개를 켜서 등 근육의 혈액순환을 도와주세요.",
            "주부/은퇴": "등과 날개뼈는 척추 정렬이 무너진 상태에서 무거운 물건을 들거나 팔을 빠르게 뻗을 때 가장 쉽게 손상됩니다. 등이 굽은 채로 아이를 안거나 무거운 빨래 바구니를 확 들어 올리는 동작은 날개뼈 주변 인대에 미세 손상을 누적시킵니다. 가사 노동 중에도 의식적으로 턱을 당기고 가슴을 펴서 등을 평평하게 유지하며, 물건을 들 때는 팔을 멀리 뻗기보다 몸쪽으로 바짝 붙여 등의 부담을 덜어주세요."
            }
    },
    "50~60대": {
        "목": {
        "사무직": "척추 전체의 정렬이 무너진 상태에서 억지로 목의 C커브만 만들려고 뒤로 꺾는 동작이 오히려 디스크 압박을 높여 신경을 건드릴 수 있습니다. 굽은 등을 먼저 펴고 턱을 가볍게 당겨 척추의 기초 정렬부터 바로잡는 것이 가장 안전한 관리법입니다. 모니터를 볼 때는 고개가 앞으로 쏠리지 않도록 높이를 조절하여 목 뼈 사이의 공간을 확보해 주는 것이 중요합니다.",
        "현장직": "척추 전체의 정렬이 무너진 상태에서 억지로 목의 C커브만 만들려고 뒤로 꺾는 동작이 오히려 디스크 압박을 높여 신경을 건드릴 수 있습니다. 무거운 장비를 들기 전 반드시 가슴을 펴서 전체 정렬을 맞추는 것이 우선이며, 고개를 위로 과하게 젖히는 작업은 피하여 경추 신경의 통로가 좁아지지 않도록 주의해야 합니다.",
        "운동선수": "척추 전체의 정렬이 무너진 상태에서 억지로 목의 C커브만 만들려고 뒤로 꺾는 동작이 오히려 디스크 압박을 높여 신경을 건드릴 수 있습니다. 취미 운동 전에는 흉추(등)의 가동성을 충분히 확보하여 전체적인 척추 정렬을 바로잡는 예열 과정에 집중하세요. 기초 정렬이 바로 서야 목 디스크가 보상 작용으로 눌리는 부상을 막을 수 있습니다.",
        "학생": "척추 전체의 정렬이 무너진 상태에서 억지로 목의 C커브만 만들려고 뒤로 꺾는 동작이 오히려 디스크 압박을 높여 신경을 건드릴 수 있습니다. 굽은 등을 먼저 펴고 턱을 가볍게 당겨 척추의 기초 정렬부터 바로잡는 것이 가장 안전한 관리법입니다. 독서대를 사용하여 고개가 숙여지지 않게 하고, 목 뼈 사이의 신경 통로가 눌리지 않는 환경을 만들어주세요.",
        "주부/은퇴": "척추 전체의 정렬이 무너진 상태에서 억지로 목의 C커브만 만들려고 뒤로 꺾는 동작이 오히려 디스크 압박을 높여 신경을 건드릴 수 있습니다. 가사 노동 시 턱을 당기고 가슴을 펴서 등과 목이 조화롭게 이어지는 정렬을 만드는 것이 무엇보다 중요합니다. 무거운 물건을 들 때도 억지로 목을 쓰기보다 전체 척추의 지지력을 활용해 디스크의 부담을 덜어주세요."
        },
       "허리": {
        "사무직": " 허리를 숙여 머리를 감거나 바닥의 물건을 주울 때처럼 일상적인 동작에서 허리 디스크가 가장 큰 압박을 받아 손상되기 쉽습니다. 특히 등이 굽은 상태에서 억지로 허리의 곡선만 만들려고 뒤로 꺾는 동작은 오히려 척추관을 자극해 통증을 유발할 수 있습니다. 의자에 앉을 때는 엉덩이를 깊숙이 넣고 가슴을 펴서 척추 전체의 정렬을 바로잡는 것이 디스크를 보호하는 가장 확실한 방법입니다.",
        "현장직": "허리를 숙여 머리를 감거나 바닥의 물건을 주울 때처럼 일상적인 동작에서 허리 디스크가 가장 큰 압박을 받아 손상되기 쉽습니다. 등이 구부정한 자세로 무거운 짐을 들어 올리는 반동은 디스크에 치명적인 파열을 일으킬 수 있습니다. 물건을 들기 전 반드시 무릎을 굽히고 가슴을 펴서 척추 정렬을 맞춘 뒤, 허리가 아닌 하체의 힘을 활용해야 디스크의 내부 압력을 낮출 수 있습니다.",
        "운동선수": "허리를 숙여 머리를 감거나 바닥의 물건을 주울 때처럼 일상적인 동작에서 허리 디스크가 가장 큰 압박을 받아 손상되기 쉽습니다. 준비되지 않은 상태에서 허리를 과하게 숙이거나 회전하는 동작은 디스크 탈출의 주원인이 됩니다. 척추 전체의 정렬을 먼저 바로잡고 고관절의 유연성을 확보한 뒤, 허리의 자연스러운 곡선이 유지되는 범위 내에서만 부드럽게 움직이는 것이 필수입니다.",
        "학생": "허리를 숙여 머리를 감거나 바닥의 물건을 주울 때처럼 일상적인 동작에서 허리 디스크가 가장 큰 압박을 받아 손상되기 쉽습니다. 특히 등이 굽은 상태에서 억지로 허리의 곡선만 만들려고 뒤로 꺾는 동작은 오히려 척추관을 자극해 통증을 유발할 수 있습니다. 평소 가슴을 펴서 척추 전체의 정렬을 바로잡고, 고개를 숙여 책을 보는 시간을 줄여 허리 마디마디에 쌓이는 하중을 관리해 주어야 합니다.",
        "주부/은퇴": "허리를 숙여 머리를 감거나 바닥의 물건을 주울 때처럼 일상적인 동작에서 허리 디스크가 가장 큰 압박을 받아 손상되기 쉽습니다. 쪼그려 앉거나 허리만 숙여서 바닥의 물건을 집는 습관은 디스크를 뒤로 밀어내는 가장 위험한 행동입니다. 가사 노동 중에도 수시로 가슴을 펴 척추 정렬을 세우고, 무거운 것을 들 때는 몸에 바짝 붙여 허리 디스크가 받는 무게 부담을 최소화하세요."
        },
        "어깨": {
        "사무직": "어깨는 거북목이나 어깨가 앞쪽으로 말린 자세에서 높은 곳의 물건을 내리거나 무거운 짐을 들어 올릴 때 가장 쉽게 손상됩니다. 특히 노화로 탄력을 잃은 힘줄이 말린 어깨 때문에 좁아진 뼈 사이에서 반복적으로 충돌하면 손상과 파열이 가속화됩니다. 굽은 등을 먼저 펴서 어깨가 움직일 수 있는 공간을 충분히 확보한 뒤 팔을 사용해야 하며, 평소에도 의식적으로 어깨를 뒤로 열어주는 정렬이 필수입니다.",
        "현장직": "어깨는 거북목이나 어깨가 앞쪽으로 말린 자세에서 높은 곳의 물건을 내리거나 무거운 짐을 들어 올릴 때 가장 쉽게 손상됩니다. 오랜 작업으로 마모된 힘줄은 말린 어깨 자세에서 과도한 무게를 버틸 때 비정상적인 마찰을 일으키며 파열로 이어지기 쉽습니다. 물건을 들기 전 반드시 가슴을 펴서 어깨 정렬을 바로잡아야 하며, 머리 위로 팔을 뻗는 동작은 어깨가 찝히지 않도록 하체와 몸통의 힘을 함께 활용해야 합니다.",
        "운동선수": "어깨는 거북목이나 어깨가 앞쪽으로 말린 자세에서 높은 곳의 물건을 내리거나 무거운 짐을 들어 올릴 때 가장 쉽게 손상됩니다. 취미 운동 시에도 말린 어깨 상태에서 갑자기 중량을 다루면, 퇴행이 시작된 관절 내 조직들이 서로 충돌하며 만성 염증을 유발합니다. 운동 전 흉추를 열어 어깨 정렬을 바로잡는 예열 과정이 반드시 선행되어야만 어깨 힘줄에 가해지는 과도한 부하를 막을 수 있습니다.",
        "학생": "어깨는 거북목이나 어깨가 앞쪽으로 말린 자세에서 높은 곳의 물건을 내리거나 무거운 짐을 들어 올릴 때 가장 쉽게 손상됩니다. 장시간 고개를 숙인 거북목 자세는 어깨 주변 근육을 딱딱하게 굳게 만들고 노화를 앞당겨 미세한 충격에도 쉽게 통증을 일으킵니다. 평소 독서대를 활용해 턱을 당기고 어깨를 펴는 정렬 습관을 들이고, 무거운 가방을 멜 때도 날개뼈를 뒤로 모아 어깨 관절 내부의 압력을 낮춰주는 것이 중요합니다.",
        "주부/은퇴": "어깨는 거북목이나 어깨가 앞쪽으로 말린 자세에서 높은 곳의 물건을 내리거나 무거운 짐을 들어 올릴 때 가장 쉽게 손상됩니다. 퇴행성 변화가 진행된 상태에서 어깨가 말린 채로 높은 찬장의 그릇을 꺼내거나 무거운 냄비를 들면 힘줄이 가위질하듯 찝히며 파열될 수 있습니다. 등을 곧게 펴서 어깨 공간을 확보한 상태에서 부드럽게 움직여야 하며, 모든 가사 노동 시 어깨가 으쓱 올라가지 않도록 날개뼈를 아래로 안정시킨 뒤 움직이세요."
        },
        "무릎": {
        "사무직": "무릎은 근육이 빠진 상태에서 쪼그려 앉거나, 고관절과 발목이 뻣뻣한 상태에서 빠른 방향 전환을 할 때 가장 큰 무리가 갑니다. 특히 장시간 앉아 지내며 엉덩이 근육이 약해지면 계단을 오르내릴 때 연골이 받는 충격이 그대로 관절에 전달됩니다. 평소 고관절 스트레칭으로 하체 가동성을 확보하고, 의자에서 일어날 때 하체 근육의 지지력을 활용해 무릎으로 쏠리는 체중 하중을 분산해야 합니다.",
        "현장직": "무릎은 근육이 빠진 상태에서 쪼그려 앉거나, 고관절과 발목이 뻣뻣한 상태에서 빠른 방향 전환을 할 때 가장 큰 무리가 갑니다. 무거운 짐을 든 채로 발바닥을 고정한 채 몸만 급하게 돌리는 동작은 퇴행된 연골에 치명적인 손상을 입힙니다. 작업 전 하체 근육을 예열하고, 방향을 바꿀 때는 무릎만 비틀지 말고 발을 함께 움직여 고관절과 발목이 부하를 나누어 갖도록 해야 합니다.",
        "운동선수": "무릎은 근육이 빠진 상태에서 쪼그려 앉거나, 고관절과 발목이 뻣뻣한 상태에서 빠른 방향 전환을 할 때 가장 큰 무리가 갑니다. 운동 시 고관절의 가동성이 떨어져 있으면 급격한 감속이나 회전 시 무릎이 모든 비틀림을 감당하며 인대와 연골이 손상됩니다. 하체 근력을 유지하여 관절의 안정성을 높이고, 인접 관절의 유연성을 확보하여 무릎이 보상 작용으로 혹사당하지 않게 관리하세요.",
        "학생": "무릎은 근육이 빠진 상태에서 쪼그려 앉거나, 고관절과 발목이 뻣뻣한 상태에서 빠른 방향 전환을 할 때 가장 큰 무리가 갑니다. 활동량 부족으로 허벅지 근육이 줄어들면 무릎 관절을 잡아주는 힘이 약해져 일상적인 보행 중에도 연골 마모가 빨라질 수 있습니다. 틈틈이 제자리 걷기나 스트레칭을 통해 하체 유연성을 관리하고, 근육이 관절의 완충 역할을 대신할 수 있는 환경을 만들어주어야 합니다.",
        "주부/은퇴": "무릎은 근육이 빠진 상태에서 쪼그려 앉거나, 고관절과 발목이 뻣뻣한 상태에서 빠른 방향 전환을 할 때 가장 큰 무리가 갑니다. 특히 바닥에 쪼그려 앉아 집안일을 하거나 허리만 숙여 물건을 집는 동작은 좁아진 무릎 뼈 사이 연골을 강하게 압박합니다. 가급적 의자 생활을 하고 하체(허벅지) 근력을 보존하여, 관절이 직접 체중을 버티기보다 근육이 무게를 지탱할 수 있게 습관을 바꿔야 합니다."
        },
        "손목손가락": {
        "사무직": "손목과 손가락은 퇴행으로 힘줄이 얇아진 상태에서 손목이 꺾인 채 힘을 쓰거나 특정 마디에만 하중이 집중될 때 가장 쉽게 손상됩니다. 특히 팔꿈치와 손목의 유연성이 떨어진 상태에서 억지로 손바닥을 뒤집거나 돌리는 동작(회내/회외)을 반복하면, 그 부하가 손목 관절과 팔꿈치 힘줄에 집중되어 만성 염증을 유발합니다. 물건을 들거나 돌릴 때는 손바닥 전체를 활용해 무게를 분산하고, 전완부 근육을 부드럽게 이완하여 손목과 팔꿈치의 정렬을 보호해야 합니다.",
        "현장직": "손목과 손가락은 퇴행으로 힘줄이 얇아진 상태에서 손목이 꺾인 채 힘을 쓰거나 특정 마디에만 하중이 집중될 때 가장 쉽게 손상됩니다. 특히 팔꿈치와 손목의 유연성이 떨어진 상태에서 억지로 손바닥을 뒤집거나 돌리는 동작(회내/회외)을 반복하면, 그 부하가 손목 관절과 팔꿈치 힘줄에 집중되어 만성 염증을 유발합니다. 물건을 들거나 돌릴 때는 손바닥 전체를 활용해 무게를 분산하고, 전완부 근육을 부드럽게 이완하여 손목과 팔꿈치의 정렬을 보호해야 합니다.",
        "운동선수": "손목과 손가락은 퇴행으로 힘줄이 얇아진 상태에서 손목이 꺾인 채 힘을 쓰거나 특정 마디에만 하중이 집중될 때 가장 쉽게 손상됩니다. 특히 팔꿈치와 손목의 유연성이 떨어진 상태에서 억지로 손바닥을 뒤집거나 돌리는 동작(회내/회외)을 반복하면, 그 부하가 손목 관절과 팔꿈치 힘줄에 집중되어 만성 염증을 유발합니다. 물건을 들거나 돌릴 때는 손바닥 전체를 활용해 무게를 분산하고, 전완부 근육을 부드럽게 이완하여 손목과 팔꿈치의 정렬을 보호해야 합니다.",
        "학생": "손목과 손가락은 퇴행으로 힘줄이 얇아진 상태에서 손목이 꺾인 채 힘을 쓰거나 특정 마디에만 하중이 집중될 때 가장 쉽게 손상됩니다. 특히 팔꿈치와 손목의 유연성이 떨어진 상태에서 억지로 손바닥을 뒤집거나 돌리는 동작(회내/회외)을 반복하면, 그 부하가 손목 관절과 팔꿈치 힘줄에 집중되어 만성 염증을 유발합니다. 물건을 들거나 돌릴 때는 손바닥 전체를 활용해 무게를 분산하고, 전완부 근육을 부드럽게 이완하여 손목과 팔꿈치의 정렬을 보호해야 합니다.",
        "주부/은퇴": "손목과 손가락은 퇴행으로 힘줄이 얇아진 상태에서 손목이 꺾인 채 힘을 쓰거나 특정 마디에만 하중이 집중될 때 가장 쉽게 손상됩니다. 특히 팔꿈치와 손목의 유연성이 떨어진 상태에서 억지로 손바닥을 뒤집거나 돌리는 동작(회내/회외)을 반복하면, 그 부하가 손목 관절과 팔꿈치 힘줄에 집중되어 만성 염증을 유발합니다. 물건을 들거나 돌릴 때는 손바닥 전체를 활용해 무게를 분산하고, 전완부 근육을 부드럽게 이완하여 손목과 팔꿈치의 정렬을 보호해야 합니다."
        },
        "발목발가락": {
        "사무직": "발목과 발가락은 고관절과 무릎이 뻣뻣하게 굳어 있을 때 그 비틀림을 대신 감당하며 가장 큰 무리가 갑니다. 특히 하체 근육이 빠진 상태에서는 작은 충격에도 균형을 잃고 넘어지면서 발목 인대가 늘어나거나 파열되는 사고가 빈번하게 발생합니다. 평소 종아리와 허벅지 근육을 길러 발목이 받는 부하를 근육이 대신 흡수하게 만들고, 유연성을 관리하여 낙상 사고로부터 관절을 안전하게 보호해야 합니다.",
        "현장직": "발목과 발가락은 고관절과 무릎이 뻣뻣하게 굳어 있을 때 그 비틀림을 대신 감당하며 가장 큰 무리가 갑니다. 특히 하체 근육이 빠진 상태에서는 작은 충격에도 균형을 잃고 넘어지면서 발목 인대가 늘어나거나 파열되는 사고가 빈번하게 발생합니다. 평소 종아리와 허벅지 근육을 길러 발목이 받는 부하를 근육이 대신 흡수하게 만들고, 유연성을 관리하여 낙상 사고로부터 관절을 안전하게 보호해야 합니다.",
        "운동선수": "발목과 발가락은 고관절과 무릎이 뻣뻣하게 굳어 있을 때 그 비틀림을 대신 감당하며 가장 큰 무리가 갑니다. 특히 하체 근육이 빠진 상태에서는 작은 충격에도 균형을 잃고 넘어지면서 발목 인대가 늘어나거나 파열되는 사고가 빈번하게 발생합니다. 평소 종아리와 허벅지 근육을 길러 발목이 받는 부하를 근육이 대신 흡수하게 만들고, 유연성을 관리하여 낙상 사고로부터 관절을 안전하게 보호해야 합니다.",
        "학생": "발목과 발가락은 고관절과 무릎이 뻣뻣하게 굳어 있을 때 그 비틀림을 대신 감당하며 가장 큰 무리가 갑니다. 특히 하체 근육이 빠진 상태에서는 작은 충격에도 균형을 잃고 넘어지면서 발목 인대가 늘어나거나 파열되는 사고가 빈번하게 발생합니다. 평소 종아리와 허벅지 근육을 길러 발목이 받는 부하를 근육이 대신 흡수하게 만들고, 유연성을 관리하여 낙상 사고로부터 관절을 안전하게 보호해야 합니다.",
        "주부/은퇴": "발목과 발가락은 고관절과 무릎이 뻣뻣하게 굳어 있을 때 그 비틀림을 대신 감당하며 가장 큰 무리가 갑니다. 특히 하체 근육이 빠진 상태에서는 작은 충격에도 균형을 잃고 넘어지면서 발목 인대가 늘어나거나 파열되는 사고가 빈번하게 발생합니다. 평소 종아리와 허벅지 근육을 길러 발목이 받는 부하를 근육이 대신 흡수하게 만들고, 유연성을 관리하여 낙상 사고로부터 관절을 안전하게 보호해야 합니다."
        },
        "고관절": {
        "사무직": "고관절은 엉덩이 근육이 빠지고 주변 관절이 뻣뻣하게 굳은 상태에서 갑자기 다리를 벌리거나 체중을 실어 회전할 때 가장 큰 무리가 갑니다. 특히 장시간 앉아 있는 습관으로 고관절 앞쪽 근육이 짧아지면 허리와 무릎에 비정상적인 부하가 집중됩니다. 평소 엉덩이 근육을 길러 관절이 받는 하중을 흡수하게 만들고, 틈틈이 자리에서 일어나 고관절 주변을 스트레칭하여 가동 범위를 확보해야 합니다.",
        "현장직": "고관절은 엉덩이 근육이 빠지고 주변 관절이 뻣뻣하게 굳은 상태에서 갑자기 다리를 벌리거나 체중을 실어 회전할 때 가장 큰 무리가 갑니다. 무거운 물건을 든 채로 뻣뻣해진 고관절을 무리하게 비틀면 연골 마모와 통증이 가속화되므로 주의가 필요합니다. 엉덩이와 허벅지 근육의 지지력을 길러 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 작업 전 충분한 예열을 통해 관절의 마찰을 최소화해야 합니다.",
        "운동선수": "고관절은 엉덩이 근육이 빠지고 주변 관절이 뻣뻣하게 굳은 상태에서 갑자기 다리를 벌리거나 체중을 실어 회전할 때 가장 큰 무리가 갑니다. 퇴행으로 유연성과 근력이 떨어진 상태에서 슈팅이나 과도한 체중지지 동작을 반복하면 고관절 충돌 증후군이나 비구순 파열로 이어질 수 있습니다. 강한 근력으로 부하를 흡수하는 것만큼이나 고관절의 유연한 회전 정렬을 확보하여 인접 관절인 허리와 무릎을 보호하는 것이 중요합니다.",
        "학생": "고관절은 엉덩이 근육이 빠지고 주변 관절이 뻣뻣하게 굳은 상태에서 갑자기 다리를 벌리거나 체중을 실어 회전할 때 가장 큰 무리가 갑니다. 오랜 시간 고정된 자세로 앉아 있으면 고관절 주변 혈액순환이 저하되고 관절이 굳어 노화가 빨라집니다. 평소 하체 근력을 길러 하중을 흡수할 수 있는 힘을 키우고, 의식적으로 자세를 바꿔가며 고관절이 한 방향으로만 압박받지 않도록 관리해야 합니다.",
        "주부/은퇴": "고관절은 엉덩이 근육이 빠지고 주변 관절이 뻣뻣하게 굳은 상태에서 갑자기 다리를 벌리거나 체중을 실어 회전할 때 가장 큰 무리가 갑니다. 특히 쪼그려 앉거나 허리만 숙여 물건을 집는 동작은 퇴행된 고관절에 극심한 압박을 주어 연골 손상을 유발합니다. 엉덩이 근육을 보존하여 하중을 대신 지탱하게 하고, 가급적 의자 생활을 하며 고관절이 과도하게 꺾이지 않도록 부드럽게 움직여야 합니다."
        },
        "팔꿈치": {
        "사무직": "팔꿈치는 전완부 근육이 긴장된 상태에서 손목을 과하게 꺾거나 반복적인 미세 동작을 할 때 힘줄에 무리가 갑니다. 특히 장시간 마우스 사용이나 키보드 타이핑, 무리하게 캔 뚜껑을 여는 동작처럼 손가락 끝의 힘이 팔꿈치 안팎의 힘줄에 반복적으로 전달될 때 염증이 발생하기 쉽습니다. 평소 팔뚝 근육을 부드럽게 이완하여 힘줄에 가해지는 부하를 흡수하게 만들고, 작업 시 팔꿈치가 자연스러운 각도를 유지하도록 정렬을 맞춰야 합니다.",
        "현장직": "팔꿈치는 전완부 근육이 긴장된 상태에서 무거운 도구를 쥐고 손바닥을 뒤집거나 비트는 동작을 반복할 때 가장 큰 무리가 갑니다. 수건을 짜듯 전완부를 강하게 회전시키거나 반동을 이용해 무거운 짐을 드는 동작은 퇴행으로 약해진 힘줄에 미세 파열을 일으키는 주원인이 됩니다. 팔 전체의 힘보다는 어깨와 몸통의 힘을 함께 사용하여 팔꿈치에 집중되는 부하를 분산하고, 작업 전후로 팔뚝 근육을 충분히 풀어주어야 합니다.",
        "운동선수": "팔꿈치는 전완부 근육이 긴장된 상태에서 손목 정렬이 깨진 채 강력한 휘두르기나 중량운동을 할 때 힘줄에 치명적인 손상을 입습니다. 테니스(외상과염)나 골프(내상과염)처럼 반복적인 회전 부하가 가해질 때, 근육이 충격을 흡수하지 못하면 그 에너지가 고스란히 뼈와 힘줄에 전달됩니다. 전신 정렬을 바로잡아 팔꿈치 한 지점에만 과도한 회전 부하가 걸리지 않도록 관리하고 근력과 유연성을 길러 충격을 완충하는 것이 필수입니다.",
        "학생": "팔꿈치는 전완부 근육이 긴장된 상태에서 손목을 과하게 꺾거나 반복적인 미세 동작을 할 때 힘줄에 무리가 갑니다. 특히 장시간 마우스 사용이나 키보드 타이핑, 무리하게 캔 뚜껑을 여는 동작처럼 손가락 끝의 힘이 팔꿈치 안팎의 힘줄에 반복적으로 전달될 때 염증이 발생하기 쉽습니다. 평소 팔뚝 근육을 부드럽게 이완하여 힘줄에 가해지는 부하를 흡수하게 만들고, 작업 시 팔꿈치가 자연스러운 각도를 유지하도록 정렬을 맞춰야 합니다.",
        "주부/은퇴": "팔꿈치는 전완부 근육이 긴장된 상태에서 무거운 냄비를 들거나 수건을 짜는 등 손목을 비트는 동작을 반복할 때 가장 큰 무리가 갑니다. 퇴행으로 약해진 힘줄은 캔 뚜껑을 억지로 열거나 손목만 사용해 물건을 집어 올릴 때 발생하는 급격한 하중을 흡수하지 못하고 만성 염증으로 이어집니다. 모든 동작 시 손바닥 전체를 사용해 부하를 분산하고, 팔꿈치가 몸통에서 멀어지지 않게 정렬하여 관절의 지렛대 압력을 줄여야 합니다."
        },
        "등/날개뼈": {
        "사무직": "등과 날개뼈는 장시간 구부정한 자세로 인해 등 근육이 늘어지고 날개뼈 주변 정렬이 무너질 때 심한 방사통과 결림이 발생합니다. 등이 굽으면 날개뼈가 앞으로 말리면서 목과 어깨의 통증을 유발하므로, 억지로 허리를 펴기보다 늘어진 등 근육의 탄력을 회복해 날개뼈를 바르게 고정하는 것이 우선입니다. 평소 등 근육을 길러 상체의 하중을 견고하게 지탱하고, 가슴 근육을 이완하여 날개뼈가 등 뒤에 안정적으로 밀착될 수 있게 관리해야 합니다.",
        "현장직": "등과 날개뼈는 상체 근력이 부족한 상태에서 무거운 물건을 반복적으로 들거나 한쪽으로만 힘을 쓸 때 날개뼈 주변 근육에 과부하가 걸리며 통증이 생깁니다. 날개뼈를 잡아주는 근육이 약해지면 그 부담이 척추 마디마디로 전달되어 등 전체가 뻣뻣해지고 담에 걸리기 쉬운 상태가 됩니다. 날개뼈 주변 근육을 강화하여 등 뒤에서 가해지는 충격을 흡수하게 만들고, 작업 중 틈틈이 날개뼈를 모아주는 동작을 통해 정렬을 바로잡아야 합니다.",
        "운동선수": "등과 날개뼈는 견갑골의 가동성이 제한된 상태에서 무리하게 팔을 휘두르거나 고중량을 다룰 때 주변 힘줄과 근육에 미세 파열을 일으킵니다. 날개뼈가 상체의 움직임을 충분히 보조하지 못하면 어깨 관절에 과도한 회전 부하가 걸려 치명적인 부상으로 이어집니다. 등 근육을 길러 강력한 지지력을 확보하는 동시에 날개뼈의 부드러운 움직임을 확보하여, 상체에서 발생하는 에너지가 특정 관절에 쏠리지 않고 분산되도록 관리해야 합니다.",
        "학생": "등과 날개뼈는 장시간 구부정한 자세로 인해 등 근육이 늘어지고 날개뼈 주변 정렬이 무너질 때 심한 방사통과 결림이 발생합니다. 등이 굽으면 날개뼈가 앞으로 말리면서 목과 어깨의 통증을 유발하므로, 억지로 허리를 펴기보다 늘어진 등 근육의 탄력을 회복해 날개뼈를 바르게 고정하는 것이 우선입니다. 평소 등 근육을 길러 상체의 하중을 견고하게 지탱하고, 가슴 근육을 이완하여 날개뼈가 등 뒤에 안정적으로 밀착될 수 있게 관리해야 합니다.",
        "주부/은퇴": "등과 날개뼈는 등 근육이 빠지면서 날개뼈를 지탱하는 힘이 약해지고, 가슴이 안으로 말리는 '라운드 숄더'가 진행될 때 통증이 심해집니다. 날개뼈 주변이 굳으면 팔을 높이 들거나 뒤로 뻗는 동작에서 어깨가 비정상적으로 압박받아 연골 손상을 초래합니다. 평소 등과 날개뼈 주변 근육을 길러 부하를 흡수할 수 있는 바탕을 만들고, 의식적으로 가슴을 펴 날개뼈가 등 중앙으로 모일 수 있는 환경을 만들어주어야 합니다."
        }
    },
    "70대 이상": {
       "목": {
        "사무직": "70대 이상의 목은 수십 년간의 퇴행으로 뼈 사이가 좁아진 상태이므로, 관절이 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 무엇보다 중요합니다. 구부정한 등은 목을 앞으로 빠지게 해 신경 압박을 심화시키므로, 평소 등을 곧게 펴서 머리의 무게가 경추 마디마디에 골고루 분산되도록 정렬을 바로잡아야 합니다. 주변 근육을 길러 이 바른 정렬을 스스로 버틸 수 있는 힘을 만들고, 고개를 갑자기 돌리거나 젖히는 동작 대신 몸 전체를 함께 움직여 관절을 보호하세요.",
        "현장직": "70대 이상의 목은 수십 년간의 퇴행으로 뼈 사이가 좁아진 상태이므로, 관절이 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 무엇보다 중요합니다. 구부정한 등은 목을 앞으로 빠지게 해 신경 압박을 심화시키므로, 평소 등을 곧게 펴서 머리의 무게가 경추 마디마디에 골고루 분산되도록 정렬을 바로잡아야 합니다. 주변 근육을 길러 이 바른 정렬을 스스로 버틸 수 있는 힘을 만들고, 고개를 갑자기 돌리거나 젖히는 동작 대신 몸 전체를 함께 움직여 관절을 보호하세요.",
        "운동선수": "70대 이상의 목은 수십 년간의 퇴행으로 뼈 사이가 좁아진 상태이므로, 관절이 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 무엇보다 중요합니다. 구부정한 등은 목을 앞으로 빠지게 해 신경 압박을 심화시키므로, 평소 등을 곧게 펴서 머리의 무게가 경추 마디마디에 골고루 분산되도록 정렬을 바로잡아야 합니다. 주변 근육을 길러 이 바른 정렬을 스스로 버틸 수 있는 힘을 만들고, 고개를 갑자기 돌리거나 젖히는 동작 대신 몸 전체를 함께 움직여 관절을 보호하세요.",
        "학생": "70대 이상의 목은 수십 년간의 퇴행으로 뼈 사이가 좁아진 상태이므로, 관절이 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 무엇보다 중요합니다. 구부정한 등은 목을 앞으로 빠지게 해 신경 압박을 심화시키므로, 평소 등을 곧게 펴서 머리의 무게가 경추 마디마디에 골고루 분산되도록 정렬을 바로잡아야 합니다. 주변 근육을 길러 이 바른 정렬을 스스로 버틸 수 있는 힘을 만들고, 고개를 갑자기 돌리거나 젖히는 동작 대신 몸 전체를 함께 움직여 관절을 보호하세요.",
        "주부/은퇴": "70대 이상의 목은 수십 년간의 퇴행으로 뼈 사이가 좁아진 상태이므로, 관절이 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 무엇보다 중요합니다. 구부정한 등은 목을 앞으로 빠지게 해 신경 압박을 심화시키므로, 평소 등을 곧게 펴서 머리의 무게가 경추 마디마디에 골고루 분산되도록 정렬을 바로잡아야 합니다. 주변 근육을 길러 이 바른 정렬을 스스로 버틸 수 있는 힘을 만들고, 고개를 갑자기 돌리거나 젖히는 동작 대신 몸 전체를 함께 움직여 관절을 보호하세요."
        },
        "허리": {
        "사무직": "70대 이상의 허리는 척추 마디 사이가 좁아지고 퇴행이 진행된 상태이므로, 척추가 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 가장 중요합니다. 허리를 구부정하게 숙이는 습관은 하중을 척추 뼈로 집중시켜 통증을 악화시키므로, 평소 등을 곧게 펴서 척추의 자연스러운 곡선을 유지해야 합니다. 특히 '누워서 엉덩이 들기(브릿지)'와 같은 운동으로 엉덩이 근육을 길러 허리가 받는 부하를 대신 흡수하게 만들고, 갑자기 허리를 비트는 동작을 피하여 관절을 보호해야 합니다.",
        "현장직": "70대 이상의 허리는 척추 마디 사이가 좁아지고 퇴행이 진행된 상태이므로, 척추가 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 가장 중요합니다. 허리를 구부정하게 숙이는 습관은 하중을 척추 뼈로 집중시켜 통증을 악화시키므로, 평소 등을 곧게 펴서 척추의 자연스러운 곡선을 유지해야 합니다. 특히 '누워서 엉덩이 들기(브릿지)'와 같은 운동으로 엉덩이 근육을 길러 허리가 받는 부하를 대신 흡수하게 만들고, 갑자기 허리를 비트는 동작을 피하여 관절을 보호해야 합니다.",
        "운동선수": "70대 이상의 허리는 척추 마디 사이가 좁아지고 퇴행이 진행된 상태이므로, 척추가 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 가장 중요합니다. 허리를 구부정하게 숙이는 습관은 하중을 척추 뼈로 집중시켜 통증을 악화시키므로, 평소 등을 곧게 펴서 척추의 자연스러운 곡선을 유지해야 합니다. 특히 '누워서 엉덩이 들기(브릿지)'와 같은 운동으로 엉덩이 근육을 길러 허리가 받는 부하를 대신 흡수하게 만들고, 갑자기 허리를 비트는 동작을 피하여 관절을 보호해야 합니다.",
        "학생": "70대 이상의 허리는 척추 마디 사이가 좁아지고 퇴행이 진행된 상태이므로, 척추가 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 가장 중요합니다. 허리를 구부정하게 숙이는 습관은 하중을 척추 뼈로 집중시켜 통증을 악화시키므로, 평소 등을 곧게 펴서 척추의 자연스러운 곡선을 유지해야 합니다. 특히 '누워서 엉덩이 들기(브릿지)'와 같은 운동으로 엉덩이 근육을 길러 허리가 받는 부하를 대신 흡수하게 만들고, 갑자기 허리를 비트는 동작을 피하여 관절을 보호해야 합니다.",
        "주부/은퇴": "70대 이상의 허리는 척추 마디 사이가 좁아지고 퇴행이 진행된 상태이므로, 척추가 눌리지 않게 바른 자세를 유지하여 신경 통로를 확보하는 것이 가장 중요합니다. 허리를 구부정하게 숙이는 습관은 하중을 척추 뼈로 집중시켜 통증을 악화시키므로, 평소 등을 곧게 펴서 척추의 자연스러운 곡선을 유지해야 합니다. 특히 '누워서 엉덩이 들기(브릿지)'와 같은 운동으로 엉덩이 근육을 길러 허리가 받는 부하를 대신 흡수하게 만들고, 갑자기 허리를 비트는 동작을 피하여 관절을 보호해야 합니다."
        },
        "어깨": {
        "사무직": "70대 이상의 어깨는 회전근개 힘줄이 얇아지고 약해진 상태이므로, 어깨가 안으로 굽지 않게 바른 정렬을 유지하여 힘줄이 뼈 사이에 끼이지 않도록 공간을 확보하는 것이 중요합니다. 등이 굽으면 어깨 관절이 좁아져 팔을 들 때마다 충돌이 발생하므로, 항상 가슴을 펴고 날개뼈를 등 뒤로 가볍게 모아주는 자세를 유지해야 합니다. 평소 '벽 밀기' 운동을 통해 날개뼈 주변 근육을 길러 어깨 관절의 부하를 대신 흡수하게 만들고, 무거운 물건을 갑자기 들어 올리는 동작을 피하여 힘줄 파열을 방지해야 합니다.",
        "현장직": "70대 이상의 어깨는 회전근개 힘줄이 얇아지고 약해진 상태이므로, 어깨가 안으로 굽지 않게 바른 정렬을 유지하여 힘줄이 뼈 사이에 끼이지 않도록 공간을 확보하는 것이 중요합니다. 등이 굽으면 어깨 관절이 좁아져 팔을 들 때마다 충돌이 발생하므로, 항상 가슴을 펴고 날개뼈를 등 뒤로 가볍게 모아주는 자세를 유지해야 합니다. 평소 '벽 밀기' 운동을 통해 날개뼈 주변 근육을 길러 어깨 관절의 부하를 대신 흡수하게 만들고, 무거운 물건을 갑자기 들어 올리는 동작을 피하여 힘줄 파열을 방지해야 합니다.",
        "운동선수": "70대 이상의 어깨는 회전근개 힘줄이 얇아지고 약해진 상태이므로, 어깨가 안으로 굽지 않게 바른 정렬을 유지하여 힘줄이 뼈 사이에 끼이지 않도록 공간을 확보하는 것이 중요합니다. 등이 굽으면 어깨 관절이 좁아져 팔을 들 때마다 충돌이 발생하므로, 항상 가슴을 펴고 날개뼈를 등 뒤로 가볍게 모아주는 자세를 유지해야 합니다. 평소 '벽 밀기' 운동을 통해 날개뼈 주변 근육을 길러 어깨 관절의 부하를 대신 흡수하게 만들고, 무거운 물건을 갑자기 들어 올리는 동작을 피하여 힘줄 파열을 방지해야 합니다.",
        "학생": "70대 이상의 어깨는 회전근개 힘줄이 얇아지고 약해진 상태이므로, 어깨가 안으로 굽지 않게 바른 정렬을 유지하여 힘줄이 뼈 사이에 끼이지 않도록 공간을 확보하는 것이 중요합니다. 등이 굽으면 어깨 관절이 좁아져 팔을 들 때마다 충돌이 발생하므로, 항상 가슴을 펴고 날개뼈를 등 뒤로 가볍게 모아주는 자세를 유지해야 합니다. 평소 '벽 밀기' 운동을 통해 날개뼈 주변 근육을 길러 어깨 관절의 부하를 대신 흡수하게 만들고, 무거운 물건을 갑자기 들어 올리는 동작을 피하여 힘줄 파열을 방지해야 합니다.",
        "주부/은퇴": "70대 이상의 어깨는 회전근개 힘줄이 얇아지고 약해진 상태이므로, 어깨가 안으로 굽지 않게 바른 정렬을 유지하여 힘줄이 뼈 사이에 끼이지 않도록 공간을 확보하는 것이 중요합니다. 등이 굽으면 어깨 관절이 좁아져 팔을 들 때마다 충돌이 발생하므로, 항상 가슴을 펴고 날개뼈를 등 뒤로 가볍게 모아주는 자세를 유지해야 합니다. 평소 '벽 밀기' 운동을 통해 날개뼈 주변 근육을 길러 어깨 관절의 부하를 대신 흡수하게 만들고, 무거운 물건을 갑자기 들어 올리는 동작을 피하여 힘줄 파열을 방지해야 합니다."
        },
        "무릎": {
        "사무직": "70대 이상의 무릎은 연골이 얇아져 관절 사이의 완충 작용이 떨어진 상태이므로, 서 있거나 걸을 때 무릎이 안으로 굽지 않게 바른 정렬을 유지하여 특정 부위만 마모되는 것을 막아야 합니다. 쪼그려 앉거나 무거운 짐을 드는 동작은 관절에 과도한 압력을 주어 퇴행을 앞당기므로 가급적 피해야 합니다. 평소 '의자에 앉아 다리 펴기' 운동으로 허벅지 근육을 길러 무릎 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 고관절과 발목 유연성을 관리하여 무릎 관절의 마찰을 줄여야 합니다.",
        "현장직": "70대 이상의 무릎은 연골이 얇아져 관절 사이의 완충 작용이 떨어진 상태이므로, 서 있거나 걸을 때 무릎이 안으로 굽지 않게 바른 정렬을 유지하여 특정 부위만 마모되는 것을 막아야 합니다. 쪼그려 앉거나 무거운 짐을 드는 동작은 관절에 과도한 압력을 주어 퇴행을 앞당기므로 가급적 피해야 합니다. 평소 '의자에 앉아 다리 펴기' 운동으로 허벅지 근육을 길러 무릎 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 고관절과 발목 유연성을 관리하여 무릎 관절의 마찰을 줄여야 합니다.",
        "운동선수": "70대 이상의 무릎은 연골이 얇아져 관절 사이의 완충 작용이 떨어진 상태이므로, 서 있거나 걸을 때 무릎이 안으로 굽지 않게 바른 정렬을 유지하여 특정 부위만 마모되는 것을 막아야 합니다. 쪼그려 앉거나 무거운 짐을 드는 동작은 관절에 과도한 압력을 주어 퇴행을 앞당기므로 가급적 피해야 합니다. 평소 '의자에 앉아 다리 펴기' 운동으로 허벅지 근육을 길러 무릎 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 고관절과 발목 유연성을 관리하여 무릎 관절의 마찰을 줄여야 합니다.",
        "학생": "70대 이상의 무릎은 연골이 얇아져 관절 사이의 완충 작용이 떨어진 상태이므로, 서 있거나 걸을 때 무릎이 안으로 굽지 않게 바른 정렬을 유지하여 특정 부위만 마모되는 것을 막아야 합니다. 쪼그려 앉거나 무거운 짐을 드는 동작은 관절에 과도한 압력을 주어 퇴행을 앞당기므로 가급적 피해야 합니다. 평소 '의자에 앉아 다리 펴기' 운동으로 허벅지 근육을 길러 무릎 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 고관절과 발목 유연성을 관리하여 무릎 관절의 마찰을 줄여야 합니다.",
        "주부/은퇴": "70대 이상의 무릎은 연골이 얇아져 관절 사이의 완충 작용이 떨어진 상태이므로, 서 있거나 걸을 때 무릎이 안으로 굽지 않게 바른 정렬을 유지하여 특정 부위만 마모되는 것을 막아야 합니다. 쪼그려 앉거나 무거운 짐을 드는 동작은 관절에 과도한 압력을 주어 퇴행을 앞당기므로 가급적 피해야 합니다. 평소 '의자에 앉아 다리 펴기' 운동으로 허벅지 근육을 길러 무릎 관절로 가는 하중을 근육이 대신 흡수하게 만들고, 고관절과 발목 유연성을 관리하여 무릎 관절의 마찰을 줄여야 합니다."
        },
        "손목손가락": {
        "사무직": "70대 이상의 손목과 손가락은 관절 주변의 인대가 뻣뻣해져 작은 충격에도 염증이 생기기 쉬우므로, 물건을 잡을 때 손가락 끝의 힘만 쓰지 말고 손바닥 전체로 감싸 쥐는 바른 자세를 유지해야 합니다. 손가락과 손목을 과하게 구부리는 동작은 퇴행된 마디 관절에 압력을 집중시켜 통증을 악화시키므로 주의가 필요합니다. 평소 '주먹 쥐고 천천히 펴기' 운동과 전완부 스트레칭을 병행하여 손목으로 가는 부하를 근육이 대신 흡수하게 만들고, 따뜻한 찜질로 관절의 유연성을 관리해 주는 것이 좋습니다.",
        "현장직": "70대 이상의 손목과 손가락은 관절 주변의 인대가 뻣뻣해져 작은 충격에도 염증이 생기기 쉬우므로, 물건을 잡을 때 손가락 끝의 힘만 쓰지 말고 손바닥 전체로 감싸 쥐는 바른 자세를 유지해야 합니다. 손가락과 손목을 과하게 구부리는 동작은 퇴행된 마디 관절에 압력을 집중시켜 통증을 악화시키므로 주의가 필요합니다. 평소 '주먹 쥐고 천천히 펴기' 운동과 전완부 스트레칭을 병행하여 손목으로 가는 부하를 근육이 대신 흡수하게 만들고, 따뜻한 찜질로 관절의 유연성을 관리해 주는 것이 좋습니다.",
        "운동선수": "70대 이상의 손목과 손가락은 관절 주변의 인대가 뻣뻣해져 작은 충격에도 염증이 생기기 쉬우므로, 물건을 잡을 때 손가락 끝의 힘만 쓰지 말고 손바닥 전체로 감싸 쥐는 바른 자세를 유지해야 합니다. 손가락과 손목을 과하게 구부리는 동작은 퇴행된 마디 관절에 압력을 집중시켜 통증을 악화시키므로 주의가 필요합니다. 평소 '주먹 쥐고 천천히 펴기' 운동과 전완부 스트레칭을 병행하여 손목으로 가는 부하를 근육이 대신 흡수하게 만들고, 따뜻한 찜질로 관절의 유연성을 관리해 주는 것이 좋습니다.",
        "학생": "70대 이상의 손목과 손가락은 관절 주변의 인대가 뻣뻣해져 작은 충격에도 염증이 생기기 쉬우므로, 물건을 잡을 때 손가닥 끝의 힘만 쓰지 말고 손바닥 전체로 감싸 쥐는 바른 자세를 유지해야 합니다. 손가락과 손목을 과하게 구부리는 동작은 퇴행된 마디 관절에 압력을 집중시켜 통증을 악화시키므로 주의가 필요합니다. 평소 '주먹 쥐고 천천히 펴기' 운동과 전완부 스트레칭을 병행하여 손목으로 가는 부하를 근육이 대신 흡수하게 만들고, 따뜻한 찜질로 관절의 유연성을 관리해 주는 것이 좋습니다.",
        "주부/은퇴": "70대 이상의 손목과 손가락은 관절 주변의 인대가 뻣뻣해져 작은 충격에도 염증이 생기기 쉬우므로, 물건을 잡을 때 손가락 끝의 힘만 쓰지 말고 손바닥 전체로 감싸 쥐는 바른 자세를 유지해야 합니다. 손가락과 손목을 과하게 구부리는 동작은 퇴행된 마디 관절에 압력을 집중시켜 통증을 악화시키므로 주의가 필요합니다. 평소 '주먹 쥐고 천천히 펴기' 운동과 전완부 스트레칭을 병행하여 손목으로 가는 부하를 근육이 대신 흡수하게 만들고, 따뜻한 찜질로 관절의 유연성을 관리해 주는 것이 좋습니다."
        },
        "발목발가락": {
        "사무직": "70대 이상의 발목과 발가락은 하체 근육이 빠지면서 지면의 충격을 흡수하는 능력이 저하되어 낙상과 골절의 위험이 매우 높은 상태입니다. 발가락이 지면을 견고하게 지지하는 바른 척추 정렬을 유지해야 전신 균형이 잡히고 발목 관절의 비틀림을 막을 수 있습니다. 평소 '발가락으로 수건 당기기'나 '가위바위보' 운동으로 발바닥 근육을 길러 충격을 흡수하게 만들고, 스트레칭을 병행하여 발목, 무릎, 고관절의 유연성을 확보함으로써 보행 시 안정성을 높여야 합니다.",
        "현장직": "70대 이상의 발목과 발가락은 하체 근육이 빠지면서 지면의 충격을 흡수하는 능력이 저하되어 낙상과 골절의 위험이 매우 높은 상태입니다. 발가락이 지면을 견고하게 지지하는 바른 척추 정렬을 유지해야 전신 균형이 잡히고 발목 관절의 비틀림을 막을 수 있습니다. 평소 '발가락으로 수건 당기기'나 '가위바위보' 운동으로 발바닥 근육을 길러 충격을 흡수하게 만들고, 스트레칭을 병행하여 발목, 무릎, 고관절의 유연성을 확보함으로써 보행 시 안정성을 높여야 합니다.",
        "운동선수": "70대 이상의 발목과 발가락은 하체 근육이 빠지면서 지면의 충격을 흡수하는 능력이 저하되어 낙상과 골절의 위험이 매우 높은 상태입니다. 발가락이 지면을 견고하게 지지하는 바른 척추 정렬을 유지해야 전신 균형이 잡히고 발목 관절의 비틀림을 막을 수 있습니다. 평소 '발가락으로 수건 당기기'나 '가위바위보' 운동으로 발바닥 근육을 길러 충격을 흡수하게 만들고, 스트레칭을 병행하여 발목, 무릎, 고관절의 유연성을 확보함으로써 보행 시 안정성을 높여야 합니다.",
        "학생": "70대 이상의 발목과 발가락은 하체 근육이 빠지면서 지면의 충격을 흡수하는 능력이 저하되어 낙상과 골절의 위험이 매우 높은 상태입니다. 발가락이 지면을 견고하게 지지하는 바른 척추 정렬을 유지해야 전신 균형이 잡히고 발목 관절의 비틀림을 막을 수 있습니다. 평소 '발가락으로 수건 당기기'나 '가위바위보' 운동으로 발바닥 근육을 길러 충격을 흡수하게 만들고, 스트레칭을 병행하여 관절의 유연성을 확보함으로써 보행 시 안정성을 높여야 합니다.",
        "주부/은퇴": "70대 이상의 발목과 발가락은 하체 근육이 빠지면서 지면의 충격을 흡수하는 능력이 저하되어 낙상과 골절의 위험이 매우 높은 상태입니다. 발가락이 지면을 견고하게 지지하는 바른 척추 정렬을 유지해야 전신 균형이 잡히고 발목 관절의 비틀림을 막을 수 있습니다. 평소 '발가락으로 수건 당기기'나 '가위바위보' 운동으로 발바닥 근육을 길러 충격을 흡수하게 만들고, 스트레칭을 병행하여 발목, 무릎, 고관절의 유연성을 확보함으로써 보행 시 안정성을 높여야 합니다.",
        },
        "고관절": {
        "사무직": "70대 이상의 고관절은 주변 근육이 빠지면서 상체의 하중이 관절면으로 직접 전달되어 연골 마모가 빨라지고 낙상 시 골절 위험이 매우 높은 상태입니다. 쪼그려 앉거나 무리하게 다리를 꼬는 자세를 피하고, 항상 골반의 평형을 유지하는 바른 자세를 통해 고관절이 한쪽으로만 눌리지 않게 관리해야 합니다. 평소 '의자 잡고 옆으로 다리 들기' 운동으로 중둔근을 길러 보행 시 흔들림을 잡아주고, 근육이 하중을 흡수하게 만들어 고관절의 퇴행을 늦춰야 합니다.",
        "현장직": "70대 이상의 고관절은 주변 근육이 빠지면서 상체의 하중이 관절면으로 직접 전달되어 연골 마모가 빨라지고 낙상 시 골절 위험이 매우 높은 상태입니다. 쪼그려 앉거나 무리하게 다리를 꼬는 자세를 피하고, 항상 골반의 평형을 유지하는 바른 자세를 통해 고관절이 한쪽으로만 눌리지 않게 관리해야 합니다. 평소 '의자 잡고 옆으로 다리 들기' 운동으로 중둔근을 길러 보행 시 흔들림을 잡아주고, 근육이 하중을 흡수하게 만들어 고관절의 퇴행을 늦춰야 합니다.",
        "운동선수": "70대 이상의 고관절은 주변 근육이 빠지면서 상체의 하중이 관절면으로 직접 전달되어 연골 마모가 빨라지고 낙상 시 골절 위험이 매우 높은 상태입니다. 쪼그려 앉거나 무리하게 다리를 꼬는 자세를 피하고, 항상 골반의 평형을 유지하는 바른 자세를 통해 고관절이 한쪽으로만 눌리지 않게 관리해야 합니다. 평소 '의자 잡고 옆으로 다리 들기' 운동으로 중둔근을 길러 보행 시 흔들림을 잡아주고, 근육이 하중을 흡수하게 만들어 고관절의 퇴행을 늦춰야 합니다.",
        "학생": "70대 이상의 고관절은 주변 근육이 빠지면서 상체의 하중이 관절면으로 직접 전달되어 연골 마모가 빨라지고 낙상 시 골절 위험이 매우 높은 상태입니다. 쪼그려 앉거나 무리하게 다리를 꼬는 자세를 피하고, 항상 골반의 평형을 유지하는 바른 자세를 통해 고관절이 한쪽으로만 눌리지 않게 관리해야 합니다. 평소 '의자 잡고 옆으로 다리 들기' 운동으로 중둔근을 길러 보행 시 흔들림을 잡아주고, 근육이 하중을 흡수하게 만들어 고관절의 퇴행을 늦춰야 합니다.",
        "주부/은퇴": "70대 이상의 고관절은 주변 근육이 빠지면서 상체의 하중이 관절면으로 직접 전달되어 연골 마모가 빨라지고 낙상 시 골절 위험이 매우 높은 상태입니다. 쪼그려 앉거나 무리하게 다리를 꼬는 자세를 피하고, 항상 골반의 평형을 유지하는 바른 자세를 통해 고관절이 한쪽으로만 눌리지 않게 관리해야 합니다. 평소 '의자 잡고 옆으로 다리 들기' 운동으로 중둔근을 길러 보행 시 흔들림을 잡아주고, 근육이 하중을 흡수하게 만들어 고관절의 퇴행을 늦춰야 합니다."
        },
        "팔꿈치": {
        "사무직": "70대 이상의 팔꿈치는 힘줄이 얇아지고 석회화가 진행되기 쉬운 상태이므로, 무거운 물건을 들거나 수건을 짜는 등 팔을 비트는 동작 시 각별한 주의가 필요합니다. 팔꿈치가 몸통에서 멀어진 상태로 힘을 쓰면 관절에 과도한 지렛대 압력이 가해지므로, 항상 물건을 몸쪽으로 밀착시켜 드는 바른 자세를 유지해야 합니다. 평소 '손목 까딱이기' 운동으로 전완부 근육을 부드럽게 길러 팔꿈치 힘줄이 받는 부하를 대신 흡수하게 만들고, 따뜻한 찜질로 혈액순환을 도와 힘줄의 노화를 늦춰야 합니다.",
        "현장직": "70대 이상의 팔꿈치는 힘줄이 얇아지고 석회화가 진행되기 쉬운 상태이므로, 무거운 물건을 들거나 수건을 짜는 등 팔을 비트는 동작 시 각별한 주의가 필요합니다. 팔꿈치가 몸통에서 멀어진 상태로 힘을 쓰면 관절에 과도한 지렛대 압력이 가해지므로, 항상 물건을 몸쪽으로 밀착시켜 드는 바른 자세를 유지해야 합니다. 평소 '손목 까딱이기' 운동으로 전완부 근육을 부드럽게 길러 팔꿈치 힘줄이 받는 부하를 대신 흡수하게 만들고, 따뜻한 찜질로 혈액순환을 도와 힘줄의 노화를 늦춰야 합니다.",
        "운동선수": "70대 이상의 팔꿈치는 힘줄이 얇아지고 석회화가 진행되기 쉬운 상태이므로, 무거운 물건을 들거나 수건을 짜는 등 팔을 비트는 동작 시 각별한 주의가 필요합니다. 팔꿈치가 몸통에서 멀어진 상태로 힘을 쓰면 관절에 과도한 지렛대 압력이 가해지므로, 항상 물건을 몸쪽으로 밀착시켜 드는 바른 자세를 유지해야 합니다. 평소 '손목 까딱이기' 운동으로 전완부 근육을 부드럽게 길러 팔꿈치 힘줄이 받는 부하를 대신 흡수하게 만들고, 따뜻한 찜질로 혈액순환을 도와 힘줄의 노화를 늦춰야 합니다.",
        "학생": "70대 이상의 팔꿈치는 힘줄이 얇아지고 석회화가 진행되기 쉬운 상태이므로, 무거운 물건을 들거나 수건을 짜는 등 팔을 비트는 동작 시 각별한 주의가 필요합니다. 팔꿈치가 몸통에서 멀어진 상태로 힘을 쓰면 관절에 과도한 지렛대 압력이 가해지므로, 항상 물건을 몸쪽으로 밀착시켜 드는 바른 자세를 유지해야 합니다. 평소 '손목 까딱이기' 운동으로 전완부 근육을 부드럽게 길러 팔꿈치 힘줄이 받는 부하를 대신 흡수하게 만들고, 따뜻한 찜질로 혈액순환을 도와 힘줄의 노화를 늦춰야 합니다.",
        "주부/은퇴": "70대 이상의 팔꿈치는 힘줄이 얇아지고 석회화가 진행되기 쉬운 상태이므로, 무거운 물건을 들거나 수건을 짜는 등 팔을 비트는 동작 시 각별한 주의가 필요합니다. 팔꿈치가 몸통에서 멀어진 상태로 힘을 쓰면 관절에 과도한 지렛대 압력이 가해지므로, 항상 물건을 몸쪽으로 밀착시켜 드는 바른 자세를 유지해야 합니다. 평소 '손목 까딱이기' 운동으로 전완부 근육을 부드럽게 길러 팔꿈치 힘줄이 받는 부하를 대신 흡수하게 만들고, 따뜻한 찜질로 혈액순환을 도와 힘줄의 노화를 늦춰야 합니다."
        },
        "등/날개뼈": {
        "사무직": "70대 이상의 등은 척추 노화로 인해 점차 앞으로 굽어지기 쉬우므로, 날개뼈를 등 뒤로 가볍게 모아 상체를 바로 세우는 자세를 유지하여 척추 마디의 압박을 줄여주는 것이 중요합니다. 등이 굽으면 날개뼈가 제 위치를 벗어나 목과 어깨에 과도한 하중을 전달하므로, 평소 가슴을 펴는 바른 정렬을 통해 전신의 부하를 분산해야 합니다. 특히 'W자 날개뼈 모으기' 운동으로 등 근육의 힘을 길러 상체를 스스로 지탱하게 만들고, 근육이 척추의 부담을 대신 흡수하도록 관리해야 합니다.",
        "현장직": "70대 이상의 등은 척추 노화로 인해 점차 앞으로 굽어지기 쉬우므로, 날개뼈를 등 뒤로 가볍게 모아 상체를 바로 세우는 자세를 유지하여 척추 마디의 압박을 줄여주는 것이 중요합니다. 등이 굽으면 날개뼈가 제 위치를 벗어나 목과 어깨에 과도한 하중을 전달하므로, 평소 가슴을 펴는 바른 정렬을 통해 전신의 부하를 분산해야 합니다. 특히 'W자 날개뼈 모으기' 운동으로 등 근육의 힘을 길러 상체를 스스로 지탱하게 만들고, 근육이 척추의 부담을 대신 흡수하도록 관리해야 합니다.",
        "운동선수": "70대 이상의 등은 척추 노화로 인해 점차 앞으로 굽어지기 쉬우므로, 날개뼈를 등 뒤로 가볍게 모아 상체를 바로 세우는 자세를 유지하여 척추 마디의 압박을 줄여주는 것이 중요합니다. 등이 굽으면 날개뼈가 제 위치를 벗어나 목과 어깨에 과도한 하중을 전달하므로, 평소 가슴을 펴는 바른 정렬을 통해 전신의 부하를 분산해야 합니다. 특히 'W자 날개뼈 모으기' 운동으로 등 근육의 힘을 길러 상체를 스스로 지탱하게 만들고, 근육이 척추의 부담을 대신 흡수하도록 관리해야 합니다.",
        "학생": "70대 이상의 등은 척추 노화로 인해 점차 앞으로 굽어지기 쉬우므로, 날개뼈를 등 뒤로 가볍게 모아 상체를 바로 세우는 자세를 유지하여 척추 마디의 압박을 줄여주는 것이 중요합니다. 등이 굽으면 날개뼈가 제 위치를 벗어나 목과 어깨에 과도한 하중을 전달하므로, 평소 가슴을 펴는 바른 정렬을 통해 전신의 부하를 분산해야 합니다. 특히 'W자 날개뼈 모으기' 운동으로 등 근육의 힘을 길러 상체를 스스로 지탱하게 만들고, 근육이 척추의 부담을 대신 흡수하도록 관리해야 합니다.",
        "주부/은퇴": "70대 이상의 등은 척추 노화로 인해 점차 앞으로 굽어지기 쉬우므로, 날개뼈를 등 뒤로 가볍게 모아 상체를 바로 세우는 자세를 유지하여 척추 마디의 압박을 줄여주는 것이 중요합니다. 등이 굽으면 날개뼈가 제 위치를 벗어나 목과 어깨에 과도한 하중을 전달하므로, 평소 가슴을 펴는 바른 정렬을 통해 전신의 부하를 분산해야 합니다. 특히 'W자 날개뼈 모으기' 운동으로 등 근육의 힘을 길러 상체를 스스로 지탱하게 만들고, 근육이 척추의 부담을 대신 흡수하도록 관리해야 합니다."
        }
    }
}

# 기간별 고정 팁
DURATION_TIPS = {
    "급성": "🚩 [급성 통증 주의] 현재는 염증기일 수 있습니다. 무리한 운동이나 스트레칭은 오히려 조직 손상을 키울 수 있으니 '냉찜질'과 '절대 안정'을 최우선으로 하세요.",
    "만성": "🔄 [만성 통증 관리] 주변 근육의 유착과 약화가 원인입니다. '온찜질'로 혈액순환을 돕고, 몸이 굳지 않게 통증이 없는 범위 내에서 조금씩 가동 범위를 늘려나가는 것이 중요합니다."
}

# -------------------------------
# 신규 라우트: 자가 문진 및 결과
# -------------------------------
@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html', region_dict=region_dict)

@app.route('/result', methods=['POST'])
def result():
    # 1. 문진 데이터 수집
    user_data = {
        "age": request.form.get("age"),      # "10~20대", "30~40대" 등
        "part": request.form.get("part"),     # "목", "허리" 등
        "duration": request.form.get("duration"),
        "job": request.form.get("job")
    }
    
    reviews = load_reviews()
    matched_hospitals = []
    target_part = user_data["part"]

    # 2. 3중 정밀 코멘트 추출
    u_age = user_data["age"]
    u_part = user_data["part"]
    u_job = user_data["job"]
    u_dur = user_data["duration"]

    # 정밀 매칭 시도
    precision_comment = PRECISION_COMMENTS.get(u_age, {}).get(u_part, {}).get(u_job, "")
    
    # 데이터가 없을 경우를 위한 안전장치(기본 가이드)
    if not precision_comment:
        precision_comment = f"{u_age} {u_job}님의 {u_part} 증상을 분석 중입니다. 신뢰도 높은 리뷰 기반 리스트를 참고해 주세요."

    # 기간별 팁 가져오기
    duration_tip = DURATION_TIPS.get(u_dur, "")

    # 최종 조립 (디자인 박스에 들어갈 최종 텍스트)
    final_comment = f"{duration_tip}\n\n[맞춤 건강 코멘트]\n{precision_comment}"

    # 3. 병원 매칭 키워드 설정
    if target_part == "등/날개뼈":
        search_keywords = ["등", "날개뼈"]
    elif target_part == "발목발가락":
        search_keywords = ["발목", "발가락"]
    elif target_part == "손목손가락":
        search_keywords = ["손목", "손가락"]
    else:
        search_keywords = [target_part]

    # 4. 병원 매칭 및 데이터 가공
    for h in hospitals:
        relevant_reviews = []
        for r in reviews:
            if r["hospital_name"] == h["name"]:
                keywords_list = r.get("keywords") or []
                is_match = False
                
                for sk in search_keywords:
                    if sk in ["등", "목"]:
                        if sk in keywords_list:
                            is_match = True
                    else:
                        if any(sk in k for k in keywords_list):
                            is_match = True
                    if is_match: break
                
                if is_match:
                    relevant_reviews.append(r)
        
        if relevant_reviews:
            h_copy = h.copy()
            avg = calculate_average_rating(h["name"], reviews)
            h_copy["rating"] = avg if avg is not None else "평점 없음"
            h_copy["review_count"] = len([r for r in reviews if r["hospital_name"] == h["name"]])
            
            display_text = target_part
            if target_part == "등":
                display_text = "등/날개뼈"
            
            h_copy["part_review_count"] = len(relevant_reviews)
            h_copy["match_message"] = f"{display_text} 관련 리뷰가 {len(relevant_reviews)}개 있습니다."
            matched_hospitals.append(h_copy)

    # 5. 정렬
    matched_hospitals.sort(key=lambda x: (-x["part_review_count"], x["rating"] == "평점 없음", -(x["rating"] if x["rating"] != "평점 없음" else 0)))

    return render_template(
        'diagnosis_result.html',
        user_data=user_data,
        hospitals=matched_hospitals,
        comment=final_comment,  # 정밀 분석 결과 전송
        video_url=""
    )

# -------------------------------
# 기존 라우트 (메인 및 상세)
# -------------------------------
@app.route('/')
def index():
    search_query = request.args.get("search", "").strip()
    gu = request.args.get("gu", "")
    category = request.args.get("category", "")
    region = request.args.get("region", "")
    sort_option = request.args.get("sort", "")

    show_notice = bool(search_query or gu or category or region or sort_option)
    reviews = load_reviews()
    
    display_hospitals = []
    for h in hospitals:
        h_copy = h.copy()
        avg = calculate_average_rating(h["name"], reviews)
        h_copy["rating"] = avg if avg is not None else "평점 없음"
        h_copy["review_count"] = len([r for r in reviews if r["hospital_name"] == h["name"]])
        display_hospitals.append(h_copy)

    filtered = [h for h in display_hospitals if 
                (not search_query or search_query.lower() in h["name"].lower()) and
                (not gu or h["gu"] == gu) and
                (not category or category in h["category"]) and
                (not region or h["region"] == region)]

    if sort_option == "rating":
        filtered.sort(key=lambda x: (x["rating"] == "평점 없음", -(x["rating"] if x["rating"] != "평점 없음" else 0)))
    else:
        filtered.sort(key=lambda x: x["name"])

    return render_template(
        'index.html',
        hospitals=filtered,
        region_dict=region_dict,
        visit_count=get_visit_count(),
        search_query=search_query,
        selected_gu=gu,
        selected_category=category,
        selected_region=region,
        regions=region_dict.get(gu, []),
        show_notice=show_notice
    )

@app.route("/hospital/<path:hospital_name>")
def hospital_detail(hospital_name):
    reviews = load_reviews()
    hospital_review_list = [r for r in reviews if r["hospital_name"] == hospital_name]
    hospital = next((h for h in hospitals if h["name"] == hospital_name), None)
    if not hospital:
        return "해당 병원을 찾을 수 없습니다.", 404
    return render_template("hospital_detail.html", hospital=hospital, reviews=hospital_review_list)

@app.route("/sitemap.xml")
def sitemap(): return send_from_directory(BASE_DIR, "sitemap.xml")

@app.route("/robots.txt")
def robots(): return send_from_directory(BASE_DIR, "robots.txt")

if __name__ == "__main__":
    app.run(debug=True)