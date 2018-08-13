import requests
import re

#申请的key
#ak='389880a06e3f893ea46036f030c94700'
#参考：https://lbs.amap.com/api/webservice/guide/api/georegeo/?
ak = 'e1a5828407fbb8fa2c1475ab68d99102'#乐租房
#传入地址，返回对应地址的经纬度信息
def addressPostion(address,busLineName):
    url = 'http://restapi.amap.com/v3/geocode/geo?key=%s&s=rsv3&city=028&address=%s'%(ak,address)
    data=requests.get(url)
    contest=data.json()
    try:
        contest=contest['geocodes'][0]['location']
        print('正在查询%s：%s,经纬度：%s' %(busLineName,address,contest))
    except:
        contest = ','
    return contest

def get_site(info):
    lat = info['geocodes'][0]['location'].split(',')[0]
    lng = info['geocodes'][0]['location'].split(',')[1]
    return lat, lng