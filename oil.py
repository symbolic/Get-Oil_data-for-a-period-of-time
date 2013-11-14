#-*- coding: utf-8 -*-
from __future__ import division
import sys
import string

class oneline_item():	#数据结构
	"""read one line """
	def __init__(self):
		self.date = ''	#日期
		self.time = ''	#时间
		self.type = ''	#发送 接收
		self.port = ''	#端口号
		self.len = ''	#长度
		self.data = ''	#数据

def power(base, n):				#16进制转10进制：base = 256,
	if n == 1:
		return 1
	return base*power(base, n-1)

def hex_decimal(hex, n = 0):		#16进制转换成10进制，n为小数点个数, 返回值str
	temp = hex.split(' ')
	b = 0
	for i in range(len(temp)):
		b += string.atoi(temp[i], 16) * power(256, len(temp)-i)

	if n:
		return str(b/power(10, n+1))
	else:
		return str(b)

def decimal_hex(dec, n = 1):	#10进制转换为16进制，n为字节数
	temp = hex(int(dec))[2:]
	a = 2*n
	if len(temp) > a:
		return 'decimal_hex error'
	
	b = '0'*(a-len(temp)) + temp
	if n == 1:
		return b
	c = ''
	y = 0
	for x in xrange(0, n-1):
		c += b[0+2*x : 2+2*x] + ' '
		y = x
	c += b[2+2*y : 4+2*y]
	return 	c

def bcd_decimal(hex, n = 0):		#BCD转换成10进制，n为小数点个数, 返回数值
	temp = hex.split(' ')
	b = 0
	for i in range(len(temp)):
		b += int(temp[i]) * power(100, len(temp)-i)
		
	if n:
		return b/power(10, n+1)
	else:
		return b

def trade_type(type):			#交易类型字符串
	a = bin(int(type, 16))
	type_length = len(a) - 2
	base = extend = ''

	if type[1] == '0' :
		base = '正常加油'
	if type[1] == '1' :
		base = '逃卡'
	if type[1] == '2' :
		base = '错卡'
	if type[1] == '3' :
		base = '补扣'
	if type[1] == '4' :
		base = '补充'
	if type[1] == '5' :
		base = '员工上班'
	if type[1] == '6' :
		base = '员工下班'
	if type[1] == '7' :
		base = '非卡'
	if type[1] == '8' :
		base = '油价接收'
	if type[1] == '9' :
		base = '卡片交易出错'	

	if type_length == 5:
		extend = '扣款签名有效'

	if type_length == 7:
		if a[4] == '1' :
			extend = '使用油机黑（白）名单，扣款签名有效'
		else:
			extend = '使用后台黑（白）名单，扣款签名有效'

	if type_length == 8:
		if (a[3] == '0') & (a[5] == '0'):
			extend = '卡错，使用后台黑（白）名单'
		if (a[3] == '0') & (a[5] == '1'):
			extend = '卡错，使用后台黑（白）名单，扣款签名有效'
		if (a[3] == '1') & (a[5] == '0'):
			extend = '卡错，使用油机黑（白）名单'
		if (a[3] == '1') & (a[5] == '1'):
			extend = '卡错，使用油机黑（白）名单，扣款签名有效'
	if type_length > 4:
		return extend + '，' + base
	else:
		return base

def case31(data):				#加油机发送实时信息命令
	if bcd_decimal(data[13:18], 0) < 2 :
		return 'data error\n'
	operate = '\n'
	operate2 = operate1 = ''
	data_list = data.split(' ')
	count = data_list[8]
	data_id = data_list[9]
	nozzle = data_list[10]
	#nozzle = str(string.atoi(data_list[10], 16))
	if count == '00':			#信息数量 = 1
		operate ='命令字: ' + data_list[7] + '（加油机发送实时信息，无卡插入）\n'
		return operate
	if count == '01':			#信息数量 = 1
		if data_id == '01':		#卡插入
			operate ='命令字: ' + data_list[7] + '(卡插入);枪号：' + hex_decimal(nozzle, 0) + ';卡号：' + data[34:63] + ';卡状态：' + data[64:69] + ';卡余额：' + hex_decimal(data[70:81], 2) + '\n'
			return operate			
		if data_id == '02':		#抬枪或加油中
			operate ='命令字: ' + data_list[7] + '加油中;枪号：' + hex_decimal(nozzle, 0) + ';结算单位：' + data[31:33] + ';数额：' + hex_decimal(data[34:42], 2) + ';升数：' + hex_decimal(data[43:51],2) + ';价格：' + hex_decimal(data[52:57],2) + '\n'
			return operate

	if count == '02':			#信息数量 = 2
		if data_id == '01':		#A卡插入
			operate1 ='命令字: ' + data_list[7] + '(卡插入);枪号：' + hex_decimal(nozzle, 0) + ';卡号：' + data[34:63] + ';卡状态：' + data[64:69] + ';卡余额：' + hex_decimal(data[70:81],2) + '\n'
			data_id2 = data[82:84]
			if data_id2 == '01':	#B卡插入
				operate2 = '(卡插入);枪号：' + hex_decimal(data[85:87], 0) + ';卡号：' + data[91:120] + ';卡状态：' + data[121:126] + ';卡余额：' + hex_decimal(data[127:138],2) + '\n'
			if data_id2 == '02':	#B加油中
				operate2 = '加油中;枪号：' + hex_decimal(data[85:87], 0) + ';结算单位：' + data[88:90] + ';数额：' + hex_decimal(data[91:99], 2) + ';升数：' + hex_decimal(data[100:108], 2)  + ';价格：' + hex_decimal(data[109:114],2) + '\n'
			
			return operate1 + operate2

		if data_id == '02':		#A加油中
			operate1 ='命令字: ' + data_list[7] + '加油中;枪号：' + hex_decimal(nozzle, 0) + ';结算单位：' + data[31:33] + ';数额：' + hex_decimal(data[34:42], 2) + ';升数：' + hex_decimal(data[43:51],2) + ';价格：' + hex_decimal(data[52:57],2) + '\n'
			data_id2 = data[58:60]
			if data_id2 == '01':	#B卡插入
				operate2 = '命令字: ' + data_list[7] + '(卡插入);枪号：' + hex_decimal(data[61:63], 0) + ';卡号：' + data[67:96] + ';卡状态：' + data[97:102] + ';卡余额：' + hex_decimal(data[103:114],2) + '\n'
			if data_id2 == '02':	#B加油中
				operate2 = '命令字: ' + data_list[7] + '加油中;枪号：' + hex_decimal(data[61:63], 0) + ';结算单位：' + data[64:66] + ';数额：' + hex_decimal(data[67:75],2) + ';升数：' + hex_decimal(data[76:84],2) + ';价格：' + hex_decimal(data[85:90],2) + '\n'
			
			return operate1 + operate2

	return operate

def case320(data):				#加油机发送成交数据
	if bcd_decimal(data[13:18], 0) < 96 :
		return 'data error\n'
	operate = ''
	operate = '枪号：' + hex_decimal(data[223:225], 0) + ',POS-TTC：' + hex_decimal(data[22:33], 0)  + ',交易时间：' + data[37:57] + ',交易类型：' + trade_type(data[34:36]) + ',卡号：' + data[58:87] + ',余额：' + hex_decimal(data[88:99],2) + ',金额：' + hex_decimal(data[100:108],2) + ',单价：' + hex_decimal(data[241:246],2) + ',升数：' + hex_decimal(data[232:240],2) + ',油品：' + data[226:231] + ',升累计：' + hex_decimal(data[250:261],2) + '\n'	
	return operate

def case321(data):				#PC机回应成交数据
	if bcd_decimal(data[13:18], 0) != 2 :
		return 'data error\n'

	data_list = data.split(' ')
	result = data_list[8]
	if bin(int(result, 16))[-1:] == '0' :			#b0 = 0:正确; b0 = 1:T-MAC错
		return '命令字：' + data_list[7] + '(PC机回应成交数据),结果：正确\n'
	else:
		return '命令字：' + data_list[7] + '(PC机回应成交数据),结果：T-MAC错\n'

def case360(data):				#加油机申请查询黑/白名单
	data_list = data.split(' ')
	card_no = data[22:51]

	return '命令字: ' + data_list[7] + '（加油机向PC机查询黑/白名单）'+';卡号：' + card_no +'\n'

def case361(data):				#PC机黑/白名单查询结果
	data_list = data.split(' ')
	flag = data_list[8]
	card_type = data_list[11]
	
	if bin(int(flag, 16))[-1:] == '0' :			#匹配
		if card_type == '01':	#用户卡不能加油
			return '命令字: ' + data_list[7] + '（PC机黑/白名单查询结果）;结果：匹配（用户卡不能加油）\n'
		if (card_type == '04')|(card_type == '05')|(card_type == '06'):	#内部卡可以能加油
			return '命令字: ' + data_list[7] + '（PC机黑/白名单查询结果）;结果：匹配（内部卡可以加油）\n'

	else:
		if card_type == '01':	#用户卡可以加油
			return '命令字: ' + data_list[7] + '（PC机黑/白名单查询结果）;结果：不匹配（用户卡可以加油）\n'
		if (card_type == '04')|(card_type == '05')|(card_type == '06'):	#内部卡可以能加油
			return '命令字: ' + data_list[7] + '（PC机黑/白名单查询结果）;结果：不匹配（内部卡不能加油）\n'

def cmd0(command, data):		#油机发送
	if command == '31':
		return case31(data)

	if command == '32':
		return case320(data)

	if command == '36':
		return case360(data)

	else:
		return 'unknown\n'

def cmd1(command, data):		#油机接收
	if command == '32':
		return case321(data)

	if command == '36':
		return case361(data)

	else:
		return 'unknown\n'
	
def analyze_cmd(type, data):	#type:	0-油机发送;	1—油机接收
	operate = ''
	data_list = data.split(' ')
	command = data_list[7]
	if type == 0:
		operate = cmd0(command, data)

	else:
		operate = cmd1(command, data)

	return operate

def analyze_line(oneline):
	end = ''
	snd_rcv = 1
	direction = ' 管控——>油机，'
	a = oneline_item()
	string = oneline.split(',')
	a.date = string[0]
	a.time = string[1]
	a.type = string[2]
	a.port = string[3]
	a.data = string[4].split(':')[1]

	if a.type == 'Recv:':
		snd_rcv = 0				#0-油机发送;	1—油机接收
		direction = ' 油机——>管控，'

	length_string1 = a.data[13:15]
	length_string2 = a.data[16:18]
	total_length = int(length_string1)*100 + int(length_string2) + 9
	
				
	if len(a.data.split(' ')) == total_length:
		result = analyze_cmd(snd_rcv, a.data)
		end = '时间：' + a.date + ' ' + a.time + direction + str(result)
	else:
		end = '时间：' + a.date + ' ' + a.time + direction + 'data length is error\n'
		
	return end
	
def analyze(filename):
	sourcefile = open(filename, 'r')	#源文件a.log
	filename = open('oildata_1.log', 'w')	#解析后的日志a_1.log
	oneline = sourcefile.readline()
	while oneline:
		if len(oneline) < 10:
			filename.write('\n')			#空行，写回车，读取下一行
			oneline = sourcefile.readline()
			continue
		
		filename.write(oneline)					#写入原始数据
		handled_with = analyze_line(oneline)	#解析数据
		filename.write(handled_with)			#写入解析数据
		oneline = sourcefile.readline()

	sourcefile.close()	#关闭文件
	filename.close()

def main():

	if len(sys.argv) != 3:
		command = sys.argv[0].split('\\')[len(sys.argv[0].split('\\')) - 1]
		print 'Usage: ' + command + ' file.log  Nozzle_no'
		sys.exit()
		
	version = 'Version: 1.0.0.2'
	print '\n****** Analyze oil data ******\n' + version
	print '\nNote: Add trade information (TTC) '
	print '\nNote: Requaired input the parameter called Nozzle_no.(base 10)\n'
	
	Nozzle_no = decimal_hex(sys.argv[2], 1)
		
	fp_src = open(sys.argv[1], 'r')
	fp_dest = open('oildata.log', 'w')
	
	old_type = 0	#初始配置
	lastline = ''
	last_liter = 0
	oneline = fp_src.readline()
	while oneline:
		data = oneline.split(',')[4].split(':')[1]	#数据
		card_string1 = '31 01 01 ' + Nozzle_no					#实时信息：插卡
		card_string2 = '36'							#查询黑白名单
		oil_string = '31 01 02 ' + Nozzle_no
		trade_string = '96 32'
		card_status1 = data[19:30]					# 31 01 01
		card_status2 = data[19:21]					# 36
		oil_status = data[19:30]					# 31 01 02
		trade_status = data[16:21]					# 96 32

		if (card_status1 == card_string1) | (card_status2 == card_string2):
			oil_type = 1	#插卡或者验卡状态
			last_liter = 0
		if oil_status == oil_string:
			oil_type = 2	#加油状态
		if trade_status == trade_string:		#交易数据
			#last_liter = 0
			trade_liter = int(hex_decimal(data[232:240], 0))
			Nozzle_no = int(hex_decimal(data[223:225], 0))
			if old_type == 2:	#加油状态切换到上传交易
				fp_dest.write(lastline)
				if trade_liter != last_liter:	#不是同一笔交易数据
					fp_dest.write('\n')
				fp_dest.write(oneline + '\n')
			if old_type == 1:	#插卡切换到上传交易数据
				fp_dest.write(lastline + '\n')
				fp_dest.write(oneline + '\n')

			if (old_type == 3) | (old_type == 0):	#上一条也是上传交易
				fp_dest.write(oneline + '\n')

			old_type = 3
			oneline = fp_src.readline()		#非插卡或加油状态，跳过
			continue

		if (card_status1 != card_string1) & (card_status2 != card_string2) & (oil_status != oil_string) & (trade_status != trade_string):
			oneline = fp_src.readline()		#非插卡或加油状态，跳过
			continue
		if 3 != old_type:		
			if old_type == oil_type:	#与上一行的状态相同
				if oil_type == 2:		#都是加油状态
					oil_liter = int(hex_decimal(data[43:51], 0))
					if oil_liter < last_liter:	#实时数据小于上一行
						fp_dest.write(lastline + '\n')	#写入上一行
						fp_dest.write(oneline)
					last_liter = oil_liter
				lastline = oneline

			if old_type != oil_type:						#状态切换
				if old_type == 1:		#从插卡切换到加油，写入当行
					fp_dest.write(lastline)
					fp_dest.write(oneline)
				if old_type == 2:		#从加油切换到插卡，写入回车
					fp_dest.write('\n')

		if 3 == old_type:				#从交易切换到加油
			if oil_type == 2:
				fp_dest.write(oneline)
				last_liter = 0
			if oil_type == 1:
				pass
					
		lastline = oneline
						
		old_type = oil_type	#读取下一行
		oneline = fp_src.readline()

	if (card_status1 == card_string1) | (card_status2 == card_string2) | (oil_status == oil_string) | (trade_status == trade_string):
		fp_dest.write(lastline + '\n')
	fp_src.close()	#关闭文件
	fp_dest.close()

	analyze('oildata.log')

if __name__ == '__main__':
	main()