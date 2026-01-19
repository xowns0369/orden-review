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
# 신규 라우트: 자가 문진 및 결과
# -------------------------------
@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html', region_dict=region_dict)

@app.route('/result', methods=['POST'])
def result():
    # 1. 문진 데이터 수집
    user_data = {
        "age": request.form.get("age"),      # 10~20, 30~40, 50~60, 70 이상
        "part": request.form.get("part"),    # 목, 허리, 어깨, 발목발가락, 손목손가락 등
        "duration": request.form.get("duration"),
        "job": request.form.get("job")
    }
    
    reviews = load_reviews()
    matched_hospitals = []
    target_part = user_data["part"]

    # 2. 노하우 데이터베이스 (운영자님 제공 데이터)
    KNOWHOW_DB = {
        "무릎": {
            "10~20": "기초 공사와 부상 예방\n신체 능력이 정점인 시기라 무릎의 소중함을 잊기 쉽습니다. 이 시기의 관리가 평생의 무릎 건강을 결정합니다.\n\n노하우 1: '착지' 교육 – 농구, 축구 등 점프가 많은 운동을 할 때 발바닥 전체로 소리 나지 않게 착지하는 습관을 들이세요. 무릎 연골판 파열의 대부분은 착지 시 발생합니다.\n노하우 2: 신발 선택 – 패션도 중요하지만, 밑창이 너무 딱딱한 신발(플랫슈즈, 단화)은 지면 충격을 무릎으로 그대로 전달합니다. 충격 흡수 기능이 있는 신발을 선호하세요.\n노하우 3: 골반 건강 – 골반이 틀어지면 무릎 정렬이 깨집니다. 짝다리 짚기, 다리 꼬고 앉는 습관을 의식적으로 교정해야 합니다.",
            "30~40": "생활 속 틈새 관리\n노화의 전조 증상이 나타나는 시기입니다. 따로 운동할 시간이 없다면 생활 습관을 바꿔야 합니다.\n\n노하우 1: 의자 높이 조절 – 의자가 너무 낮으면 일어날 때 무릎에 큰 부하가 걸립니다. 무릎 각도가 90도 이상이 되도록 의자 높이를 조절하세요.\n노하우 2: 하이힐/구두 사용 제한 – 높은 굽은 체중을 앞쪽으로 쏠리게 해 무릎 앞쪽 통증(슬개대퇴통증증후군)을 유발합니다. 업무 시에는 실내화로 갈아 신으세요.\n노하우 3: '무릎 주변' 근육 이완 – 허벅지 앞쪽만 강화하지 말고, 폼롤러를 이용해 허벅지 옆쪽(장경인대)과 종아리 근육을 풀어주어 관절의 긴장을 완화하세요.",
            "50~60": "윤활유 공급과 정렬 유지\n본격적인 퇴행성 관절염 예방 단계입니다. 관절을 아끼면서도 기능을 유지하는 지혜가 필요합니다.\n\n노하우 1: 아침 기상 직후 '허공 자전거' – 자고 일어나면 관절액이 굳어 뻣뻣합니다. 일어나기 전 침대에 누워 다리를 들고 가볍게 자전거 타는 동작을 1~2분만 해도 관절에 윤활유가 돕니다.\n노하우 2: 단백질 섭취 극대화 – 운동만큼 중요한 것이 영양입니다. 근육 생성을 위해 끼니마다 양질의 단백질(닭가슴살, 계란, 콩 등)을 반드시 포함하세요.\n노하우 3: 무릎 '소리'에 집중 – 무릎에서 모래 긁히는 소리가 나거나 걸리는 느낌이 든다면 연골 마모의 신호일 수 있으니 즉시 전문가의 검진을 받으세요.",
            "70 이상": "통증 조절과 낙상 방지\n안전이 최우선입니다. 무릎이 아프다고 가만히 있으면 근육이 빠져 더 못 걷게 되는 악순환에 빠집니다.\n\n노하우 1: 발목 운동 병행 – 무릎을 지탱하는 것은 발목의 안정성입니다. 앉아서 발목을 앞뒤로 까딱거리는 운동을 자주 하여 혈액순환을 돕고 균형 감각을 키우세요.\n노하우 2: 따뜻한 환경 유지 – 관절은 온도에 예민합니다. 항상 무릎을 따뜻하게 유지하고(무릎 담요 등), 비가 오거나 추운 날에는 온찜질을 습관화하세요.\n노하우 3: 욕실 안전장치 – 무릎 힘이 약해지는 이 시기에는 욕실에서 미끄러져 2차 부상을 당하는 경우가 많습니다. 욕실에 손잡이를 설치하고 미끄럼 방지 매트를 까는 것도 무릎 관리의 일부입니다."
        },
        "고관절": {
            "10~20": "변형 예방과 대칭 유지\n이 시기에는 고관절 자체의 문제보다는 잘못된 습관으로 인한 골반 변형을 막는 것이 최우선입니다.\n\n- 가방 메는 습관: 한쪽으로만 메는 숄더백은 골반의 높낮이를 다르게 하여 고관절 비대칭을 유발합니다. 가급적 백팩을 이용하거나 양쪽을 번갈아 가며 메세요.\n- 스마트폰 볼 때 다리 꼬기 금지: 다리를 꼬고 앉으면 한쪽 고관절이 과도하게 회전되어 관절막이 느슨해지거나 찝히는 증상이 생깁니다.\n- 바지 뒷주머니 비우기: 뒷주머니에 두꺼운 지갑이나 휴대폰을 넣고 앉으면 골반이 한쪽으로 기울어지며 고관절 정렬이 깨집니다.",
            "30~40": "압력 분산과 주변 근육 보호\n활동량은 많지만 신체 유연성이 떨어지기 시작하는 시기입니다. 고관절에 가해지는 누적 압력을 관리해야 합니다.\n\n- '양반다리'와 '아빠천사' 자세 피하기: 바닥에 앉을 때 양반다리를 하거나 무릎을 굽혀 앉는 자세는 고관절 내 압력을 평소의 수 배로 높입니다. 무조건 의자 생활을 습관화하세요.\n- 오래 서 있을 때 짝다리 금지: 한쪽 고관절에만 체중을 싣는 짝다리는 고관절 염증(점액낭염)의 주원인입니다. 양발에 무게를 5:5로 분산하는 의식을 하세요.\n- 신발 쿠션 확인: 딱딱한 구두나 하이힐은 지면 충격을 고관절로 고스란히 전달합니다. 충격 흡수가 잘 되는 기능성 깔창을 활용하는 것도 노하우입니다.",
            "50~60": "퇴행 지연과 환경 대전환\n본격적으로 고관절 연골이 얇아지고 골밀도가 낮아지는 시기입니다. 관절을 '아껴 쓰는 모드'로 전환해야 합니다.\n\n- 취침 시 다리 사이에 베개 끼우기: 옆으로 누워 잘 때 다리 사이에 두툼한 베개를 끼우면 고관절이 과도하게 꺾이는 것을 막아주어 통증 완화에 매우 효과적입니다.\n- 변기 높이 조절: 낮은 변기에 앉았다 일어날 때 고관절에 큰 힘이 들어갑니다. 필요한 경우 변기 높이 조절기(시트)를 설치하면 관절 부담을 크게 줄일 수 있습니다.\n- 체중 유지와 식단: 고관절은 체중을 직접적으로 지탱합니다. 1kg의 체중 감량은 고관절이 느끼는 하중을 3~4kg 줄여주는 효과가 있습니다.",
            "70 이상": "낙상 방지와 안전제일\n이 연령대에서는 고관절 관리의 핵심이 '낙상 사고 예방' 그 자체입니다.\n\n- 집안 문턱 없애기: 사소한 문턱에 발이 걸려 넘어지는 것이 고관절 골절의 가장 큰 원인입니다. 문턱을 제거하거나 경사로를 설치하세요.\n- 기상 시 서두르지 않기: 자고 일어날 때 갑자기 일어나면 기립성 저혈압으로 어지러워 넘어질 수 있습니다. 침대 끝에 1분 정도 걸터앉았다가 천천히 일어나세요.\n- 욕실 미끄럼 방지 패드: 물기가 많은 욕실은 고관절의 가장 큰 적입니다. 미끄럼 방지 스티커나 매트를 사각지대 없이 꼼꼼히 설치하세요."
        },
        "어깨": {
            "10~20": "정렬 유지와 과사용 방지\n스마트폰 사용과 공부로 인해 어깨가 앞으로 말리는 '라운드 숄더'를 예방하는 것이 핵심입니다.\n\n- 스마트폰 눈높이 조절: 고개를 숙이고 어깨를 웅크리는 자세는 어깨 관절 앞쪽 인대를 짧게 만듭니다. 스마트폰을 눈높이까지 들어 올려 어깨가 펴지게 하세요.\n- 옆으로 누워 스마트폰 금지: 한쪽 어깨로 체중을 지탱하며 옆으로 누워 스마트폰을 보는 습관은 어깨 관절의 '비대칭 충돌'을 일으키는 주범입니다.\n- 과도한 상체 운동 경계: 본인의 가동 범위를 벗어난 무거운 무게를 들 때 어깨 회전근개가 파열되는 경우가 많습니다.",
            "30~40": "경직 방지와 자세 교정\n사회활동이 왕성하여 업무 스트레스가 어깨 근육(승모근)에 쌓이고, 관절 내부가 굳기 시작하는 시기입니다.\n\n- 컴퓨터 작업 환경 개선: 키보드와 마우스가 너무 멀리 있으면 어깨가 계속 긴장 상태가 됩니다. 팔꿈치 각도가 90도가 되도록 책상 높이를 맞추세요.\n- 어깨 가방 번갈아 메기: 한쪽으로만 무거운 가방을 메면 어깨 관절이 한쪽으로 하강하며 정렬이 깨집니다.\n- 운전 자세 체크: 핸들 아래쪽(8시 20분 방향)을 잡아 어깨의 힘을 빼주세요.",
            "50~60": "동결건(오십견) 예방과 보온\n회전근개 파열이나 오십견이 가장 많이 발생하는 시기입니다. 관절을 '부드럽게' 유지하는 것이 노하우입니다.\n\n- 어깨 보온 유지: 어깨는 외부 온도에 민감합니다. 자는 동안 어깨가 노출되지 않게 하고, 통증이 느껴지면 온찜질을 해서 혈액순환을 도와야 합니다.\n- 뒷짐 지는 습관 주의: 뒷짐 자세가 관절 내 공간을 좁게 만들어 회전근개에 압박을 줍니다.\n- 높은 곳의 물건 내릴 때 주의: 팔을 머리 위로 갑자기 뻗는 동작에서 충돌 증후군이 발생하기 쉽습니다.",
            "70 이상": "가동 범위 보존과 무리한 활동 자제\n어깨 관절염과 만성 파열이 흔한 시기입니다. 완전히 굳지 않도록 관리하는 것이 목표입니다.\n\n- 팔 베개 절대 금지: 본인이나 손주에게 팔 베개를 해주는 행동은 어깨 관절 상태를 급격히 악화시킵니다.\n- 옷 입고 벗는 순서: 통증이 있다면 아픈 팔부터 먼저 소매에 넣고, 벗을 때는 건강한 팔부터 빼세요.\n- 무거운 시장바구니 주의: 바퀴가 달린 카트를 적극 활용하세요."
        },
        "발목발가락": {
            "10~20": "변형 방지와 아치(Arch) 보호\n- 신발 선택 노하우: 디자인 때문에 너무 꽉 끼거나 앞코가 뾰족한 신발은 피하세요.\n- 슬리퍼/단화 주의: 밑창이 얇은 신발은 발바닥 충격 흡수가 안 되어 족저근막염의 원인이 됩니다.\n- 발가락 정렬: 집에서는 발가락 사이를 벌려주는 스트레칭을 자주 해주세요.",
            "30~40": "충격 완화와 피로 회복\n- 신발의 '골든타임': 뒷굽이 한쪽으로만 닳았다면 즉시 수선하세요. 무너진 굽은 발목 불안정증을 유발합니다.\n- 사무실 내 환경: 구두 대신 쿠션감이 충분한 실내화로 갈아 신으세요.\n- 발바닥 지압 노하우: 골프공이나 테니스공을 발바닥 아래에 두고 굴려주면 족저근막 유연성에 좋습니다.",
            "50~60": "발바닥 지방층 보호와 보온\n- 집안에서도 신발 착용: 맨발로 딱딱한 바닥을 걷는 것은 얇아진 지방층에 큰 무리를 줍니다. 거실화를 신으세요.\n- 족욕 생활화: 자기 전 15분 따뜻한 족욕은 관절 유연성 확보에 탁월합니다.\n- 신발 사이즈 재측정: 노화로 아치가 낮아지면 발이 넓어집니다. 현재 발에 맞는 사이즈를 찾으세요.",
            "70 이상": "균형 유지와 피부 관리\n- 발톱 관리: 발톱을 너무 짧게 자르지 말고 '일자'로 깎아 관리하세요.\n- 양말의 중요성: 보온성이 좋고 미끄럼 방지 처리가 된 양말을 항상 착용하세요.\n- 발 피부 관찰: 매일 저녁 발바닥에 상처가 있는지 확인하세요. 낡은 신발은 척추에도 영향을 줍니다."
        },
        "손목손가락": {
            "10~20": "변형 방지와 아치 보호: 스마트폰 사용 시 손목이 꺾이지 않도록 주의하고 자주 스트레칭 하세요.",
            "30~40": "충격 완화와 피로 회복: 장시간 타이핑 시 손목 받침대를 사용하고 피로를 즉시 풀어주세요.",
            "50~60": "지방층 보호와 보온: 손을 따뜻한 물에 담가 혈액순환을 돕고 무리한 가사일 후에는 휴식하세요.",
            "70 이상": "균형 유지와 피부 관리: 손가락 마디 관절에 무리가 가지 않도록 가벼운 물건도 나누어 드세요."
        },
        "허리": {
            "10~20": "C자 곡선(요추 전만) 사수하기\n- 스마트폰 '눈높이' 노하우: 화면을 눈높이까지 올려서 보세요.\n- 바닥 앉기(좌식) 피하기: 바닥에 앉으면 디스크 압력이 2배 이상 높아집니다. 등받이 의자를 사용하세요.\n- 가방 무게 분산: 가방 무게는 몸무게의 10%를 넘지 않게 조절하세요.",
            "30~40": "디스크 압력 관리와 환경 개선\n- '모니터 암' 활용: 시선이 아래로 향하지 않게 모니터 상단을 눈높이에 맞추세요.\n- 5010 법칙: 50분 앉아 있었다면 반드시 10분은 일어나 움직이세요.\n- 운전 시 요추 받침대: 엉덩이와 등받이 사이 빈 공간에 쿠션을 사용하세요.",
            "50~60": "퇴행 지연과 생활 습관의 대전환\n- 물건 들 때 '무릎' 사용: 허리만 숙이지 말고 무릎을 굽혔다가 다리 힘으로 일어나세요.\n- 세수 및 머리 감기 자세: 가급적 샤워기를 이용해 서서 씻는 습관으로 바꾸세요.\n- 보온과 혈액순환: 배와 허리를 항상 따뜻하게 유지하세요.",
            "70 이상": "압박 골절 방지와 안전 확보\n- 재채기 요령: 무릎을 살짝 굽히거나 벽을 짚어 충격을 분산하세요.\n- 수면 시 베개 활용: 천장을 보고 누울 때는 무릎 밑에 베개를 넣어 허리 긴장을 푸세요."
        },
        "목": {
            "10~20": "거북목 탈출과 시선 처리\n- 스마트폰 '코 높이' 법칙: 시선이 아래로 향하는 것을 방지하기 위해 폰을 높이 드세요.\n- 엎드려서 책 보기 금지: 목 뒤쪽 근육을 극도로 긴장시켜 디스크 탈출의 원인이 됩니다.\n- 백팩 끈 조절: 가방을 등에 밀착시켜 목이 앞으로 굽는 것을 방지하세요.",
            "30~40": "업무 환경 재정비와 근육 경직 관리\n- 눈높이 모니터: 노트북 거치대를 활용해 고개를 들 수밖에 없는 환경을 만드세요.\n- 전화 통화 습관: 이어폰을 사용하세요. 어깨에 폰을 끼우는 자세는 치명적입니다.\n- 운전 시 헤드레스트 활용: 머리 뒷부분이 받침대에 살짝 닿게 하여 목 근육의 피로를 줄이세요.",
            "50~60": "보온과 수면 자세 개선\n- 맞춤 베개 찾기: 목의 C자 곡선을 받쳐주는 경추 베개를 활용하세요.\n- 목 보온: 찬바람으로부터 목을 보호하기 위해 스카프를 두르는 습관이 좋습니다.\n- 소파 팔걸이 베개 대용 금지: 딱딱한 팔걸이는 목 정렬을 망가뜨립니다.",
            "70 이상": "낙상 예방과 안전한 움직임\n- 급격한 고개 돌리기 금지: 몸 전체를 함께 돌리세요. 어지럼증을 유발할 수 있습니다.\n- 안경(다초점 렌즈) 주의: 계단을 내려갈 때 목의 각도에 특히 주의하세요.\n- 기상 시 롤링 기법: 옆으로 몸을 돌린 뒤 팔 힘을 이용해 천천히 일어나세요."
        }
    }

    # 3. 매칭 키워드 및 노하우 추출
    search_keywords = []
    if target_part == "발목발가락":
        search_keywords = ["발목", "발가락"]
    elif target_part == "손목손가락":
        search_keywords = ["손목", "손가락"]
    else:
        search_keywords = [target_part]

    # 노하우 가져오기
    part_key = target_part
    age_key = user_data["age"]
    exercise_comment = KNOWHOW_DB.get(part_key, {}).get(age_key, "해당 부위와 연령에 맞는 관리 가이드를 준비 중입니다.")

    # 4. 병원 매칭 및 데이터 가공
    for h in hospitals:
        relevant_reviews = []
        for r in reviews:
            if r["hospital_name"] == h["name"]:
                content = r.get("content", "")
                keywords_list = r.get("keywords") or []
                is_match = False
                for sk in search_keywords:
                    if sk in content or any(sk in k for k in keywords_list):
                        is_match = True
                        break
                if is_match:
                    relevant_reviews.append(r)
        
        if relevant_reviews:
            h_copy = h.copy()
            avg = calculate_average_rating(h["name"], reviews)
            h_copy["rating"] = avg if avg is not None else "평점 없음"
            h_copy["review_count"] = len([r for r in reviews if r["hospital_name"] == h["name"]])
            h_copy["part_review_count"] = len(relevant_reviews)
            h_copy["match_message"] = f"{target_part} 관련 리뷰가 {len(relevant_reviews)}개 있습니다."
            matched_hospitals.append(h_copy)

    # 5. 정렬
    matched_hospitals.sort(key=lambda x: (
        -x["part_review_count"], 
        x["rating"] == "평점 없음", 
        -(x["rating"] if x["rating"] != "평점 없음" else 0)
    ))

    exercise_video_url = "" # 추후 영상 매칭 시 사용

    return render_template(
        'diagnosis_result.html',
        user_data=user_data,
        hospitals=matched_hospitals,
        comment=exercise_comment,
        video_url=exercise_video_url
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