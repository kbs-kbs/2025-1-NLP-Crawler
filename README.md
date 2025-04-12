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

## 권장 설치
1. uv 설치 (Powershell):
   - `Set-ExecutionPolicy RemoteSigned Process`
   - `irm https://astral.sh/uv/install.ps1 | iex`
2. `uv init --python 3.12`
4. `uv venv`
5. `uv add -r requirements.txt`
6. `uv sync`
7. `playwright install`


# 환경 설정 및 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `python pipeline.py`: 실행

# 또는
1. `uv run pipeline.py`: 가상환경 활성화 없이도 프로젝트 venv을 자동으로 인식하여 실행

# 도메인별로 따로 실행
1. `venv\Scripts\activate` 및 편집기에서 가상환경 활성화
2. `scrapy crawl dbpia -O csv/dbpia.csv`: dbpia 크롤링 + csv로 저장
3. `scrapy crawl riss -O csv/riss.csv`: riss 크롤링 + csv로 저장


# 코드
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/dbpia.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/scrpy_plwrt_demo/spiders/riss.py
- https://github.com/kbs-kbs/2025-1-NLP-Crawler/blob/main/pipeline.py
