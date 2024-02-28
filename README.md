基于geoip查询ip地址信息

# 功能
查询IP地址、ASN、运营商、位置、城市等等

# 数据
```
https://www.maxmind.com/en/accounts/399866/geoip/downloads   下载最新GeoLite2数据
geopip文件夹是20240223
```

# 使用
```
main_local:终端查询
python .\main_local.py 1.1.1.1

main_web:web访问查询
python .\main_web.py
curl http://127.0.0.1:8080/1.1.1.1 or curl http://127.0.0.1:8080/getip/1.1.1.1
```
