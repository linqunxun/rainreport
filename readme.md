# 雨情报表采集程序
> 该程序采集来自[雨情报表](http://210.76.80.76:9001/Report/RainReport.aspx)的数据</br>
> 程序使用python3进行开发

## 使用方式
```shell
./rainreport.py [begin_date] [end_date]
```
## 打包方式
注意：由于程序依赖`VIEWSTATE`文件，所以打包完成后，务必将`VIEWSTATE`文件放在与`rainreport.exe`文件同目录下。
```shell
pyinstaller -F .\rainreport.py
```

## 更新日志
- 2022-01-18 完善程序，支持日期段采集