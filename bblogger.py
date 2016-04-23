from enum import IntEnum
import datetime
import utils

class LogLevel(IntEnum):
	MANDATORY = 1,
	INFO = 2,
	DEBUG = 3

#TODO: make it singleton
class Logger:
	logLevel = None

	def __init__(self):
		self.logLevel = LogLevel.MANDATORY

	def SetLogLevel(self, currentlogLevel):
		if currentlogLevel == "1":
			self.logLevel = LogLevel.MANDATORY
		elif currentlogLevel == "2":
			self.loglevel = LogLevel.INFO
		elif currentLogLevel == "3":
			self.logLevel = LogLevel.DEBUG

	def Log(self, *arg):
		currentLogLevel = None

		args_list = list()
		for argument in arg:
			if type(argument) == LogLevel:
				currentLogLevel = argument
			else:
				args_list.append(argument)

		if currentLogLevel == None:
			print("buildblame: Incorrect usage of Logger::Log!")
			return

		if currentLogLevel < self.logLevel:
			return

		time_stamp_pos = datetime.datetime.now().timestamp()
		time_stamp = utils.convertTimeDate(time_stamp_pos, True)

		logMessage = "buildblame[{}]: ".format(time_stamp)	
		
		for argument in args_list:
			if type(argument) == str:
				logMessage += argument
			else:
				logMessage += str(argument)
			logMessage += " "

		print(logMessage)

	