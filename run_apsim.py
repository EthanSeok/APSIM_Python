import os
import subprocess
import shutil
import xml.etree.ElementTree as ET
import pandas as pd
import PySimpleGUI as sg


def run(met_list, s_date, e_date, apsim_file, output_element):
    inpath = 'C:/APSIM_Python/'
    os.chdir(inpath)

    '''apsim 파일 불러오기'''
    wheat_tree = ET.parse(apsim_file)
    root = wheat_tree.getroot()

    '''run.apsim 파일 내 met 경로 변경'''
    for i in range(len(met_list)):
        for node in root.iter('simulation'):
            node.attrib['name'] = met_list[i][20:-4]

            for metfile in node.iter('filename'):
                metfile.text = met_list[i]

            for s_clock in node.iter('start_date'):
                s_clock.text = s_date

            for e_clock in node.iter('end_date'):
                e_clock.text = e_date

        wheat_tree.write(apsim_file)  # apsim 파일 덮어 씌우기
        apsim_exe = f'C:/Program Files (x86)/APSIM710-r4218/Model/Apsim.exe "{apsim_file}"'  # apsim exe 경로 및 apsim 파일 선언
        subprocess.run(apsim_exe, stdout=open(os.devnull, 'wb'))  # apsim 파일 실행

        '''결과 파일 불러오기'''
        out_list = met_list[i][20:-4]
        out_file = pd.read_csv(f'C:/APSIM_Python/{out_list}.out', sep="\\s+", skiprows=[0, 1, 3], parse_dates=['Date'],
                               infer_datetime_format=True)
        output_element.print(out_list)
        output_element.print(f'{out_file} \n')
        output_element.update()  # Update the GUI window to display the printed output
        sg.popup_auto_close(f'{out_list} simulation completed.')


def main():
    '''met 파일 불러오기'''
    met_list = [f'C:\APSIM_Python\met\{x}' for x in os.listdir("met/") if x.endswith(".txt")]
    print('met 리스트 : \n', met_list)

    sg.theme('SandyBeach')

    layout = [
        [sg.Text('APSIM 설치 경로'), sg.InputText('C:/Program Files (x86)/APSIM710-r4218/Model/Apsim.exe "run.apsim"')],
        [sg.Text('APSIM 실행 파일'), sg.InputText('run.apsim')],
        [sg.Text('시뮬레이션 시작 날짜 (format: dd/mm/yyyy)'), sg.InputText('01/01/2007')],
        [sg.Text('시뮬레이션 종료 날짜 (format: dd/mm/yyyy)'), sg.InputText('31/12/2008')],
        [sg.Submit(), sg.Cancel()],
        [sg.Output(size=(80, 20), key='output')]  # Output element for displaying the printed output
    ]

    window = sg.Window('APSIM Python', layout, return_keyboard_events=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        if event == 'Submit':
            apsim_file = values[1]
            s_date = values[2]
            e_date = values[3]
            window['output'].update('')
            run(met_list, s_date, e_date, apsim_file,window['output'])

    window.close()


###########################################################################################################################################
# 폴더 정리

"""폴더선택"""
dir_path = 'C:\APSIM_Python'

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
    main()
    cached_listdir(dir_path)

    for item in global_cache[dir_path]:

        """추가할 확장자를 수동으로 리스트에 추가"""
        extList = ["sum", "out"]

        for i in range(0, len(extList)):
            moveFile(extList[i])
