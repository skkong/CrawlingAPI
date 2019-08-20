# coding=utf-8
#
# Date: 2016-01-26
# Author: skkong89@gmail.com
# 기상청 과거 날씨 정보 조회 프로그램
# www.kma.go.kr/weather/climate/past_cal.jsp?stn=108&yy=2013&mm=1&obs=1&x=24&y=9
#
# ex)2013년도 1월달 기온 정보를 조회한다. (년도, 월, 지역코드: 서울 108)
# dict_month = getWeather(2013, 1, 108)
#
import urllib
import re

# 특정년도, 월에 대한 날씨 정보 조회
def getWeather(year, mm, stn = "108"):
    obs = 1
    x = 24
    y = 9

    # 기상청 조회 url 설정 (python3.5)
    url = "http://www.kma.go.kr/weather/climate/past_cal.jsp?stn=" + stn + "&yy=" + year + "&mm=" + mm + "&obs=1&x=24&y=9"

    # 읽기 버퍼 설정
    lines = []

    # 자료 읽기
    f = urllib.request.urlopen(url)
    r = f.read()
    f.close()

    # 한글로 디코딩함
    r2 = r.decode('euc-kr', 'ignore')

    # 엔터키 값으로 라인을 구분함
    lines = r2.split('\n')

    # <td class="align_left">평균기온:2.2℃<br />최고기온:3.7℃<br />최저기온:-0.3℃<br />평균운량:9.6<br />일강수량:0.0mm<br /></td>
    regex = '.*<td class="align_left">평균기온:(.*?)<br \/>최고기온:(.*?)<br \/>최저기온:(.*?)<br \/>평균운량:(.*?)<br \/>일강수량:(.*?)<br \/><\/td>'

    dict_month = {}   # {1 => {평균기온: xx, 최고기온: yy, 최저기온: zz, 평균운량: kk, 일강수량: ll}, 2 => ...}
    day = 1
    for l in lines:
        if not '평균기온' in l: continue

        # 불필요한 문자는 제거함
        l = l.replace("℃", "")

        # 정규식 검사를 한다.
        l_reg = re.match(regex, l)
        if not l_reg: continue

        # 일자별 딕셔너리 객체 초기화
        dict_day = {'avg':0, 'high':0, 'low':0, 'cloud':0, 'rain':0}
        #[print(a) for a in l_reg.groups()]

        data_avg = l_reg.groups()[0]     # 평균기온
        data_high = l_reg.groups()[1]    # 최고기온
        data_low = l_reg.groups()[2]     # 최저기온
        data_cloud = l_reg.groups()[3]   # 평균운량
        data_rain = l_reg.groups()[4]    # 일강수량

        dict_day['avg'] = data_avg     # 평균기온
        dict_day['high'] = data_high    # 최고기온
        dict_day['low'] = data_low     # 최저기온
        dict_day['cloud'] = data_cloud   # 평균운량
        dict_day['rain'] = data_rain.replace("-", "0").replace("mm", "")    # 일강수량

        dict_month[day] = dict_day
        day = day + 1

    return (dict_month)


# 조회년도, 월, 지역코드 설정
year = "2013"
mm = "2"
stn = "108"

# 2013년도 1월달 기온 정보를 조회한다.
dict_month = getWeather(year, mm, stn)

# 기온정보 출력: 일자, 평균기온, 최고기온, 최저기온, 평균운량, 일강수량
for (day, dict_day) in dict_month.items():
    print ("{0}{1}{2}, {3}, {3}, {4}, {5}, {6} ".format(year, mm.zfill(2), str(day).zfill(2), dict_day['avg'], dict_day['high']
        , dict_day['low'], dict_day['cloud'], dict_day['rain']))





