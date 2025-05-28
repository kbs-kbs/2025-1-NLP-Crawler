import scrapy
from scrapy_playwright.page import PageMethod # Playwright 페이지 조작을 위한 모듈
import time # 실행 시간 측정용
import math # 페이지 계산용
from scrpy_plwrt_demo.items import ThesisItem # 데이터 저장을 위한 아이템 클래스

class AdvancedDbpiaSpider(scrapy.Spider):
    name = 'advanced_dbpia' # 스파이더 이름
    allowed_domains = ['www.dbpia.co.kr'] # 허용 도메인

    def __init__(self, category='NE08', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        self.thesis_paths = []
        self.max_pages = 0 # 최대 페이지 수
        self.pages_crawled = 0 # 현재 크롤링 완료 페이지 수
        self.start_time = time.time() # 실행 시작 시간 기록

    def start_requests(self):
        # 초기 요청 생성 (Playwright 설정 포함)
        yield scrapy.Request(
            url=f'https://www.dbpia.co.kr/search/topSearch?collectionQuery=(<TITLE:contains:인공지능>|<NODE_NM_2:contains:인공지능>)|(<TITLE:contains:ai> | <NODE_NM_2:contains:ai>) | (<TITLE:contains:딥러닝> | <NODE_NM_2:contains:딥러닝>)|(<TITLE:contains:머신러닝>|<NODE_NM_2:contains:머신러닝>)|&filter=&prefix=&subjectCategory={self.category}',
            meta={
                "playwright": True, # Playwright 활성화
                "playwright_include_page": True, # 페이지 객체 포함
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "#search-result-total-count > strong") # 총 논문 수 요소 대기
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
        node_count = int(response.css('#search-result-total-count > strong::text').get().replace(',', ''))
        self.inform('논문 개수', node_count)

        page = response.meta["playwright_page"]
        if node_count == 0:
            return # 결과 없으면 종료
        elif node_count > 20:
            # 100개씩 보기 설정 (페이지네이션 최적화)
            self.max_pages = math.ceil(node_count/100)
            await page.wait_for_selector('#page-size-btn')
            element = await page.query_selector('#page-size-btn')
            await element.click() # 페이지당 표시 수 드롭다운 클릭
            await page.wait_for_selector('#sort-page-size-section > div > ul > li:nth-of-type(4) > button')
            element = await page.query_selector('#sort-page-size-section > div > ul > li:nth-of-type(4) > button')
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
            self.parse_thesis_paths(new_response)

            if self.pages_crawled < self.max_pages:
                await self.click_next_button(page) # 다음 페이지 버튼 클릭
                await page.wait_for_load_state('load')
                updated_html = await page.content()
            else: break
        
        # 수집된 노드 ID 기반 상세 페이지 요청 생성
        for thesis_path in self.thesis_paths:
            yield scrapy.Request( # 학술지 세부 페이지 요청
                url='https://www.dbpia.co.kr' + thesis_path,
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

    def parse_thesis_paths(self, response):
        self.thesis_paths += response.css('#paper-cards-section > div.thesisCard__cont > p.thesis__subject > a::attr(href)').getall()
        self.pages_crawled += 1
        self.inform('완료한 페이지', self.pages_crawled, '패스 리스트', self.thesis_paths)

    async def click_next_button(self, page):
        # 페이지네이션 버튼 클릭 로직
        if self.pages_crawled%10 < 10:
            next_button = await page.query_selector(f'#pagination-section > div > a:nth-child({self.pages_crawled%10 + 2})')
        else:
            next_button = await page.query_selector('#pagination-section > div > a.arrow.next')
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
