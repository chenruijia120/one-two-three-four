from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3
import brotli
import requests as req

def main():
    #爬取音乐类别
    categories=['pop','Electronic','Folk','rock','R&B','post-rock','jazz','metal','classical']
    datalist=[]
    for num in range(0,8):
        baseurl="https://music.douban.com/tag/"+categories[num]
        #爬取网页
        datalist.append(getData(baseurl))
        savepath=".\\dbMusicClassification.xls"
        #保存数据
    saveData(datalist,savepath,categories)
   
#创建正则表达式对象
#唱片链接
findlink=re.compile(r'<a class="nbg" href="(.*?)"')
#唱片图片链接
findImgSrc=re.compile(r'<img(.*?)src="(.*?)"')
#其他信息，包括作者、发行日期、标签等
findBd=re.compile(r'<p class="pl">(.*?)</p>')

#爬取网页
def getData(baseurl):
    datalist=[]
    #保存获取到的网页源码
    html=askURL(baseurl)
    #解析数据
    soup=BeautifulSoup(html,"html.parser")
    #查找符合要求的字符串，形成列表
    for item in soup.find_all('tr',class_="item"):
        #保存一张专辑的所有信息
        data=[]
        item=str(item)
        
        #re库用来查找字符串
        link=re.findall(findlink,item)[0]
        link=re.sub('<a class="nbg" href='," ",link)
        data.append(link)

        imgSrc=re.findall(findImgSrc,item)[0]
        data.append(imgSrc[1])
        title=re.sub('alt=(.*?)-'," ",imgSrc[0])
        data.append(title.strip())

        bd=re.findall(findBd,item)[0]
        data.append(bd)
 
        #处理好的一张专辑放入datalist
        datalist.append(data) 

    return datalist


#得到指定一个url的网页内容
def askURL(url):
    #模拟浏览器头部信息，向豆瓣服务器发消息
    #用户代理，表示告诉豆瓣服务器，我们是什么类型的机器
    head={"User-Agent":	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    request= urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        #将得到的信息以utf-8解析
        html=response.read().decode("utf-8")
        #报错信息
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html





#保存数据
def saveData(datalist,savepath,categories):
    #创建workbook对象
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)
    for k in range(0,8):
        sheetname="豆瓣音乐分类_"+categories[k]
        #根据类别创建工作表
        sheet=book.add_sheet(sheetname,cell_overwrite_ok=True)
        #列名
        col=("音乐详情链接","图片链接","音乐名","作者/发行日期/标签")
        #写入具体数据
        for i in range(0,4):
            sheet.write(0,i,col[i])
        for i in range(0,20):
            data=datalist[k][i]
            for j in range(0,4):
                sheet.write(i+1,j,data[j])
    #保存
    book.save(savepath)
        




if __name__=="__main__":
    #当程序执行时

    main()
    print("爬取完毕")
