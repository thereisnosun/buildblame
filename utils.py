import time
import datetime
import re
import sys
from bblogger import Logger, LogLevel

SECONDS_IN_DAY = 86400

Log = Logger()

def convertTimeDate(seconds):
	time_object = time.gmtime(seconds)
	str_time = "{}-{}-{} {}:{}:{}".format(time_object.tm_year, time_object.tm_mon, time_object.tm_mday, time_object.tm_hour, time_object.tm_min, time_object.tm_sec)
	return str_time

def convertDate(seconds):
	time_object = time.gmtime(seconds)
	str_time = "{}-{}-{}".format(time_object.tm_year, time_object.tm_mon, time_object.tm_mday)
	return str_time

def checkDate(str_date, bIsMandatory = False):
	if str_date == None:
		return None
	match = re.findall("(\d+)\.(\d+)\.(\d+)", str_date) 
	if len(match) < 1:
		if bIsMandatory:
			Log.Log (LogLevel.MANDATORY, "Wrong date format at all!")
		return None

	if len(match[0]) < 3:
		if bIsMandatory:
			Log.Log (LogLevel.MANDATORY, "Wrong date format!")
		return None

	return match


def convertDateToSec(str_time):
	match = checkDate(str_time, True)	
	if match == None:
		return 0
	Log.Log (LogLevel.DEBUG, match[0][0], match[0][1], match[0][2])

	try:
		year, month, day = int(match[0][0]), int(match[0][1]), int(match[0][2])
		time_zone = datetime.timezone(datetime.timedelta())
		total_secs = datetime.datetime(year, month, day, tzinfo = time_zone).timestamp()
		Log.Log (LogLevel.DEBUG, convertTimeDate(total_secs))
		return int(total_secs)
	except ValueError as error:
		Log.Log (LogLevel.MANDATORY, "Incorrect date format [{}]".format(error))
	except:
		Log.Log (LogLevel.MANDATORY, "Unexpected error:", sys.exc_info()[0])

	return 0

def findClosestNumber(numbers_list, number):
	numbers_list.sort()
	index = numbers_list.index(number)
	prev_index = index - 1
	next_index = index + 1
	if prev_index < 0:
		return next_index

	if next_index >= len(numbers_list):
		return prev_index

	if abs(numbers_list[index] - numbers_list[prev_index]) < abs(numbers_list[next_index] - numbers_list[prev_index]):
		return numbers_list[prev_index]
	else:
		return numbers_list[next_index]
