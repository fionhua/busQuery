import json
import getWeb
import praseWeb
from getJsonList import getJsonFile
from getPostion import addressPostion

#抓取公交网站信息，并保存到c:\BusLine
busRoot = getWeb.getBusRoot()
praseWeb.parseBusRoot(busRoot)

#获得指定目录下所有Json文件列表
jsonList = getJsonFile('c:\BusLine')
#逐个解析Json文件
jumpOver = True
for jsonFile in jsonList:
    print('正在查询经纬度:%s'%jsonFile)
    with open(jsonFile, 'r') as f:
        if jsonFile.find('P开头') >= 0 : jumpOver = False
        if jumpOver:continue
        busLine = json.load(f)
        for singleLine in busLine:
            for (busLineName, stations) in singleLine[0].items():
                for station in stations:
                    #高德地图查询公交站，后缀以'(公交站)'结尾，都能有数据
                    station['name'] = station['name'] + '(公交站)'
                    address = addressPostion(station['name'],busLineName)
                    postion = address.split(',')
                    try:
                        station['long'] = postion[0]
                        station['lat'] =  postion[1]
                    except:
                        print('获取经纬度异常：%s'%station['name'])
                    #time.sleep(1)
    with open(jsonFile, 'w') as f2:
        json.dump(busLine, f2, ensure_ascii=False, indent=2)
print('经纬度查询完毕！——Over')



