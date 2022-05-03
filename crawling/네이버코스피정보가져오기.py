import requests
from  bs4 import BeautifulSoup
import time
import pyautogui
import openpyxl

wb = openpyxl.Workbook()
ws = wb.create_sheet("코스피")
ws.append(["종목명", "PER", "ROE", "PBR", "유보율"])


lastpage = int(pyautogui.prompt("몇 페이지까지 크롤링할까요?(1페이지 = 50개"))

for i in range(1, lastpage + 1):
    response = requests.get(f"https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?&page={i}&fieldIds=per&fieldIds=roe&fieldIds=pbr&fieldIds=reserve_ratio")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.select("table > tbody > tr[onmouseover='mouseOver(this)']")
    #print(trs)
    for tr in trs:
        #n-th child 속성 이용한다.
        name = tr.select_one("td:nth-child(2)").text
        per = tr.select_one("td:nth-child(7)").text
        roe = tr.select_one("td:nth-child(8)").text
        pbr = tr.select_one("td:nth-child(9)").text
        reserve_ratio = tr.select_one("td:nth-child(10)").text

        print(name,per, roe, pbr, reserve_ratio)
        
        ws.append([name,per, roe, pbr, reserve_ratio])
        

wb.save("코스피정보.xls")
