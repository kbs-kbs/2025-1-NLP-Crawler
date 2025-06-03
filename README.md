최근 인공지능(AI)은 다양한 분야에서 핵심 연구 주제로 부상하며, 학제간 융합 연구가 활발히 이루어지고 있다. 예를 들어, 미디어커뮤니케이션 분야에서는 2010~2024년 학술지 논문을 텍스트 분석하여 AI가 미디어 환경과 커뮤니케이션 방식에 미치는 영향과 연구 트렌드를 분석한 바 있다. 교육 분야에서도 인공지능 교육의 연구 동향을 파악하기 위해 LDA(잠재 디리클레 할당, Latent Dirichlet Allocation) 기반 토픽모델링을 활용하여 주요 키워드와 연구 주제를 도출하였다. 이러한 연구들은 AI가 단일 기술적 영역을 넘어 사회, 교육, 산업 등 다양한 분야와 융합되어 새로운 연구 지형을 형성하고 있음을 보여준다.

특히 “토픽모델링을 이용한 초등학생 인공지능 교육의 국내 연구동향”과 같은 논문에서는 2014년부터 2021년까지 발표된 논문 314편을 수집하여, LDA 토픽모델링으로 연구 동향을 분석하였다. 여기서는 학교 현장 기반 AI 리터러시, 챗봇 설계, 융합인재 교육, 인간-AI 협업 등 네 가지 주요 토픽을 도출하고, 향후 연구 방향을 제안하였다. 이외에도 국내 인공지능 분야 전체의 연구 동향을 파악하기 위해 토픽모델링과 의미연결망 분석을 결합한 연구도 이루어지고 있다.

기존의 인공지능 관련 동향 분석 논문들은 다음과 같은 방법론을 주로 활용해왔다.
키워드 빈도 분석: 논문 제목, 초록, 키워드에서 출현 빈도를 분석하여 주요 연구 주제를 도출.
토픽모델링(LDA 등): 대량의 논문 텍스트에서 잠재적 연구 토픽을 추출하여 연구 흐름과 주제 간 관계를 파악.
의미연결망 분석: 키워드 간의 연관성을 시각화하여 연구 분야 내 주요 이슈와 트렌드를 파악.
연도별, 분야별 분류: 논문을 연도, 학술지, 연구 방법 등 기준으로 분류해 시계열적 변화와 연구 유형을 분석.
예를 들어, 생성형 AI와 교육 분야 연구 동향 분석에서는 논문 제목, 연도, 학술지, 연구 방법, 핵심 키워드 등을 정리한 뒤, ChatGPT 등 AI 도구를 활용해 키워드 빈도, 논문 유형, 연도별 추이 등을 분석하였다.

기존 연구들은 주로 교육, 미디어, 산업 등 다양한 분야에서 인공지능의 활용 동향을 분석해왔으나, 본 논문은 임상의학 분야에 특화된 인공지능 연구 동향을 집중적으로 분석한다는 점에서 차별성을 가진다. 특히 PubMed에서 수집한 임상의학 논문 초록을 기반으로, AI·딥러닝·머신러닝 관련 키워드를 중심으로 데이터 전처리 및 단어 모음(코퍼스)을 구축한다. 이후, 본 논문에서는 기존의 키워드 빈도 분석을 넘어 LDA 토픽모델링을 활용하여 특정 질병명과 AI 알고리즘·모델명 간의 연관성을 연도별로 추출한다. 이를 통해 임상의학 분야에서 어떤 질병에 어떤 AI 기술이 어떻게 활용·연구되어 왔는지, 그리고 그 변화 양상이 어떻게 진화해왔는지를 체계적으로 분석한다. 이러한 접근은 기존의 단순 빈도 분석이나 키워드 네트워크 분석보다 더 심층적이고 구조적인 연구 동향 파악을 가능하게 한다.

결론적으로, 본 논문은 임상의학 분야의 인공지능 연구 동향을 정량적·정성적으로 분석하고, 토픽모델링을 통한 질병-알고리즘 연관성의 시계열적 변화까지 포괄적으로 조망한다는 점에서 기존 학제간 연구 동향 분석 논문과 차별화된다.








![python](https://img.shields.io/badge/python-3.12.10-blue)

# Scrapy-playwright를 통한 dbpia 및 riss 크롤링 도구
- 셀레니움보다 훨씬 간결한 코드 사용 가능
- splash 서버를 이용하는 것보다 간편하게 사용 가능
- dbpia + riss를 한번에 크롤링 후 합집합을 저장

# 📦 설치 방법
프로젝트를 로컬 환경에 설치하려면 깃을 실행한 뒤 다음 명령어를 입력합니다:
```bash
git clone https://github.com/kbs-kbs/2025-1-NLP-Crawler.git
```

# 초기 환경 설정
## 최소 의존성 설치
1. 파이썬 3.12.10 설치 (Winget):
   - `winget install --id=Python.Python.3.13 -e`
2. `temp\configurator.bat`
3. `python3.13 -m venv venv`
4. `venv\Scripts\activate` 및 편집기에서 가상 환경 활성화
5. `pip3.13 install -r requirements.txt`
6. `playwright install`
2. `uv init --p 3.12`


## 권장 설치
1. uv 설치 (Powershell):
   ```
   Set-ExecutionPolicy RemoteSigned Process
   ```
   ```
   irm https://astral.sh/uv/install.ps1 | iex
   ```
2. 의존성 설치 (CMD):
   ```
   uv sync
   ```
3. scrapy playwright 설치 (CMD):
   ```
   uv run playwright install
   ```


# 환경 설정 및 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `python pipeline.py`: 실행

# 또는
1. `uv run pipeline.py`: 가상환경 활성화 없이도 프로젝트 venv을 자동으로 인식하여 실행

# 도메인별로 따로 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `uv run scrapy crawl dbpia -O csv/dbpia.csv`: dbpia 크롤링 + csv로 저장
3. `uv run scrapy crawl riss -O csv/riss.csv`: riss 크롤링 + csv로 저장
4. `uv run scrapy crawl advanced_dbpia -O csv/advanced_dbpia.csv`: dbpia 크롤링 + csv로 저장


# 코드
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/dbpia.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/riss.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/pipeline.py
