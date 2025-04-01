import subprocess
import pandas as pd

def run_crawlers():
    keyword = input('키워드를 입력해주세요: ')
    # 1. DBpia 크롤러 실행 (검색어 전달)
    subprocess.run(['scrapy', 'crawl', 'dbpia', '-O', 'csv/dbpia.csv', '-a', f'keyword={keyword}'], check=True)
    # 2. RISS 크롤러 실행 (검색어 전달)
    subprocess.run(['scrapy', 'crawl', 'riss', '-O', 'csv/riss.csv', '-a', f'keyword={keyword}'], check=True)

def merge_csv_files(output_file='csv/merged.csv'):
    # 1. CSV 파일 읽기
    dbpia_df = pd.read_csv('csv/dbpia.csv')
    riss_df = pd.read_csv('csv/riss.csv')
    
    # 2. NaN 값을 빈 문자열로 대체 (abstract 열)
    dbpia_df['abstract'] = dbpia_df['abstract'].fillna('')
    riss_df['abstract'] = riss_df['abstract'].fillna('')

    # 2. 데이터 병합 (lsuffix와 rsuffix 사용)
    merged_links = pd.merge(
        dbpia_df[['issue_year', 'title', 'link']],
        riss_df[['issue_year', 'title', 'link']],
        on=['issue_year', 'title'],
        how='outer',
        suffixes=('_dbpia', '_riss')  # 접미사 추가
    )

    # 3. 원본 데이터에서 링크 제거
    dbpia_main = dbpia_df.drop(columns=['link'])
    riss_main = riss_df.drop(columns=['link'])

    # 4. 메인 데이터 병합 (중복 제거 및 추상화 처리)
    merged_main = pd.concat([dbpia_main, riss_main])
    merged_main = (
        merged_main.groupby(['issue_year', 'title'], as_index=False)
        .agg({'abstract': lambda x: max(x, key=len)})  # 가장 긴 abstract 선택
    )

    # 5. 최종 병합 (메인 데이터 + 링크)
    merged_df = pd.merge(
        merged_main,
        merged_links,
        on=['issue_year', 'title'],
        how='left'
    )

    sorted_df = merged_df.sort_values(by='issue_year', ascending=True)

    # 6. 결과 저장
    sorted_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")

if __name__ == '__main__':
    # 크롤러 실행 및 CSV 병합
    run_crawlers()
    merge_csv_files()
