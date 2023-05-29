모델링 - 참조 글
* [모델링 - 여러가지 작물생육 모델 돌려보기 -1부](https://ethanseok.github.io/2023-03-01/crop_model1-post)
* [모델링 - 여러가지 작물생육 모델 돌려보기 -2부](https://ethanseok.github.io/2023-03-02/crop_model2-post)

<br>

## APSIM

* APSIM은 The Agricultural Production Systems sIMulator의 약자로 
농업 시스템 의 생물물리학적 과정을 시뮬레이션하기 위해 개발된 포괄적인 모델로, 특히 기후 위험에 직면한 관리 관행의 경제적 및 생태학적 결과와 관련이 있다.


* 식량 안보, 기후 변화 적응 및 완화, 탄소 거래 문제 영역에 대한 옵션과 솔루션을 탐색하는 데 사용되고 있다.


* APSIM은 식물, 토양 및 관리 모듈을 중심으로 구성되며, 이러한 모듈에는 다양한 범위의 작물, 물 균형을 포함한 토양 공정, 
N 및 P 변환, 토양 pH, 침식 및 모든 범위의 관리 제어 가능.

<br>

### APSIM 설치 방법

<img width="1213" alt="image" src="https://user-images.githubusercontent.com/93086581/222314434-85c14384-305c-463c-888e-250cd985f8d0.png">

* GUI: [https://registration.apsim.info/](https://registration.apsim.info/)에서 설치 가능 (2023.02 기준 Apsim7.10-r4218 버전 설치)

<br>

<br>

## APSIM Python

**본 APSIM Python은 기존 GUI 인터페이스의 APSIM에서 사이트 별로 모두 별도로 돌려야 했던 단점을 커버함과 동시에 캘리브레이션을 효율적으로 하기 위한 목적으로 개발되었다.**

### 설치 및 사용 방법

[여기에서 설치](https://drive.google.com/file/d/1umtgLz-Ka9PkoTwLDwIsJBmdkmGTe1tT/view?usp=sharing)

다운 받은 파일의 압축을 풀면 생성되는 `APSIM_Python` 폴더를 **반드시  C 드라이브 root에 설치해야 한다. 절대 경로는 C:\ 이다.
C드라이브 root에 설치하지 않으면 실행시 오류가 발생하므로 주의하자.**

<br>

#### APSIM_Python 구성요소
* met - 모델 입력자료 (기상자료)

* run.apsim (APSIM Setting 파일)

* run_apsim.exe (APSIM Python 실행 파일)

<br>

#### met 폴더

met 파일이란 APSIM 모델을 시뮬레이션을 위한 사이트 정보와 기상자료를 모델에서 요구하는 형식에 맞추어 정리된 파일이다. 


![met 폴더](https://github.com/EthanSeok/APSIM_Python/assets/93086581/7a39cf99-36c1-4e10-b78d-b7a3c1d2e41c)


![met 파일 예시](https://github.com/EthanSeok/APSIM_Python/assets/93086581/710e762c-2c91-43b4-b522-a5d014f17244)

<br>

#### run.apsim

run.apsim 파일은 APSIM 시뮬레이션 config 파일이라 이해하면 된다. 각종 시뮬레이션 옵션을 컨트롤 하는 중요한 파일이다. APSIM 파일의 구성 요소와 
적용방법은 추후에 정리할 예정이다.

![apsim 파일 예시](https://github.com/EthanSeok/APSIM_Python/assets/93086581/e4819538-2ee1-4219-93fd-2ceb11f128d2)

<br>

#### run_apsim.exe

APSIM Python을 실행하는 파일이다. 실행시 GUI 인터페이스가 출력되며, APSIM 설치 경로와 apsim 파일 위치 그리고 시뮬레이션하고자 하는 날짜를 넣어주면 된다.

<br>

run_apsim.exe 실행시 다음과 같은 화면이 출력된다. 해당 화면은 met 폴더에 들어있는 파일들의 목록을 출력한다.

![터미널](https://github.com/EthanSeok/APSIM_Python/assets/93086581/f6a24176-4a4d-4739-b8ff-759513683aa5)

<br>

run_apsim.exe 실행시 다음과 같은 GUI 인터페이스가 출력된다. 차례로 정보를 입력한 뒤에 `submit`을 클릭하여 실행하면 된다.

![GUI](https://github.com/EthanSeok/APSIM_Python/assets/93086581/6ef89183-693e-49ac-872e-0dfc40a084c7)

<br>

정상적으로 실행 되면 다음과 같이 output이 출력되고, 시뮬레이션 완료시 팝업이 출력된다. 팝업은 일정시간이 지나면 자동으로 없어지니 별다른 클릭을 하지 않아도 된다.

![실행 화면](https://github.com/EthanSeok/APSIM_Python/assets/93086581/5c697d67-81ad-4a1d-b4dc-9e12bcadf2c4)

<br>

정상적으로 실행 시 여러 사이트를 다음과 같이 한번에 시뮬레이션할 수 있다는 것이 장점이다.

![image](https://github.com/EthanSeok/APSIM_Python/assets/93086581/f23f3e22-9679-41a3-b2ca-67c022f862d3)

<br>

시뮬레이션 진행 시 다음과 같이 시뮬레이션 과정을 정리해준 파일인 summary (.sum) 파일과 결과 파일인 .out 파일이 생성된다.
![image](https://github.com/EthanSeok/APSIM_Python/assets/93086581/6dde7333-59f2-49fd-8786-7e259361e467)

<br>

시뮬레이션 종료시 `cancle`을 클릭하면 GUI가 종료되고, .sum 파일과 .out 파일이 각 이름의 폴더가 새롭게 생성되고 자동으로 정리된다.

![GUI](https://github.com/EthanSeok/APSIM_Python/assets/93086581/6ef89183-693e-49ac-872e-0dfc40a084c7)