import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode # query_params 딕셔너리를 query_string으로 변환하기 위한 표준 라이브러리
import time # 디버깅을 위한 표준 라이브러리
import math
from scrpy_plwrt_demo.items import ThesisItem # ThesisItem 모델

class RissSpider(scrapy.Spider):
    name = 'riss'
    allowed_domains = ['www.riss.kr']

    def __init__(self, keyword, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.query_params = {
            'isDetailSearch': 'Y', # 상세 검색 사용
            'searchGubun': 'true',
            'viewYn': 'CL', # 검색 결과 좁혀 보기: 닫음
            'query': '', # 상세 검색에서는 쓰지 않음
            'queryText': f'znTitle,{self.keyword}@op,OR@znSubject,{self.keyword}@op,OR@znAbstract,{self.keyword}@op,OR@znKtoc,{self.keyword}', # 상세 검색 사용
            'p_year1': '',
            'p_year2': '',
            'iStartCount': 0, # 이전 페이지까지의 논문 수 (100개씩 출력에서 2번째 페이지로 이동하면 100이 됨)
            'iGroupView': 5,
            'icate': 're_a_kor', # 이전 페이지: 국내학술논문
            'colName': 're_a_kor', # 현재 페이지: 국내학술논문
            'order': '/DESC', # 내림차순
            'onHanja': 'true', # 한글로 보기 (true로 해야 한글로 보임)
            'strSort': 'RANK', # 정확도순
            'pageScale': 100 # 100개씩 출력
        }
        self.max_pages = 0
        self.crawled_pages = 0
        self.start_time = time.time()

    def start_requests(self):
        query_string = urlencode(self.query_params)
        yield scrapy.Request(
            url='https://www.riss.kr/search/Search.do?' + query_string,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "timeout": 200000,
                    "wait_until": "domcontentloaded"
                },
            },
            callback=self.parse
        )

    async def parse(self, first_response):
        # 최초 응답을 저장
        response = first_response
        page = response.meta["playwright_page"]
        total = 0

        # 논문 개수 추출하여 총 페이지 수 계산
        try:
            total = int(response.css('#divContent > div > div.rightContent > div > div.searchBox > dl > dd > span > span::text').get().replace(',', ''))
        except TypeError:
            return
        self.max_pages = math.ceil(total/100)
        self.inform('논문 개수', total, '최대 페이지 수', self.max_pages)

        # 마지막 페이지까지 크롤링 반복
        while True:
            items = response.css('#divContent > div > div.rightContent > div > div.srchResultW > div.srchResultListW > ul > li')
            for item in items:
                thesis = ThesisItem()
                thesis['title'] = ''.join(item.css(f'div.cont > p.title > a *::text').getall())
                thesis['issue_year'] = item.css(f'div.cont > p.etc > span:nth-child(3)::text').get()
                abstract = item.css(f'div.cont > p.preAbstract::text').get()
                thesis['abstract'] = abstract.replace('\n', '').replace('\t', '').replace('\r', '') if abstract else None
                thesis['link'] = 'https://www.riss.kr' + item.css(f'div.cont > p.title > a::attr(href)').get()
                self.inform('제목', thesis['title'], '발행 연도', thesis['issue_year'], '초록', thesis['abstract'], '링크', thesis['link'])

                yield thesis

            self.crawled_pages += 1
            self.inform('완료한 페이지', self.crawled_pages)

            # 완료한 페이지가 최대 페이지와 동일할 경우 반복 종료
            if self.crawled_pages == self.max_pages:
                break
            
            # 크롤링할 페이지가 남아 있을 경우 다음 페이지 번호 클릭
            await self.click_next_button(page)
            await page.wait_for_load_state('load')

            # 바뀐 페이지로 응답 객체를 생성 후 업데이트
            content = await page.content()
            response = response.replace(body=content)

    # 버튼 클릭 함수
    async def click_next_button(self, page):
        next_button = await page.query_selector(f'#divContent > div > div.rightContent > div > div.paging > a.num.on + a')
        await next_button.click()

    # 디버깅을 위한 로그 출력 함수
    def inform(self, name, value, *args):
        info = { name: value }
        if args:
            info.update({ args[i]: args[i + 1] for i in range(0, len(args), 2) })
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
