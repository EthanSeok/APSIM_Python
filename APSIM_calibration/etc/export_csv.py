# 춘천과 강릉 기상 데이터 csv

from datetime import datetime
import json
import time
from urllib.parse import quote_plus, urlencode
import pandas as pd
import os
import requests
import tqdm
import xlsxwriter as xlsxwriter
from openpyxl import load_workbook


def load_data(stn_Ids, stn_Nm, output_dir, site_info, latitude, longitude):

    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    servicekey = 'HOhrXN4295f2VXKpOJc4gvpLkBPC/i97uWk8PfrUIONlI7vRB9ij088/F5RvIjZSz/PUFjJ4zkMjuBkbtMHqUg=='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                             'Safari/537.36'}


    list_dfs = []
    for y in range(2007, 2021):
        params = f'?{quote_plus("ServiceKey")}={servicekey}&' + urlencode({
            quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
            quote_plus("numOfRows"): "720",  # 한 페이지 결과 수 // default : 10
            quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
            quote_plus("dataCd"): "ASOS",
            quote_plus("dateCd"): "DAY",
            quote_plus("startDt"): f"{y}0101",
            quote_plus("endDt"): f"{y}1231",
            quote_plus("stnIds"): f"{stn_Ids}"
        })
        try:
            result = requests.get(url + params, headers=headers)
        except:
            time.sleep(2)
            result = requests.get(url + params, headers=headers)

        js = json.loads(result.content)
        weather = pd.DataFrame(js['response']['body']['items']['item'])
        weather['year'] = pd.to_datetime(weather['tm']).dt.year
        weather['month'] = pd.to_datetime(weather['tm']).dt.month
        weather['day'] = pd.to_datetime(weather['tm']).dt.day

        weather['date'] = pd.to_datetime(weather[['year', 'month', 'day']])
        # weather['day'] = weather['date'].dt.strftime('%j')

        # sumRn: 일강수량, sumGsr: 합계 일사량, sumSmlEv: 합계 소형증발량, avgTa: 평균기온, minTa: 최저기온, maxTa: 최고기온, sumSsHr: 일조시간, avgRhm: 평균상대습도
        # avgWs: 평균풍속
        # li = ['year', 'day', 'sumGsr', 'maxTa', 'minTa', 'sumRn', 'sumSmlEv', 'avgTa', 'avgRhm', 'avgWs', 'avgTca', 'sumSsHr','month']
        # li = ['year', 'day', 'sumGsr', 'maxTa', 'minTa', 'sumRn', 'sumSmlEv', 'avgTa', 'avgRhm', 'avgWs', 'avgTca', 'sumSsHr','month']
        li = ['tm', 'month', 'day', 'avgTa', 'avgRhm', 'avgWs', 'sumSsHr']
        weather = weather.loc[:, li]
        weather[['month', 'day', 'avgTa', 'avgRhm', 'avgWs', 'sumSsHr']] = weather[['month', 'day', 'avgTa', 'avgRhm', 'avgWs', 'sumSsHr']].apply(pd.to_numeric)
        list_dfs.append(weather)

    df = pd.concat(list_dfs)
    # df.columns = ['year', 'day', 'radn', 'maxt', 'mint', 'rain', 'evap', 'tavg', 'humid', 'wind', 'cloud', '', 'month']
    df.columns = ['날짜', '월', '일', '평균기온', '평균습도', '평균풍속', '일조시간']
    df['풍속계높이'] = 10
    # df['rain'] = df['rain'].fillna(0)
    # df['evap'] = df['evap'].fillna(0)
    # df['radn_c'] = df['']

    # tav = round(df.groupby('year').mean()['tavg'].mean(), 2)
    # amp = round((df.groupby('month').max()['tavg'] - df.groupby('month').min()['tavg']).mean(), 2)
    #
    # df.drop(columns = ['tavg', 'month'], inplace=True)

    # df.insert(0, 'site', site_info[site_info['행정구역'] == stn_Nm]['영문 표기'].values[0])
    # new_row = pd.DataFrame([['()', '()', '()', '(MJ/m2)', '(oC)', '(oC)', '(mm)', '(mm)']],
    #                        columns=df.columns)
    # df = pd.concat([df.iloc[:0], new_row, df.iloc[0:]], ignore_index = True)
    # filename = df['site'].values[1]
    filename = site_info[site_info['행정구역'] == stn_Nm]['영문 표기'].values[0]
    df.to_csv(os.path.join(output_dir, f"{filename}_weather.csv"))

    print(filename)

def main():
    output_dir = "../output/weather_csv/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    site_info = pd.read_excel('../input/한국행정구역분류.xlsx', sheet_name='1. 총괄표(현행)')
    site_info = site_info.rename(columns=site_info.iloc[1])
    site_info = site_info.drop(site_info.index[:2])
    site_info['영문 표기'] = site_info['영문 표기'].str.split('-').str[0]
    site_info[['시도', '시군구', '읍면동']] = site_info[['시도', '시군구', '읍면동']].fillna(" ")
    site_info['행정구역'] = site_info['시도'] + "_" + site_info['시군구'] + "_" + site_info['읍면동']
    site_info['행정구역'] = site_info['행정구역'].str.split(' ').str[0]
    site_info['행정구역'] = site_info['행정구역'].apply(lambda x: x.rstrip("_") if x.endswith("_") else x)

    station_code = pd.read_excel('../input/지점코드.xlsx')

    filenames_wheat = [x.strip(".csv") for x in os.listdir("../output/kosis/") if x.endswith(".csv")]

    s = ['강릉', '춘천']
    f = ['강원도_강릉시', '강원도_춘천시']
    n = []

    for i in tqdm.tqdm(range(len(s))):
        a = station_code[station_code['지점명'] == s[i]]
        if a.empty:
            n.append(f[i])
        else:
            # try:
            stn_Ids = a['지점코드'].values[0].item()
            stn_Nm = f[i]
            latitude = a['위도'].values[0].item()
            longitude = a['경도'].values[0].item()
            load_data(stn_Ids, stn_Nm, output_dir, site_info, latitude, longitude)

if __name__ == '__main__':
    main()

    # =21.8161 + J2 * 0.5515 - 0.0836 * H2 - 0.3103 * L2 - 0.1863 * K2 - 0.5177 * N2 - 0.2188 * M2
