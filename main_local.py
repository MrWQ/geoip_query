# -*- coding: utf-8 -*-
# @Time : 2024/2/26 15:17
# @Author : ordar
# @Project : ip_query
# @File : main_local.py
# @Python: 3.7.5
import geoip2.database
import sys
import json

"""
https://www.maxmind.com/en/accounts/399866/geoip/downloads   下载最新GeoLite2数据
20240223
"""
city_reader = geoip2.database.Reader(r'geoip/GeoLite2-City.mmdb')
asn_reader = geoip2.database.Reader(r'geoip/GeoLite2-ASN.mmdb')


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

    # print(result)
    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            ip = sys.argv[1]
            print(json.dumps(query_ip(ip), indent=4))
        except Exception as e:
            print(e)
    else:
        print("usage:python main_local.py 1.1.1.1")
