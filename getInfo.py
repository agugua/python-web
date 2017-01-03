from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS
from bs4.element import Tag

def Get_BS(url):
    try:
        html = urlopen(url)
    except (HTTPError,URLError) as e:
        # 1.当网页在服务器上不存在 （或者获取页面的时候出现错误）返回 HTTPError
        #   例如："404 Page Not Found" "500 internal server Error"等。所有类似情形。
        # 2.服务器不存在，网址打不开或是URL链接写错了 urlopen 会返回一个None对象。
        return None
    try:
        oBS = BS(html.read(),"lxml")
    except AttributeError as e:
        return None
    return oBS

def GetShengUrl(url):
    sheng_url = []  # 保存各省url地址的列表
    bsObj = Get_BS(url)
    if not bsObj:
        return None
    try:
        aUrl = bsObj.select("#category_165 div")
        for link in aUrl:
            if 'href' in link.find("a").attrs:
                sheng_url.append(link.find("a").attrs['href'])
    except AttributeError as e:
        return None

    return sheng_url

def GetShiUrl(url):
    shi_url = []  # 保存市url地址列表
    bsObj = Get_BS(url)
    if not bsObj:
        return None

    try:
        aurl = bsObj.select(".bm_c div")

        for link in aurl:
            if 'href' in link.find("a").attrs:
                shi_url.append(link.find("a").attrs['href'])
    except AttributeError as e:
        return None
    return shi_url

def GetWuliu(url):
    zUrl ="http://www.lecong56.com/"
    arrUrl = []
    bsObj = Get_BS(url)
    if not bsObj:
        return None
    try:
        aurl = bsObj.select('.bm_c a')

        for link in aurl:
            if 'href' in link.attrs:
               arrUrl.append(zUrl+str(link.attrs['href']))
    except AttributeError as e:
        return None
    return arrUrl

def GetData(url):
    data_dict = {}  # 临时存放每条数据的字典
    bsObj = Get_BS(url)
    if not bsObj:
        return None
    try:
        oDiv = bsObj.find("table", {"class": "t_table"})
        aDr = oDiv.find_all("tr", recursive=False)

        data_dict["公司名称"] = aDr[3].select('td:nth-of-type(2)')[0].get_text()
        data_dict["起始站"] = aDr[5].select('td:nth-of-type(2)')[0].get_text()
        data_dict["收货电话"] = aDr[5].select('td:nth-of-type(4)')[0].get_text()
        data_dict["收货地址"] = aDr[6].select('td:nth-of-type(2)')[0].get_text()
        data_dict["到达站"] = aDr[8].select('td:nth-of-type(2)')[0].get_text()
        data_dict["到货电话"] = aDr[8].select('td:nth-of-type(4)')[0].get_text()
        data_dict["到货地址"] = aDr[9].select('td:nth-of-type(2)')[0].get_text()
    except AttributeError as e:
        return None
    return data_dict

def main(url):
    Sheng_url = GetShengUrl(url)
    if not Sheng_url: return None

    shi_url = GetShiUrl(Sheng_url[5])
    if not shi_url: return None

    wuliu = GetWuliu(shi_url[2])
    if not wuliu: return None

    data = GetData(wuliu[5])
    if not data: return None

    return data

if __name__ == "__main__":
    data = []  # 保存物流公司详情列表
    data1 = main("http://www.lecong56.com/")
    if data1:
        data.append(data1)
        print(data)




