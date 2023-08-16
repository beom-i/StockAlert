from bs4 import BeautifulSoup as bs
import requests


class StockCrawler:
    def __init__(self):
        self.base_url = "https://finance.naver.com/item/main.naver?code="

    def get_soup(self, url):
        html = requests.get(url)
        return bs(html.text, "html.parser")

    def find_company_name(self, code, target_name):
        url = self.base_url + code
        soup = self.get_soup(url)
        company_name_tag = soup.select_one("div.wrap_company > h2 > a")
        if company_name_tag and target_name == company_name_tag.text:
            return True
        return False

    def get_current_price(self, code):
        url = self.base_url + code
        soup = self.get_soup(url)
        price_tag = soup.select_one("div.today > p.no_today > em")
        if price_tag:
            price = ([span.text for span in price_tag.find_all("span")])[0]
            return price
        return None

    def get_current_price_and_change(self, code):
        url = self.base_url + code
        soup = self.get_soup(url)

        # 상승/하락 둘다 no_tags를 받아옴
        no_tags = soup.select("p.no_exday > em.no_up, p.no_exday > em.no_down")
        print(no_tags)

        if no_tags[0] and "no_up" in no_tags[0]["class"]:
            ex_price_tag = no_tags[0]
            ex_price = "+" + ex_price_tag.find("span", class_="blind").text
        elif no_tags[0] and "no_down" in no_tags[0]["class"]:
            ex_price_tag = no_tags[0]
            ex_price = "-" + ex_price_tag.find("span", class_="blind").text
        else:
            ex_price = "error"

        # 변동률 추출
        change = None
        if no_tags[1] and "no_up" in no_tags[1]["class"]:
            change_tag = no_tags[1]
            change = "+" + change_tag.find("span", class_="blind").text
        elif no_tags[1] and "no_down" in no_tags[1]["class"]:
            change_tag = no_tags[1]
            change = "-" + change_tag.find("span", class_="blind").text
        else:
            change = "error"
        return ex_price, change
