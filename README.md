# weatherapi

기상청 과거 날씨를 조회하는 api 입니다.
실제 기상청 과거 날씨는 다음 url 에서 확인이 가능합니다.

http://www.kma.go.kr/weather/observation/past_cal.jsp?stn=108&yy=2013&mm=1&x=23&y=8&obs=1

이 페이지에서 날짜에 해당하는 평균기온, 최고기온, 최저기온, 평균운량, 일강수량을 html parsing 하고 json 포맷으로 응답합니다.
지역에 해당하는 코드는 stn 이고 108은 서울을 의미합니다. 지역코드는 위의 기상청 페이지를 참조 바랍니다.

호출예제:
ex) http://angel.vps.phps.kr/data_analysis/getWeather.php?yy=2013&mm=1&stn=108

