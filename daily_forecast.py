# encoding=utf8
import urllib2
import json
from wxpy import *
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

city_dict = {'beijing': '北京', 'xian': '西安', 'shanghai': '上海', 'hangzhou': '杭州', 'suzhou': '苏州', 'shenzhen': '深圳',
             'changchun': '长春'}
weather_dict = {'Overcast': '阴', 'Light Snow': '小雪', 'Cloudy': '多云', 'Sunny/Clear': '晴', 'Haze': '霾',
                'Light Rain': '小雨', 'Moderate Rain': '中雨', 'Moderate Snow': '中雪', 'Sleet': '雨夹雪',
                'Light to moderate rain': '小到中雨', 'Few Clouds': '少云',
                'Partly Cloudy': '晴间多云', 'Windy': '有风', 'Calm': '平静', 'Light Breeze': '微风',
                'Moderate/Gentle Breeze': '和风', 'Fresh Breeze': '清风',
                'Strong Breeze': '强风/劲风', 'High Wind, Near Gale': '疾风', 'Gale': '大风', 'Strong Gale': '烈风',
                'Storm': '风暴/暴雨', 'Violent Storm': '狂爆风', 'Hurricane': '飓风',
                'Tornado': '龙卷风', 'Tropical Storm': '热带风暴', 'Shower Rain': '阵雨', 'Heavy Shower Rain': '强阵雨',
                'Thundershower': '雷阵雨', 'Heavy Thunderstorm': '强雷阵雨', 'Thundershower with hail': '雷阵雨伴有冰雹',
                'Heavy Rain': '大雨', 'Extreme Rain': '极端降雨', 'Drizzle Rain': '毛毛雨/细雨', 'Heavy Storm': '大暴雨',
                'Severe Storm': '特大暴雨', 'Freezing Rain': '冻雨', 'Moderate to heavy rain': '中到大雨',
                'Heavy rain to storm': '大到暴雨',
                'Storm to heavy storm': '暴雨到大暴雨', 'Heavy to severe storm': '大暴雨到特大暴雨', 'Rain': '雨',
                'Heavy Snow': '大雪', 'Snowstorm': '暴雪', 'Rain And Snow': '雨雪天气', 'Shower Snow': '阵雨夹雪',
                'Snow Flurry': '阵雪',
                'Light to moderate snow': '小到中雪', 'Moderate to heavy snow': '中到大雪', 'Heavy snow to snowstorm': '大到暴雪',
                'Snow': '雪', 'Mist': '薄雾', 'Foggy': '雾', 'Sand': '扬沙', 'Dust': '浮尘', 'Duststorm': '沙尘暴',
                'Sandstorm': '强沙尘暴', 'Dense fog': '浓雾',
                'Strong fog': '强浓雾', 'Moderate haze': '中度霾', 'Heavy haze': '重度霾', 'Severe haze': '严重霾',
                'Heavy fog': '大雾', 'Extra heavy fog': '特强浓雾',
                'Hot': '热', 'Cold': '冷', 'Unknown': '未知'
                }

week_dict = {'Mon': '一', 'Tue': '二', 'Wed': '三', 'Thu': '四', 'Fri': '五', 'Sat': '六', 'Sun': '日'}


class Daily_forecast(object):

    def __init__(self, city):
        self.city = city

    def get_prepare(self):
        # 调用和风天气的API
        url = 'https://free-api.heweather.net/s6/weather/forecast?location=%s&lang=en&unit=m&key=1840e462b9ee4298a968a2f832dc80cb' % (
            self.city)

        # 用urllib2创建一个请求并得到返回结果
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req).read()
        # print resp

        # 将JSON转化为Python的数据结构
        json_data = json.loads(resp)
        # print json_data
        data = json_data['HeWeather6'][0]

        # 获取城市
        city = data['basic']['parent_city']

        # 获取温度
        tmp_max = data['daily_forecast'][0]['tmp_max']
        tmp_min = data['daily_forecast'][0]['tmp_min']
        isinstance(tmp_max, int)

        # 天气状况
        cond_txt_d = data['daily_forecast'][0]['cond_txt_d']
        cond_txt_n = data['daily_forecast'][0]['cond_txt_n']

        return city, cond_txt_d, cond_txt_n, tmp_min, tmp_max


def get_daily_forecast():
    list = []
    city_list = ['西安', '北京', '上海', '苏州', '杭州', '深圳', '长春']

    for i in city_list:
        for j in Daily_forecast(i).get_prepare():
            list.append(j)

    return list


def send_to_wechat():
    weather_list = get_daily_forecast()
    bot = Bot(True)
    my_group = bot.groups().search(u'番茄炒鸡蛋🤒')[0]
    # my_friend = bot.friends().search(u'万恶的星星果')[0]
    my_group.send(
        '西电驻京办事处为您播报未来24小时天气' + '\n' + time.strftime("%Y年%m月%d日", time.localtime()) + ' 星期' + week_dict[
            time.strftime("%a", time.localtime())] + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[0]], weather_dict[weather_list[1]], weather_dict[weather_list[2]], weather_list[3],
            weather_list[4])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[5]], weather_dict[weather_list[6]], weather_dict[weather_list[7]], weather_list[8],
            weather_list[9])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[10]], weather_dict[weather_list[11]], weather_dict[weather_list[12]],
            weather_list[13],
            weather_list[14])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[15]], weather_dict[weather_list[16]], weather_dict[weather_list[17]],
            weather_list[18],
            weather_list[19])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[20]], weather_dict[weather_list[21]], weather_dict[weather_list[22]],
            weather_list[23],
            weather_list[24])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[25]], weather_dict[weather_list[26]], weather_dict[weather_list[27]],
            weather_list[28],
            weather_list[29])
        + '\n' + '%s:白天:%s 夜间:%s,%s~%s℃' % (
            city_dict[weather_list[30]], weather_dict[weather_list[31]], weather_dict[weather_list[32]],
            weather_list[33],
            weather_list[34])
    )


if __name__ == '__main__':
    send_to_wechat()
