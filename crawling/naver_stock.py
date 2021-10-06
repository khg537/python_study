import requests
import bs4

my_header = {
    "referer" : "https://finance.naver.com/item/sise_day.naver?code=005930&page=1",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}

r = requests.get(
    "https://finance.naver.com/item/sise_day.naver?code=005930&page=1", headers=my_header
    )
bs= bs4.BeautifulSoup(r.text, "lxml")
tr_elements= bs.select("table.type2 > tr[onMouseOut = 'mouseOut(this)']")

data_list = []
data= tr_elements[0].select("td")
for x in data:
    # print(x.text.strip())
    data_list.append(x.text.strip())
print(data_list)
