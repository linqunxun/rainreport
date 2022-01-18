#!/usr/local/bin/python
# -*- coding:utf-8 -*- 

import os
import urllib.request
import re
import sys
import datetime
import urllib  

# ################################ 定义开始 ###############################

MATCH_NO = 0
MATCH_TR_BEGIN = 1
MATCH_TR_END = 2
MATCH_TD_BEGIN = 3
MATCH_TD_END = 4
MATCH_TABLE_END = 5
DATE_FORMAT = "%Y-%m-%d"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def grab(date, file):
	print("正在采集%s的数据..." %(date.strftime(DATE_FORMAT)))
	global_match_state = MATCH_NO
	write_line = ""

	txt_time1 = date.strftime("%Y-%m-%d 00:00")
	txt_time2 = (date + datetime.timedelta(days = 1)).strftime("%Y-%m-%d 00:00")

	req = urllib.request.Request(url)
	data = urllib.parse.urlencode({
		'__VIEWSTATE':view_state,
		'__EVENTVALIDATION':eventvalidation,
		'txt_time1':txt_time1, 
		'txt_time2':txt_time2, 
		'btn_query':'查询'
		#'ddl_addvcd':'全部'
		})
	#enable cookie  
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())  
	response = opener.open(req, bytes(data, encoding='utf-8')) 

	line_list = response.readlines()
	for lineBytes in line_list:		#遍历网页的每一行  
		line = str(lineBytes, encoding='utf-8').strip()		#去除行首位的空格，习惯性写法
		if line == '':
			continue

		if MATCH_NO == global_match_state:
			if re.match( '<tr align="center" bgcolor=".', line ):
				# print ('set state = MATCH_TR_BEGIN line = ' + line)
				global_match_state = MATCH_TR_BEGIN

		elif MATCH_TR_BEGIN == global_match_state:
			write_line = date.strftime(DATE_FORMAT) + ","
			if re.match('<td  class=tdleft>', line):
				# print ('set state = MATCH_TD line = ' + line)
				global_match_state = MATCH_TD_BEGIN

		elif MATCH_TD_BEGIN == global_match_state:
			if re.match('</td>', line) or '' == line:
				global_match_state = MATCH_TD_END
			else:
				write_line = write_line + line + ','

		elif MATCH_TD_END == global_match_state:
			if re.match('<td +class=.', line):
				# print ('set state = MATCH_TD line = ' + line)
				global_match_state = MATCH_TD_BEGIN
			elif re.match('</tr>', line):
				# print ('write write_line to file, write_line = ' + write_line)
				file.write( write_line + '\n' )
			elif re.match('<tr align="center" bgcolor=".', line):
				# print ('set state = MATCH_TR_BEGIN line = ' + line)
				global_match_state = MATCH_TR_BEGIN
			elif re.match('</table>', line):
				global_match_state = MATCH_TABLE_END

	print("采集%s的数据完成.\n" %(date.strftime(DATE_FORMAT)))

# ################################ 逻辑处理开始 ###############################

try :
	if 1 == len(sys.argv) : 
		begin_date = datetime.datetime.now()
		end_date = begin_date
		filename = begin_date.strftime(DATE_FORMAT)
	elif 2 == len(sys.argv) :
		begin_date = datetime.datetime.strptime(sys.argv[1], DATE_FORMAT)
		end_date = begin_date
		filename = begin_date.strftime(DATE_FORMAT)
	elif 3 == len(sys.argv) :
		begin_date = datetime.datetime.strptime(sys.argv[1], DATE_FORMAT)
		end_date = datetime.datetime.strptime(sys.argv[2], DATE_FORMAT)
		filename = begin_date.strftime(DATE_FORMAT) + "_" + end_date.strftime(DATE_FORMAT)
	else :
		raise Exception("参数个数有误")
except Exception as err :
	print("异常信息：%s\n" %(err))
	print("帮助手册（help）：\n● 不传参则取当天数据\n● 传一个日期则取该日期数据\n● 传两个日期则取日期范围数据\n● 日期格式为：2022-01-01")
	sys.exit()

print("准备开始采集，日期为：%s" %(filename))

file = write_file_bl = open("./" + filename + "_big_lit.cvs", 'a')
url = 'http://210.76.80.76:9001/Report/RainReport.aspx'
viewstate_file = open(resource_path('VIEWSTATE'), "r")
view_state = viewstate_file.read().strip('\n')
viewstate_file.close()
eventvalidation = '/wEdABx9RZMmw1LG+yU0BQd3TV2rD5R4QB07L6EPE8hbiA1HCjQe693E4rfh8w4KrFy5Bj3qc95Ub9AmjsCaEcQ1PRGXJY9KOVS66bYw3q07YOQVt4DmtqNRf8Rh8CBmDXE37HiN5RVSvKkNx6BevOTmSZwzKK4M9qnFNMlL/90YA0v2KsxbrBB3jo9Cugoavc63zLm9My41G4k2bD1H9/DevJa7wcjQz304htdplq4o6qLjU7BToL28oNzz/tjDoVVVIhiD3oM18XDf8vos8kRdlCgWpjFPpuO0nCnf++I958L2pfPnIB5/wJLV8h40L35u+d4vFTOoUBfCvciBoq6O3SZ4CMvy4Ne/abH/S8UnCo91U4bK+iIVPQ9Qmq1oIGHjR+rSlof14T3WkNe3Bfqmtxf9LKiIdtM0Qyv+SkqglRIe2eX+ybSo2jt25MGjS+iu0HzzRgyGF4e9D60kZeFjGcVG3Mp8k0MqtIykrMCeFt1vrvYBoMfVKie2hgAVD0f/Dy7Ev58OiHZScWJMXWzdRGgTupO9qKKX2H5OVAecnhdKrp/niFT6iq+w7w6u1SnFjkNYEmXUkIdwCjm7RrNxm+3ecjUCzmBKr0HCW4ODG/DfLtR6irz7pCQihoGrG/aDEXc='

file.write( "日期,市,市(县),站点,累计雨量(毫米),\n" )
for i in range((end_date - begin_date).days + 1):
	grab(begin_date + datetime.timedelta(days=i), file)
file.close()
print("采集完毕，生成的文件名为：%s_big_lit.cvs" %(filename))