# -*- coding: utf-8 -*-

import os,subprocess
import shutil
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import mean_squared_error



out_list = []

'''met 파일 불러오기'''
met_list = [f'C:\code\Apsim_2023\met\{x}'  for x in os.listdir("met/") if x.endswith(".txt")]
print('met 리스트 : \n', met_list)


inpath = 'C:/code/Apsim_2023/'
os.chdir(inpath)

'''apsim 파일 불러오기'''
wheat_tree = ET.parse('run.apsim')
root = wheat_tree.getroot()

'''run.apsim 파일 내 met 경로 변경'''
for i in range(len(met_list)):
    for node in root.iter('simulation'):
        node.attrib['name'] = met_list[i][23:-4]

        for metfile in node.iter('filename'):
            metfile.text = met_list[i]

    wheat_tree.write('run.apsim')                                                           # apsim 파일 덮어 씌우기
    apsim_exe = 'C:/Program Files (x86)/APSIM710-r4218/Model/Apsim.exe "run.apsim"'         # apsim exe 경로 및 apsim 파일 선언
    subprocess.run(apsim_exe, stdout=open(os.devnull, 'wb'))                                # apsim 파일 실행

    '''결과 파일 불러오기'''
    out_list = met_list[i][23:-4]
    out_file = pd.read_csv(f'C:/code/Apsim_2023/{out_list}.out',sep="\\s+" ,skiprows=[0, 1, 3],parse_dates=['Date'], infer_datetime_format=True)
    out_file['year'] = out_file['Date'].dt.year
    observation = pd.read_csv(f'C:/code/Apsim_2023/kosis/{out_list}.csv')

    # print(out_file)

    '''결과 파일 후처리'''
    kosis = observation[observation['item'] == '단위생산량']
    kosis = kosis.drop(columns=['lo1', 'lo2', 'lo3', 'item'])
    pred = out_file.drop(columns=['Date', 'biomass','grain_size','grain_protein', 'esw'])
    pred['yield']= pred['yield'] * 0.1
    pred = pred[pred['year'].isin(kosis['year'])]

    kosis = kosis.groupby(kosis['year'])['value'].mean()

    results = pd.merge(kosis, pred,how='inner', on='year')
    results = results.rename(columns={'value':'kosis_results', 'yield':'pred_results'})
    print(out_list)
    print(results)

    '''생산량 그래프 그리기'''
    if len(results['year']) != 1:
        index = np.arange(len(results["year"]))
        plt.figure(figsize=(15, 10))
        plt.barh(index, results['pred_results'])
        plt.title(f'{out_list} yield', fontsize=15)
        plt.xlabel('yield (kg/10a)', fontsize=15)
        plt.ylabel('Year', fontsize=15)
        plt.yticks(index, results["year"], fontsize=15)
        plt.savefig(f'C:/code/Apsim_2023/graph/bar/{out_list}.png')
        plt.close()


        '''모델 결과 비교 그래프'''
        y_pred = results['pred_results']
        obs = results['kosis_results']
        r, p = stats.pearsonr(obs, y_pred)
        rmse = np.sqrt(mean_squared_error(obs, y_pred))
        filename = f'C:/code/Apsim_2023/graph/scatter/ {out_list},  {r ** 2:.4f}, RMSE {rmse:.4f}.png'

        print(f'\n R2 {r ** 2:.4f}, ', end="")
        print(f'RMSE {rmse:.4f}')

        fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
        sns.regplot(x="pred_results", y="kosis_results", data=results, ax=ax,scatter_kws={"fc":"b", "ec":"b", "s":100, "alpha":0.3})
        fig.savefig (filename)

    else:
        print(out_list)
        # pass
###########################################################################################################################################
# 폴더 정리

"""폴더선택"""
dir_path = 'C:\code\Apsim_2023'

"""폴더내파일검사"""

global_cache = {}

def cached_listdir(path):
    res = global_cache.get(path)
    if res is None:
        res = os.listdir(path)
        global_cache[path] = res
    return res


def moveFile(ext):
    if item.rpartition(".")[2] == ext:
        """폴더이동"""
        # print(ext + "확장자를 가진 " + item)

        tDir = dir_path + '/' + ext
        # print(dir_path + '/' + item)

        if not os.path.isdir(tDir):
            os.mkdir(tDir)

        filePath = dir_path + '/' + item
        finalPath = tDir + '/' + item

        if os.path.isfile(filePath):
            shutil.move(filePath, finalPath)


if __name__ == '__main__':

    cached_listdir(dir_path)

    for item in global_cache[dir_path]:

        """추가할 확장자를 수동으로 리스트에 추가"""
        extList = ["sum", "out"]

        for i in range(0, len(extList)):
            moveFile(extList[i])
