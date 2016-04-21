import sys
import os
from git import Repo

import utils
from utils import LogLevel
from utils import printMessage
import settings
import githandler

def main():
	config = settings.parseConfig(settings.DEFAULT_CONFIG_FILE)
	if config == None:
		sys.exit()

	repo_path = config.get(settings.REPO)
	printMessage(LogLevel.INFO, "Path is {}".format(repo_path))
	repo = Repo(repo_path)
	if repo.bare:
		printMessage (LogLevel.MANDATORY, "The repository is bare!")
		exit()
	else:
		printMessage (LogLevel.INFO, "Repository is inited")

	active_branch = None
	try:
		active_branch = repo.active_branch
		printMessage (LogLevel.MANDATORY, "Current branch is {}. Head is {} Commit is {}".format(active_branch, repo.head, active_branch.commit))
	except TypeError as error:
		printMessage (LogLevel.MANDATORY, "The error has happened {}".format(error))

	printMessage (LogLevel.MANDATORY, "If there are any files which blocks checkout - they will be stashed")

	if config.get(settings.FORCE_PULL):
		printMessage (LogLevel.MANDATORY, "Warning! Force flag is set. In case of conflicts \"git reset --hard\" can be used.")		

	collect_builds = config.get(settings.COLLECT_BUILDS)
	last_work = config.get(settings.FIND_LAST_WORK)
	# if last_work:
	# 	printMessage (LogLevel.MANDATORY, "Will find the last working version")
	# 	if collect_builds:
	# 		printMessage (LogLevel.MANDATORY, "All builds will be kept")
	# 	githandler.getLastWorkVersion(repo,config)
	# else:
	# 	printMessage (LogLevel.MANDATORY, "Will collect builds from given gitid range")
	# 	githandler.collectBuilds(repo, config)

	# if active_branch != None:
	# 	githandler.getRevision(repo, active_branch, True)

if __name__ == "__main__":
	main()

'''
TODO:
1) Add ability to track changes only from specific folders
2) Add ability to collect builds from different branches as well
'''



