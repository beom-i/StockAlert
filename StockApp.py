import tkinter as tk
from tkinter import ttk  # ttk는 tk의 확장된 라이브러리로 더 나은 스타일의 위젯을 제공합니다.
from StockDB import StockDB


class StockApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("입력 폼")

        # DB 생성 (종목 정보들)
        self.db = StockDB()

        # 테이블의 컬럼 이름
        # 종목 - company_name
        # 가격 - current_price
        # 변동가격 - price_change
        # 등락률 - rate_change
        columns = ("종목", "가격", "변동가격", "등락률")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20)

        # 앱 버튼 들 초기화
        self.create_widgets()

        # 관심 종목 정보들 display
        self.display_stock_info()

    def display_stock_info(self):
        # 가상의 주식 데이터
        stocks = self.db.get_all_from_watchlist()

        # 기존에 있는 모든 아이템들 삭제
        for i in self.tree.get_children():
            self.tree.delete(i)

        # 각 주식 데이터를 행으로 추가
        for stock in stocks:
            # stock은 튜플이므로 인덱스를 사용하여 값에 접근
            company_name = stock[0]
            current_price = stock[2]
            price_change = stock[3]
            rate_change = stock[4]

            self.tree.insert(
                "",
                "end",
                values=(
                    company_name,
                    current_price,
                    price_change,
                    rate_change,
                ),
            )
        self.tree.pack(pady=20)

    def create_widgets(self):
        # 라벨 추가
        label = tk.Label(self.root, text="값을 입력해주세요:")
        label.pack(pady=10)

        # 텍스트 입력 창 추가
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)

        # 제출 버튼 추가
        submit_button = tk.Button(self.root, text="제출", command=self.submit)
        submit_button.pack(pady=10)

        # 새로고침 버튼 추가
        refresh_button = tk.Button(self.root, text="새로고침", command=self.refresh)
        refresh_button.pack(pady=10)

    def refresh(self):
        # Treeview의 현재 아이템들 모두 삭제
        for i in self.tree.get_children():
            self.tree.delete(i)
        # 주식 정보 다시 불러와서 Treeview 업데이트
        self.display_stock_info()

    def submit(self):
        input_value = self.entry.get()
        self.db.add_to_watchlist(input_value)

    def run(self):
        self.root.mainloop()
