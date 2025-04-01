import scrapy
from scrapy_playwright.page import PageMethod # Playwright 페이지 조작을 위한 모듈
import time # 실행 시간 측정용
import math # 페이지 계산용
from scrpy_plwrt_demo.items import ThesisItem # 데이터 저장을 위한 아이템 클래스

class DbpiaSpider(scrapy.Spider):
    name = 'dbpia' # 스파이더 이름
    allowed_domains = ['www.dbpia.co.kr'] # 허용 도메인

    def __init__(self, keyword, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = keyword # 사용자 검색어
        self.node_ids = [] # 수집할 논문 노드 ID 저장 리스트
        self.max_pages = 0 # 최대 페이지 수
        self.pages_crawled = 0 # 현재 크롤링 완료 페이지 수
        self.start_time = time.time() # 실행 시작 시간 기록

    def start_requests(self):
        # 초기 요청 생성 (Playwright 설정 포함)
        yield scrapy.Request(
            url=f'https://www.dbpia.co.kr/search/topSearch?searchOption=all&query={self.query}#a',
            meta={
                "playwright": True, # Playwright 활성화
                "playwright_include_page": True, # 페이지 객체 포함
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#totalCount") # 총 논문 수 요소 대기
                ],
                "playwright_page_goto_kwargs": {
                    "timeout": 200000, # 페이지 로딩 타임아웃 200초
                    "wait_until": "domcontentloaded" # 로딩 완료 조건
                },
            },
            callback=self.parse_node_count # 콜백 함수 지정
        )

    async def parse_node_count(self, response):
        # 총 논문 수 파싱
        node_count = int(response.css('#totalCount::text').get().replace('건', '').replace(',', ''))
        self.inform('논문 개수', node_count)

        page = response.meta["playwright_page"]
        if node_count == 0:
            return # 결과 없으면 종료
        elif node_count > 20:
            # 100개씩 보기 설정 (페이지네이션 최적화)
            self.max_pages = math.ceil(node_count/100)
            await page.wait_for_selector('#selectWrapper')
            element = await page.query_selector('#selectWrapper')
            await element.click() # 페이지당 표시 수 드롭다운 클릭
            await page.wait_for_selector('#get100PerPage')
            element = await page.query_selector('#get100PerPage')
            await element.click() # 100개 선택
        else:
            self.max_pages = 1
        await page.wait_for_load_state('load') # 새 설정 적용 대기
        updated_html = await page.content() # 업데이트된 HTML 가져오기
        self.inform('최대 페이지 수', self.max_pages)

        # 페이지 순회 로직
        while True:
            new_response = scrapy.http.HtmlResponse( # 새 HTML 응답 객체 생성
                url=response.url,
                body=updated_html,
                encoding="utf-8",
                request=response.request
            )
            self.parse_node_ids(new_response) # 노드 ID 추출

            if self.pages_crawled < self.max_pages:
                await self.click_next_button(page) # 다음 페이지 버튼 클릭
                await page.wait_for_load_state('load')
                updated_html = await page.content()
            else: break
        
        # 수집된 노드 ID 기반 상세 페이지 요청 생성
        for node_id in self.node_ids:
            if 'NODE' in node_id:
                yield scrapy.Request( # 학술지 세부 페이지 요청
                    url=f'https://www.dbpia.co.kr/journal/articleDetail?nodeId={node_id}',
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_goto_kwargs": {
                            "timeout": 200000,
                            "wait_until": "domcontentloaded"
                        }
                    },
                    callback=self.parse_article_detail_page
                )
            else:
                yield scrapy.Request( # 일반 세부 페이지 요청
                    url=f'https://www.dbpia.co.kr/journal/detail?nodeId={node_id}',
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_goto_kwargs": {
                            "timeout": 200000,
                            "wait_until": "domcontentloaded"
                        }
                    },
                    callback=self.parse_detail_page
                )

    def parse_node_ids(self, response):
        # 노드 ID 추출 및 페이지 완료 카운트
        self.node_ids += response.css('#searchResultList section.thesisAdditionalInfo.thesis__info::attr(data-nodeid)').getall()
        self.pages_crawled += 1
        self.inform('완료한 페이지', self.pages_crawled, '노드 리스트', self.node_ids)

    async def click_next_button(self, page):
        # 페이지네이션 버튼 클릭 로직
        if self.pages_crawled%10 < 10:
            next_button = await page.query_selector(f'#pageList a:nth-child({self.pages_crawled%10 + 2})')
        else:
            next_button = await page.query_selector('#goNextPage')
        await next_button.click()

    async def parse_article_detail_page(self, response):
        thesis = ThesisItem()
        thesis['title'] = response.css('#dpMain > section > section.thesisDetail__upper > div.thesisDetail__info > div.thesisDetail__titWrap > h1 > span::text').get()
        thesis['issue_year'] = response.css('#dpMain > section > section.thesisDetail__upper > div.thesisDetail__info > div.thesisDetail__basicInfo > dl:nth-child(5) > dd::text').get().split('.')[0].replace('\n', '').strip()
        abstract = response.css('#dpMain > section > section.thesisDetail__abstract > div::text').get()
        thesis['abstract'] = abstract.replace('\n', '').replace('\t', '').strip() if abstract else None
        thesis['link'] = response.url
        self.inform('제목', thesis['title'], '발행 연도', thesis['issue_year'], '초록', thesis['abstract'], '링크', thesis['link'])

        page = response.meta["playwright_page"]
        await page.close() # 페이지 리소스 해제

        yield thesis

    async def parse_detail_page(self, response):
        thesis = ThesisItem()
        thesis['title'] = response.css('#dpMain > section > section.thesisDetail__upper > div.thesisDetail__info > div.thesisDetail__titWrap > h1 > span::text').get()
        thesis['issue_year'] = response.css('#dpMain > section > section.thesisDetail__upper > div.thesisDetail__info > div.thesisDetail__basicInfo > dl:nth-child(5) > dd::text').get().replace('\n', '').strip()
        abstract = response.css('#dpMain > section > section.thesisDetail__abstract > div::text').get()
        thesis['abstract'] = abstract.replace('\n', '').replace('\t', '').strip() if abstract else None
        thesis['link'] = response.url
        self.inform('제목', thesis['title'], '발행 연도', thesis['issue_year'], '초록', thesis['abstract'], '링크', thesis['link'])

        page = response.meta["playwright_page"]
        await page.close()

        yield thesis

    # 디버그용 함수
    def inform(self, name, value, *args):
        info = {name: value}
        if args:
            info.update({args[i]: args[i + 1] for i in range(0, len(args), 2)})
        self.logger.info(f'{info} ({(time.time() - self.start_time):.1f}초)')
