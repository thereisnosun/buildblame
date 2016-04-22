import configparser
from bblogger import Logger, LogLevel

DEFAULT_CONFIG_FILE = "config.ini"

TEST_BUILD_SECTION = "TEST_BUILD"
GIT_SECTION = "GIT"
OPTIONS_SECTION = "OPTIONS"

BUILD_SCRIPT = "build_script"
OUTPUT_DIR = "output_dir"
TEST_SCRIPT = "test_script"

REPO = "repo_path"
START_INTERVAL = "start_interval"
END_INTERVAL = "end_interval"
LAST_WORK = "last_working"

FORCE_PULL = "force_pull"
VERBOSE = "verbose"
COLLECT_BUILDS = "collect_builds"
FIND_LAST_WORK = "find_last_work_version"

Log = Logger()

def checkConfig(config_dict):
	mandatory_args = [BUILD_SCRIPT, OUTPUT_DIR, REPO]
	bIsArgsOk = True
	for argument in mandatory_args:
		if config_dict.get(argument) == None:
			Log.Log(LogLevel.MANDATORY, "Please specify {} mandatory argument".format(argument))
			bIsArgsOk = False

	if not bIsArgsOk:
		return False

	find_last_working = config_dict.get(FIND_LAST_WORK, False)
	
	if not find_last_working:
		colect_builds = config_dict.get(COLLECT_BUILDS, True)
		if config_dict.get(END_INTERVAL) == None:
			Log.Log(LogLevel.MANDATORY, "Only collect builds options is set. Please, specify end interval.")
			return False
	else:
		colect_builds = config_dict.get(COLLECT_BUILDS, False)
		if config_dict.get(LAST_WORK) == None:
			Log.Log(LogLevel.MANDATORY, "Please specify the last date or gitid, when the version was stable")
			return False
		if config_dict.get(TEST_SCRIPT) == None:
			Log.Log(LogLevel.MANDATORY, "You choose option to indetify broken systemversion. Plese specify script for testing")
			return False

	return True


def parseConfig(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)

	sections_list = config.sections()
	if TEST_BUILD_SECTION not in sections_list:
		Log.Log(LogLevel.MANDATORY, "Please check {} section".format(TEST_BUILD_SECTION))
		return None

	if GIT_SECTION not in sections_list:
		Log.Log(LogLevel.MANDATORY, "Please check {} section".format(GIT_SECTION))
		return None

	Log.Log(LogLevel.DEBUG, "Config values are: ")
	config_dict = dict()
	for section in config:
		for argument in config[section]:
			value = config[section][argument]
			Log.Log(LogLevel.DEBUG, argument, "=", value)
			if value == "YES":
				config_dict[argument] = True
			elif value == "NO":
				config_dict[argument] = False
			else:
				if value != "" and value != " ":
					config_dict[argument] = value

	if not checkConfig(config_dict):
		return None

	return config_dict


		

