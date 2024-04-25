# -*- coding: utf-8 -*-
# @Time : 2024/2/26 15:17
# @Author : ordar
# @Project : ip_queryoject
# @File : main_local.py
# @Python: 3.7.5
import geoip2.database
import xlwt
import requests
requests.packages.urllib3.disable_warnings()
request_session = requests.session()
head = {"X-Forwarded-For":"127.0.0.1","Referer":"https://ip.sb/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"}

request_session.headers.update(head)

"""
https://www.maxmind.com/en/accounts/399866/geoip/downloads   下载最新GeoLite2数据
20240223
"""
city_reader = geoip2.database.Reader("../geoip/GeoLite2-City.mmdb")
asn_reader = geoip2.database.Reader("../geoip/GeoLite2-ASN.mmdb")


def query_ip(ip):

    city_ipinfo = city_reader.city(ip)
    asn_ipinfo = asn_reader.asn(ip)

    # print(city_ipinfo)
    # print(asn_ipinfo)
    result = {}
    # ASN
    result["autonomous_system_number/ASN"] = asn_ipinfo.autonomous_system_number
    # ASN对应组织：运营商
    result["autonomous_system_organization/ASO"] = asn_ipinfo.autonomous_system_organization
    # 网络范围
    result["network"] = f"{asn_ipinfo.network}"
    # 大陆
    result["continent"] = city_ipinfo.continent.name
    if len(city_ipinfo.continent.names) > 0:
        result["continent_zh"] = city_ipinfo.continent.names["zh-CN"]
    else:
        result["continent_zh"] = None
    # 国家
    result["country"] = city_ipinfo.country.name
    if len(city_ipinfo.country.names) > 0:
        result["country_zh"] = city_ipinfo.country.names["zh-CN"]
    else:
        result["country_zh"] = None
    # 省份
    if len(city_ipinfo.subdivisions) > 0:
        result["subdivisions"] = city_ipinfo.subdivisions[0].name
        result["subdivisions_zh"] = city_ipinfo.subdivisions[0].names["zh-CN"]
    else:
        result["subdivisions"] = None
        result["subdivisions_zh"] = None
    # 城市
    result["city"] = city_ipinfo.city.name
    if len(city_ipinfo.city.names) > 0:
        result["city_zh"] = city_ipinfo.city.names["zh-CN"]
    else:
        result["city_zh"] = None
    # 经纬度
    result['location'] = [city_ipinfo.location.longitude, city_ipinfo.location.latitude]

    # 获取运营商/ISP
    # https://api.ip.sb/geoip/1.1.8.21
    u = f"https://api.ip.sb/geoip/{ip}"
    isp_en = None
    try:
        resp = request_session.get(u, verify=False)
        ips_json = resp.json()
        isp_en = ips_json["isp"]
        # 更新省份和城市
        if "city" and "region" in ips_json.keys():
            result["city"] = ips_json["city"]
            result["subdivisions"] = ips_json["region"]
    except Exception as e:
        print(e)
        isp_en = "Error"
    result["isp_en"] = isp_en

    # print(result)
    return result


if __name__ == '__main__':
    # 创建xls文件
    myWorkbook = xlwt.Workbook()
    mySheet = myWorkbook.add_sheet('china_ip_list')
    # 写入标题
    mySheet.write(0, 0, "No")
    mySheet.write(0, 1, "IP")
    mySheet.write(0, 2, "network")
    mySheet.write(0, 3, "autonomous_system_number/ASN")
    mySheet.write(0, 4, "autonomous_system_organization")
    mySheet.write(0, 5, "continent")
    mySheet.write(0, 6, "continent_zh")
    mySheet.write(0, 7, "country")
    mySheet.write(0, 8, "country_zh")
    mySheet.write(0, 9, "subdivisions")
    mySheet.write(0, 10, "subdivisions_zh")
    mySheet.write(0, 11, "city")
    mySheet.write(0, 12, "city_zh")
    mySheet.write(0, 13, "location")
    mySheet.write(0, 14, "ISP")

    # 循环写入数据
    line_num = 0
    with open("china_ip_list.txt", 'r') as f:
        lines = f.readlines()
    for ip in lines:
        ip = ip.strip()
        ip = ip.replace(".0/", ".")
        if "/" in ip:
            ip = ip.split("/")[0]
        print(ip)
        try:
            result = query_ip(ip)
            print(result)
            line_num = line_num + 1
            print(line_num)
            mySheet.write(line_num, 0, line_num)
            mySheet.write(line_num, 1, ip)
            mySheet.write(line_num, 2, result["network"])
            mySheet.write(line_num, 3, result["autonomous_system_number/ASN"])
            mySheet.write(line_num, 4, result["autonomous_system_organization/ASO"])
            mySheet.write(line_num, 5, result["continent"])
            mySheet.write(line_num, 6, result["continent_zh"])
            mySheet.write(line_num, 7, result["country"])
            mySheet.write(line_num, 8, result["country_zh"])
            mySheet.write(line_num, 9, result["subdivisions"])
            mySheet.write(line_num, 10, result["subdivisions_zh"])
            mySheet.write(line_num, 11, result["city"])
            mySheet.write(line_num, 12, result["city_zh"])
            mySheet.write(line_num, 13, str(result["location"]))
            mySheet.write(line_num, 13, result["isp_en"])
        except:
            pass

    # 保存xls
    myWorkbook.save('china_ip_list.xls')
