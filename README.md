![python](https://img.shields.io/badge/python-3.13.2-blue)

# Scrapy-playwright를 통한 dbpia 및 riss 크롤링 도구
- 셀레니움보다 훨씬 간결한 코드 사용 가능
- splash 서버를 이용하는 것보다 간편하게 사용 가능
- dbpia + riss를 한번에 크롤링 후 합집합을 저장

# 📦 설치 방법
프로젝트를 로컬 환경에 설치하려면 깃을 실행한 뒤 다음 명령어를 입력합니다:
```bash
git clone https://github.com/kbs-kbs/2025-1-NLP-Crawler.git
```

# 최초 환경 설정
1. `winget install --id=Python.Python.3.13 -e`
2. `configurator.bat`
3. `python3.13 -m venv venv`
4. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
5. `pip3.13 install -r requirements.txt`
6. `playwright install`

# 환경 설정 및 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `python pipeline.py`: 실행

# 도메인별로 따로 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `scrapy crawl dbpia -O csv/dbpia.csv`: dbpia 크롤링 + csv로 저장
3. `scrapy crawl riss -O csv/riss.csv`: riss 크롤링 + csv로 저장


# 코드
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/dbpia.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/riss.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/pipeline.py
