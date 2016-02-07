<?php
	/*
		Date: 2016-01-28
		Author: skkong89@gmail.com
		ex) http://angel.vps.phps.kr/data_analysis/getWeather.php?yy=2013&mm=1&stn=108
		ex) http://www.kma.go.kr/weather/observation/past_cal.jsp?stn=108&yy=2013&mm=1&x=23&y=8&obs=1
	*/

	//  날씨 조회 api

	function getWeather($yy, $mm, $stn)
	{
		$arr_data = array();

		$url = "http://www.kma.go.kr/weather/observation/past_cal.jsp?stn=$stn&yy=$yy&mm=$mm&obs=1&x=24&y=9";

		$results = "";
		$contents = file_get_contents($url);
		if($contents)
		{
			// euc-kr 페이지를 utf8로 변환한다.
			$contents = iconv('euc-kr', 'utf8', $contents);
		}


	    // <td class="align_left">평균기온:2.2℃<br />최고기온:3.7℃<br />최저기온:-0.3℃<br />평균운량:9.6<br />일강수량:0.0mm<br /></td>
        $regex = '/.*<td class="align_left">평균기온:(.*?)<br \/>최고기온:(.*?)<br \/>최저기온:(.*?)<br \/>평균운량:(.*?)<br \/>일강수량:(.*?)<br \/><\/td>.*/';

		// 라인단위로 분리
		$arr_line = explode("\n", $contents);

		$day = 1;		// 일 정보
		foreach($arr_line as $line)
		{
			if(strpos($line, "평균기온") > 0)
			{
				$line = str_replace("℃", "", $line);
				$line = str_replace("mm", "", $line);

        		preg_match ($regex , $line, $matches);

        		$arr_data[$day]['avg'] = $matches[1];		// 평균기온
        		$arr_data[$day]['high'] = $matches[2];	// 최고기온
        		$arr_data[$day]['low'] = $matches[3];		// 최저기온
        		$arr_data[$day]['cloud'] = $matches[4];	// 평균운량
        		$arr_data[$day]['rain'] = trim(str_replace("-", '0', $matches[5]));	// 일강수량

        		$day++;
			}

		}

		return $arr_data;

	}


	// main routine
	// ====================

	$yy = $_REQUEST['yy'];				// 년도
	$mm = $_REQUEST['mm']; 				// 월
	$stn = $_REQUEST['stn'];			// 지역

	$yy = $yy == '' ? date("Y") : $yy;
	$mm = $mm == '' ? date('m') : $mm;
	$stn = $stn == '' ? 108 : $stn;

	$arr_data = getWeather($yy, $mm, $stn);
	echo json_encode($arr_data);

?>
