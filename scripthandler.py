import subprocess
import shutil
import sys

import utils

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
		print ("Error code is {}, output {}".format(error.returncode, error.output))
		return False

def runBuildScript(script, out_dir, revision):
	print ("Building {} ...".format(revision))
	sDate = utils.convertDate(revision.committed_date)
	short_rev = str(revision)[0:7]
	if runScript(script) == True:
		new_dir = out_dir + "_" + short_rev + "_" + sDate
		print ("Build script ran successfully. Moving dir binaries to {} ...".format(new_dir))
		try:
			shutil.copytree(out_dir, new_dir, symlinks=True)
			print ("Binaries is successfully moved to {}".format(new_dir))
			return new_dir
		except:
			print ("Caught exception ", sys.exc_info())
	else:
		print ("Build failed for gitid [{}] date [{}]".format(revision, sDate))
		return None


def runTestScript(script):
	if runScript(script) == False:
		print("Test failed")
		return False
	else:
		print("Test went successfully")
		return True
