import sqlite3
from StockCrawler import StockCrawler


class StockDB:
    def __init__(self, db_name="stocks.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # entire_stock 테이블 생성
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS entire_stock (name TEXT, stock_code TEXT)"
        )

        # my_watchlist 테이블 생성
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS my_watchlist (company_name TEXT, stock_code TEXT, current_price TEXT, price_change TEXT,rate_change TEXT)"
        )
        self.add_to_entire_stock_bulk()

        # db 자체에서 크롤링해서 App단으로 넘겨줄 예정
        self.stock_crawler = StockCrawler()

        self.conn.commit()

    # interested_stock = [
    # {"company_name": "원익피앤이", "stock_code": "217820"},
    # {"company_name": "서남", "stock_code": "294630"},
    # {"company_name": "펄어비스", "stock_code": "263750"},]
    # 이런식으로 된 자료구조가 있으면 외부에서도 한번에 추가할 수 있음
    def add_to_entire_stock_bulk(self):
        entire_stock_list = [
            {"company_name": "원익피앤이", "stock_code": "217820"},
            {"company_name": "서남", "stock_code": "294630"},
            {"company_name": "서원", "stock_code": "021050"},
        ]
        with self.conn:
            self.conn.executemany(
                "INSERT INTO entire_stock (name, stock_code) VALUES (?, ?)",
                [
                    (stock["company_name"], stock["stock_code"])
                    for stock in entire_stock_list
                ],
            )

    def add_to_watchlist(self, company_name):
        # entire_stock 테이블에서 주어진 company_name에 해당하는 stock_code 가져오기
        self.cursor.execute(
            "SELECT stock_code FROM entire_stock WHERE name = ?", (company_name,)
        )
        result = self.cursor.fetchone()

        if result:
            stock_code = result[0]

            # my_watchlist에서 해당 company_name이 이미 존재하는지 확인
            self.cursor.execute(
                "SELECT 1 FROM my_watchlist WHERE company_name = ?", (company_name,)
            )
            exists = self.cursor.fetchone()

            if not exists:
                with self.conn:
                    self.conn.execute(
                        "INSERT INTO my_watchlist (company_name, stock_code) VALUES (?, ?)",
                        (company_name, stock_code),
                    )
            else:
                print(f"{company_name} already exists in watchlist")
        else:
            print(f"No stock code found for company {company_name}")

    # 크롤링 함수: company_name과 stock_code를 인자로 받아 현재가, 가격 변동, 변동률을 반환
    def fetch_latest_stock_data(self, company_name, stock_code):
        current_price = self.stock_crawler.get_current_price(stock_code)
        price_change, rate_change = self.stock_crawler.get_current_price_and_change(
            stock_code
        )
        return current_price, price_change, rate_change

    # 관심종목 업데이트 함수
    def update_watchlist_price(
        self, stock_code, current_price, price_change, rate_change
    ):
        with self.conn:
            self.conn.execute(
                "UPDATE my_watchlist SET current_price = ?, price_change = ?, rate_change = ? WHERE stock_code = ?",
                (current_price, price_change, rate_change, stock_code),
            )

    # 관심종목 전체 업데이트 함수: 모든 관심종목에 대해 크롤링 후 업데이트
    def refresh_all_watchlist(self):
        self.cursor.execute("SELECT company_name, stock_code FROM my_watchlist")
        all_stocks = self.cursor.fetchall()

        for stock in all_stocks:
            company_name, stock_code = stock
            current_price, price_change, rate_change = self.fetch_latest_stock_data(
                company_name, stock_code
            )
            self.update_watchlist_price(
                stock_code, current_price, price_change, rate_change
            )

    # 관심종목 삭제 함수 (삭제 버튼))
    def delete_from_watchlist(self, stock_code):
        with self.conn:
            self.conn.execute(
                "DELETE FROM my_watchlist WHERE stock_code = ?", (stock_code,)
            )

    # 관심종목 정보들 표시 (display에 사용)
    def get_all_from_watchlist(self):
        self.refresh_all_watchlist()
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM my_watchlist")
            return cursor.fetchall()
