import subprocess
import shutil
import sys

import utils
from utils import LogLevel, printMessage

def runScript(script, output_to_console=False):
	try:
		if output_to_console:
			output = subprocess.call(script, shell=True)
		else:
			output = subprocess.call(script, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		if output == 0:
			return True
		else:
			return False
	except subprocess.CalledProcessError as error:
		printMessage(LogLevel.MANDATORY, "Error code is {}, output {}".format(error.returncode, error.output))
		return False

def runBuildScript(script, out_dir, revision):
	printMessage(LogLevel.INFO, "Building {} ...".format(revision))
	sDate = utils.convertDate(revision.committed_date)
	short_rev = str(revision)[0:7]
	if runScript(script) == True:
		new_dir = out_dir + "_" + short_rev + "_" + sDate
		printMessage(LogLevel.MANDATORY, "Build script ran successfully. Moving dir binaries to {} ...".format(new_dir))
		try:
			shutil.copytree(out_dir, new_dir, symlinks=True)
			printMessage(LogLevel.INFO, "Binaries is successfully moved to {}".format(new_dir))
			return new_dir
		except:
			printMessage(LogLevel.MANDATORY, "Caught exception ", sys.exc_info())
	else:
		printMessage(LogLevel.MANDATORY, "Build failed for gitid [{}] date [{}]".format(revision, sDate))
		return None


def runTestScript(script):
	if runScript(script) == False:
		printMessage(LogLevel.MANDATORY, "Test failed")
		return False
	else:
		printMessage(LogLevel.MANDATORY, "Test went successfully")
		return True
