import urllib.parse
import urllib.request

# params  CategoryId=808 CategoryType=SiteHome ItemListActionName=PostList PageIndex=3 ParentCategoryId=0 TotalPostCount=4000
def getHtml(url,values):
    user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    headers = {'User-Agent':user_agent}
    data = urllib.parse.urlencode(values)
    response_result = urllib.request.urlopen(url+'?'+data).read()
    html = response_result.decode('utf-8')
    return html

#请求公交线路列表根页面
def getBusRoot():
    print('请求公交线路列表根页面数据')
    url = 'http://bus.mapbar.com/chengdu/xianlu/'
    values = {}
    result = getHtml(url,values)
    return result