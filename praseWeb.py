import re
import sys
import time

from bs4 import BeautifulSoup
import json
import getWeb

#这里已经拿到具体线路明细页面的URL
#'http://bus.mapbar.com/chengdu/xianlu/1lu/'
def GetBusLineContent(busLineURL,busLineName):
    values = {}
    stationInfo2 = [busLineName]
    time.sleep(3)#延时1秒
    busLineInfo = getWeb.getHtml(busLineURL, values)
    temp = re.findall('您的计算机或网络可能正在发送自动查询',busLineInfo)
    if temp.__len__() == 1 :
        print('您的计算机或网络可能正在发送自动查询，为了保护我们的用户，我们目前无法处理您的请求您的刷新超速，若解除IP屏蔽，请输入检证码。')
        return None

    print('正在获取公交线路信息：'+busLineName)
    soupInfo = BeautifulSoup(busLineInfo, 'html.parser')
    busStation = soupInfo.find_all('div', attrs={'class': 'publicBox buslist'})
    stationList = []
    stationInfo = []
    for station in busStation[0].contents[1].contents:
        #<li class="first"><a href="http://bus.mapbar.com/chengdu/poi/6Oj8d95lw55i4wa7hP" id="HAARIBVTUSEAT" target="_blank" title="昭觉寺公交站"><span>1</span><em>昭觉寺公交站</em></a></li>
        if (station  == '\n'):continue
        stationName = station.contents[0]['title']
        statronOrder = getattr(station.contents[0],'span').text
        stationInfo.append({"name" : stationName  , "order": statronOrder,"long":"", "lat":""})
    stationList.append({busLineName:stationInfo})
    return stationList

#这里已经拿到<dd>里面所有数据
#<dd>
#<a href="http://bus.mapbar.com/chengdu/xianlu/1lu/" target="_blank" title="成都1路公交线路 ">1路</a>
#<a href="http://bus.mapbar.com/chengdu/xianlu/10lu/" target="_blank" title="成都10路公交线路 ">10路</a>
#<a href="http://bus.mapbar.com/chengdu/xianlu/11lu/" target="_blank" title="成都11路公交线路 ">11路</a>
#……
#</dd>
def GetBusLineURL(classifyBusLine,saveName):#获取具体公交线路的明细页URL
    jsonData = []
    for singleBusLine in classifyBusLine:
        if not hasattr(singleBusLine,'href'): continue
        #singleBusLine = <a href="http://bus.mapbar.com/chengdu/xianlu/1lu/" target="_blank" title="成都1路公交线路 ">1路</a>
        busLineURL = singleBusLine['href']
        busLineName = singleBusLine.text
        jsonData.append(GetBusLineContent(busLineURL,busLineName))

    jsonfile = sys.path[0]+ '//' +saveName + '.json'
    with open(jsonfile, 'w') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=2)

    return "Run Over !"

#解析最外层
def parseBusRoot(busRoot):
    soup = BeautifulSoup(busRoot, 'html.parser')
    #取出页面中1-9开头、D-X开头的列表
    all_div = soup.find_all('dl', attrs={'class': 'ChinaTxt'})

    jumpFlag = '成都公交线路查询列表_7开头'
    vaildLine = {'成都公交线路查询列表_1开头',
                 '成都公交线路查询列表_2开头',
                 '成都公交线路查询列表_3开头',
                 '成都公交线路查询列表_4开头',
                 '成都公交线路查询列表_5开头',
                 '成都公交线路查询列表_6开头',
                 '成都公交线路查询列表_7开头',
                 '成都公交线路查询列表_8开头',
                 '成都公交线路查询列表_9开头',
                 # '成都公交线路查询列表_D开头',#大丰、都江堰
                 '成都公交线路查询列表_G开头',
                 # '成都公交线路查询列表_J开头',#金堂
                 '成都公交线路查询列表_K开头',
                 # '成都公交线路查询列表_L开头',#龙泉驿
                 # '成都公交线路查询列表_P开头',#郫县、彭州
                 # '成都公交线路查询列表_Q开头',#青白江
                 '成都公交线路查询列表_S开头',  #双流
                 '成都公交线路查询列表_T开头',  #天府新区
                 '成都公交线路查询列表_W开头',  #温江
                 '成都公交线路查询列表_X开头',  #新繁、新都
                 }
    jumpOver = False
    if all_div is not None:
        for classifyBusLine in all_div:
            if classifyBusLine.contents[3] is not None:
                saveName = classifyBusLine.contents[1].contents[1].contents[1]['title']
                if saveName == jumpFlag: jumpOver = True
                #if jumpOver: GetBusLineURL(classifyBusLine.contents[3],saveName)
                GetBusLineURL(classifyBusLine.contents[3],saveName)
    print('全部抓取完成！——Over')
