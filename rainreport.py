#!/usr/local/bin/python
# -*- coding:utf-8 -*- 
# 调用方式一：获取当天的数据：$ python rainreport.py
# 调用方式二：获取一段时期的数据：$ python rainreport.py "2016-09-01 00:00" "2016-09-04 00:00"


import urllib2
import re
import HTMLParser
import sys
import datetime
import urllib  
import cookielib
#print html

MATCH_NO = 0
MATCH_TR_BEGIN = 1
MATCH_TR_END = 2
MATCH_TD_BEGIN = 3
MATCH_TD_END = 4
MATCH_TABLE_END = 5

global_match_state = MATCH_NO

begin_time = ""
end_time = ""

print( sys.argv )
if 1 == len(sys.argv) : 
	write_file_bl = open("./" + now.strftime('%m-%d') + "_big_lit.cvs", 'a')
	write_file_area = open("./" + now.strftime('%m-%d') + "_area.cvs", 'a')
else:
    begin_time = sys.argv[1]
    end_time = sys.argv[2]
    filename = begin_time + "_" + end_time
    filename = filename.replace(":", "")
    filename = filename.replace("-", "")
    filename = filename.replace(" ", "")
    write_file_bl = open("./" + filename + "_big_lit.cvs", 'a')
    write_file_area = open("./" + filename + "_area.cvs", 'a')	


################################ 代码开始 ###############################
now = datetime.datetime.now()


write_file = write_file_bl
write_line = ""

url = 'http://www.gdwater.gov.cn:9001/Report/RainReport.aspx'
if 0 == len(begin_time):
    response = urllib2.urlopen(url)
else:
    viewstate_file = open("VIEWSTATE", "r")
    view_state = viewstate_file.read().strip('\n')
    viewstate_file.close()

    req = urllib2.Request(url)
    data = urllib.urlencode({
        '__VIEWSTATE':view_state,
		'__EVENTVALIDATION':'/wEWHALKnaiwDgKfts6aDQLzpIrbDwLzpP78BALzpNKRDALzpMaqBQLzpLrOAgLzpK7jCwLzpIKEAwLzpLbvDQLzpKqABQKYyoPhDgKYyve6BgKYyuvfDwKYyt/wBAKYyrOUDAKYyqepBQKYytuRBgKYys+qDwK9093dAgLslpexCALslovKAQLslv/vDgKzwPf7DQKO5oKYAQKN5oKYAQLjwOP9CALcoYgbAFxfEg5XjmrAgNSS7S3F/N2OWNY=',
        'txt_time1':begin_time, 
        'txt_time2':end_time, 
        'btn_query':'查询'
        #'ddl_addvcd':'全部'
		})

    print(data)
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data) 



html = response.read()

#type = sys.getfilesystemencoding()
#html = html.decode("UTF-8").encode(type)

line_list = html.split('\r\n')
html_parser = HTMLParser.HTMLParser()

for eachLine in line_list:		#遍历网页的每一行  
	line = eachLine.strip()		#去除行首位的空格，习惯性写法
	if line == '':
		continue

	#line = line.decode("UTF-8")

	if MATCH_NO == global_match_state:
		if re.match( '<tr align="center" bgcolor=".', line ):
			print 'set state = MATCH_TR_BEGIN line = ' + line
			global_match_state = MATCH_TR_BEGIN
			write_file.write( "市,市(县),站点,累计雨量(毫米),\n" )

	elif MATCH_TR_BEGIN == global_match_state:
		write_line = ""
		if re.match('<td  class=tdleft>', line):
			print 'set state = MATCH_TD line = ' + line
			global_match_state = MATCH_TD_BEGIN

	elif MATCH_TD_BEGIN == global_match_state:
		if re.match('</td>', line) or '' == line:
			global_match_state = MATCH_TD_END
		else:
			write_line = write_line + line + ','

	elif MATCH_TD_END == global_match_state:
		if re.match('<td +class=.', line):
			print 'set state = MATCH_TD line = ' + line
			global_match_state = MATCH_TD_BEGIN
		elif re.match('</tr>', line):
			print 'write write_line to file, write_line = ' + write_line
			write_file.write( write_line + '\n' )
		elif re.match('<tr align="center" bgcolor=".', line):
			print 'set state = MATCH_TR_BEGIN line = ' + line
			global_match_state = MATCH_TR_BEGIN
		elif re.match('</table>', line):
			global_match_state = MATCH_TABLE_END
			write_file.close()

	elif MATCH_TABLE_END == global_match_state:
		if re.match( '<tr align="center" bgcolor=".', line ):
			print 'set state = MATCH_TR_BEGIN line = ' + line
			global_match_state = MATCH_TR_BEGIN
			write_file = write_file_area
			write_file.write( "市,市(县),站点,累计雨量(毫米),\n" )


