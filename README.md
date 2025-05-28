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

네, 지적해주셔서 감사합니다. 신약 개발을 제외하고, **임상의학**에 초점을 맞춰 인공지능(AI) 기술이 어떻게 활용되고 있는지 최근 5년간 연구동향을 분석하는 글을 아래와 같이 작성해드립니다.

---

텍스트 마이닝은 비정형 텍스트 데이터에서 의미 있는 정보를 추출하는 기법으로 산업, 의료, 금융, 정책, 마케팅 등 다양한 분야에서 데이터 기반 의사결정을 내리고 후속 연구의 발판을 마련하는 데 활용되고 있다. 그 예로 배홍철(2025)의 연구에서는 토픽 모델링 방법으로 미술계 온라인 커뮤니티 '네오룩'의 아카이브 52,111건(2000-2024년)을 분석하여 동시대 미술계의 지형을 탐색하였다. 또한 ~에서는 ~방법으로 ~를 분석하였다. 주요 분석 방법으로는 단어 빈도 분석: 특정 용어나 키워드의 출현 빈도를 집계하여 주요 관심사를 파악
토픽 모델링(LDA 등): 대량의 텍스트에서 잠재적인 주제(Topic)를 자동 추출하는 비지도 학습 기법으로, 임상 연구 주제의 자동 분류 및 트렌드 분석
연결망 분석(Network Analysis): 추출된 키워드 또는 개념 간의 관계망을 구축하여, 영향력 있는 주제어 및 그 구조적 특성을 분석
자연어처리(NLP) 기반 개념 추출: 의료 텍스트에서 의학용어 또는 개념을 자동 추출하는 방법(예: MetaMap, cTAKES 등)을 통해 임상 데이터의 구조화와 분석에 활용
텍스트 임베딩 및 기계학습: 텍스트를 벡터로 변환(임베딩)한 후, 분류·예측 등 기계학습 모델에 적용하여 임상적 의사결정 지원, 진단, 예후 예측 등에 활용