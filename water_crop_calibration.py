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
import tqdm

all_site = []
all_year = []
all_yield = []

out_list = []

'''met 파일 불러오기'''
met_list = [f'C:\code\Apsim_2023_water\met\{x}'  for x in os.listdir("met/") if x.endswith(".txt")]
print('met 리스트 : \n', met_list)


inpath = 'C:/code/Apsim_2023_water/'
os.chdir(inpath)

'''apsim 파일 불러오기'''
wheat_tree = ET.parse('run_water.apsim')
root = wheat_tree.getroot()

'''water param list'''
# ll15s = np.arange(0.0, 0.5, 0.1).tolist()
# duls = np.arange(0.0, 1.0, 0.2).tolist()
# sats = np.arange(0.0, 1.0, 0.2).tolist()
ll15s = [0.29]
duls = [0.5]
sats = [0.5]
'''run.apsim 파일 수정'''
for i in tqdm.tqdm(range(len(met_list))):
    for ll15 in ll15s:
        for dul in duls:
            for sat in sats:
                for node in root.iter('simulation'):
                    node.attrib['name'] = met_list[i][29:-4]

                    for metfile in node.iter('filename'):
                        metfile.text = met_list[i]

                    for node_water in node.iter('LL15'):
                        child_node = node_water.iter("double")
                        for x, child in enumerate(child_node):
                            if x < 3:
                                child.text = str(round(ll15, 3))

                    for node_water in node.iter('DUL'):
                        child_node = node_water.iter("double")
                        for x, child in enumerate(child_node):
                            if x < 3:
                                child.text = str(round(dul, 3))

                    for node_water in node.iter('SAT'):
                        child_node = node_water.iter("double")
                        for x, child in enumerate(child_node):
                            if x < 3:
                                child.text = str(round(sat, 3))

                wheat_tree.write('run_water.apsim')                                                           # apsim 파일 덮어 씌우기
                apsim_exe = 'C:/Program Files (x86)/APSIM710-r4218/Model/Apsim.exe "run_water.apsim"'         # apsim exe 경로 및 apsim 파일 선언
                subprocess.run(apsim_exe, stdout=open(os.devnull, 'wb'))                                      # apsim 파일 실행

                '''결과 파일 불러오기'''
                out_list = met_list[i][29:-4]
                out_file = pd.read_csv(f'C:/code/Apsim_2023_water/{out_list}.out',sep="\\s+" ,skiprows=[0, 1, 3],parse_dates=['Date'], infer_datetime_format=True)
                out_file['year'] = out_file['Date'].dt.year
                observation = pd.read_csv(f'C:/code/Apsim_2023_water/kosis/{out_list}.csv')

                # print(out_file)

                '''결과 파일 후처리'''
                kosis = observation[observation['item'] == '단위생산량']
                kosis = kosis.drop(columns=['lo2', 'lo3', 'item'])
                pred = out_file.drop(columns=['Date', 'biomass','grain_size','grain_protein', 'esw'])
                pred['yield']= pred['yield'] * 0.1   # ha --> 10a
                pred = pred[pred['year'].isin(kosis['year'])]

                kosis_yield = kosis.groupby(kosis['year']).mean().reset_index()
                results = pd.merge(kosis_yield, pred,how='inner', on='year')
                results = pd.merge(kosis[['lo1', 'year']],results, how='inner', on='year').drop_duplicates()

                results = results.rename(columns={'lo1':'시도','value':'kosis_results', 'yield':'pred_results'})
                results.to_csv(f'{out_list}_out.csv')
                all_site.append(results['시도'].values)
                all_year.append(results['year'].values)
                all_yield.append(results['pred_results'].values)
                print(out_list, f'LL15: {ll15:.3f}  DUL: {dul:.3f}  SAT: {sat:.3f}')
                print(results)

                '''생산량 그래프 그리기'''
                bar_path = f'C:/code/Apsim_2023_water/graph/bar/{out_list}'
                if not os.path.exists(bar_path):
                    os.makedirs(bar_path)

                if len(results['year']) != 1:
                    index = np.arange(len(results["year"]))
                    plt.figure(figsize=(15, 10))
                    plt.barh(index, results['pred_results'], height = 0.7)
                    plt.title(f'{out_list} yield', fontsize=15)
                    plt.xlabel('yield (kg/10a)', fontsize=15)
                    plt.ylabel('Year', fontsize=15)
                    plt.yticks(index, results["year"], fontsize=15)
                    plt.xlim(0, 900)
                    plt.savefig(os.path.join(f'{bar_path}', f'{out_list}, LL15_{ll15:.3f}, DUL_{dul:.3f}, SAT_{sat:.3f}.png'))
                    plt.close()


                    '''모델 결과 비교 그래프'''
                    scatter_path = f'C:/code/Apsim_2023_water/graph/scatter/{out_list}'
                    if not os.path.exists(scatter_path):
                        os.makedirs(scatter_path)

                    y_pred = results['pred_results']
                    obs = results['kosis_results']
                    r, p = stats.pearsonr(obs, y_pred)
                    rmse = np.sqrt(mean_squared_error(obs, y_pred))
                    filename = os.path.join(f'{scatter_path}', f'{out_list}, LL15_{ll15:.3f}, DUL_{dul:.3f}, SAT_{sat:.3f}, R2_{r ** 2:.4f}, RMSE_{rmse:.4f}.png')

                    print(f'\n R2 {r ** 2:.4f}, ', end="")
                    print(f'RMSE {rmse:.4f}')

                    fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
                    sns.regplot(x="pred_results", y="kosis_results", data=results, ax=ax,scatter_kws={"fc":"b", "ec":"b", "s":100, "alpha":0.3})
                    plt.xlim(0,900)
                    plt.ylim(0,900)
                    fig.savefig (filename)

                else:
                    print(out_list)

'''결과 정리'''
scores = []
site = [x for x in os.listdir("C:/code/Apsim_2023_water/graph/scatter/")]
for i in range(len(site)):
    score = [x for x in os.listdir(f"C:/code/Apsim_2023_water/graph/scatter/{site[i]}")]
    scores.extend(score)

scores = pd.DataFrame(scores, columns=['site'])
scores = scores['site'].str.split(', ', expand=True)
scores.columns = ['site', 'LL15', 'DUL', 'SAT', 'R2', 'RMSE']
scores = scores[scores['R2'].str[3:] != 'nan']
scores['RMSE'] = scores['RMSE'].str[5:-4].astype('float')
scores = scores.sort_values(by=['RMSE'])
scores.to_csv('C:/code/Apsim_2023_water/graph/results.csv')
print(scores.head(10))

'''시도별 정리'''
res = {'시도':[], '연도':[], '단위생산량':[]}
for i in range(len(all_site)):
    res['시도'].extend(all_site[i])
    res['연도'].extend(all_year[i])
    res['단위생산량'].extend(all_yield[i])

res = pd.DataFrame(res)
# res = res.groupby(['시도','연도'])['단위생산량'].mean().reset_index()
# res = pd.merge(res_mean, res[['시도', '연도']], how='inner', on='연도').drop_duplicates()

print(res.head(20))
res.to_csv('시도별_결과.csv', index=False)


###########################################################################################################################################
# 폴더 정리

"""폴더선택"""
dir_path = 'C:\code\Apsim_2023_water'

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
        extList = ["sum", "out", "csv"]

        for i in range(0, len(extList)):
            moveFile(extList[i])

