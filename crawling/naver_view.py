import requests
import bs4

res = requests.get(
    "https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EB%A7%9B%EC%A7%91"
)

soup= bs4.BeautifulSoup(res.text )
# ul_elements = soup.select("ul")
ul = soup.select("ul.lst_total")
ul_element = ul[0]

li_element = ul_element.select("li")