#-*- coding: utf-8 -*-
import sys
#import string

def power(base, n):				#16进制转10进制：base = 256
	if n == 1:
		return 1
	return base*power(base, n-1)

def time_second(time):			#时间转换成秒， 返回值int
	second = 0
	time_list = time.split(':')
	for i in range(len(time_list)):
		second += int(time_list[i])*power(60, len(time_list)-i)

	return second

def time_span(time1, time2):	#计算时间间隔，返回值int

	return math.fabs(time_second(time2) - time_second(time1))	


def main():
	if len(sys.argv) != 4:
		command = sys.argv[0].split('\\')[len(sys.argv[0].split('\\')) - 1]
		print 'Usage: ' + command + ' log_file  start_time  end_time (time format: HH:MM:SS)'
		sys.exit()

	fp_src = open(sys.argv[1], 'r')
	fp_dest = open('temp.log', 'w')
	oneline = fp_src.readline()
	while oneline:
		if len(oneline) < 30:
			oneline = fp_src.readline()
			continue

		value = time_second(oneline.split(',')[1])
		time_min = time_second(sys.argv[2])
		time_max = time_second(sys.argv[3])
		if ((value >= time_min) & (value <= time_max)):
			fp_dest.write(oneline)
		if value > time_max:
			break

		oneline = fp_src.readline()

	fp_src.close()
	fp_dest.close()

if __name__ == '__main__':
	main()