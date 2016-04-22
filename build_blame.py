import sys
import os
from git import Repo

import utils
from bblogger import Logger, LogLevel
import settings
import githandler

def main():
	config = settings.parseConfig(settings.DEFAULT_CONFIG_FILE)
	if config == None:
		sys.exit()

	Log = Logger()
	Log.SetLogLevel(config.get(settings.VERBOSE))

	repo_path = config.get(settings.REPO)
	Log.Log(LogLevel.INFO, "Path is {}".format(repo_path))
	repo = Repo(repo_path)
	if repo.bare:
		Log.Log (LogLevel.MANDATORY, "The repository is bare!")
		exit()
	else:
		Log.Log (LogLevel.INFO, "Repository is inited")

	active_branch = None
	try:
		active_branch = repo.active_branch
		Log.Log (LogLevel.MANDATORY, "Current branch is {}. Head is {} Commit is {}".format(active_branch, repo.head, active_branch.commit))
	except TypeError as error:
		Log.Log (LogLevel.MANDATORY, "The error has happened {}".format(error))

	Log.Log (LogLevel.MANDATORY, "If there are any files which blocks checkout - they will be stashed")

	if config.get(settings.FORCE_PULL):
		Log.Log (LogLevel.MANDATORY, "Warning! Force flag is set. In case of conflicts \"git reset --hard\" can be used.")		

	collect_builds = config.get(settings.COLLECT_BUILDS)
	last_work = config.get(settings.FIND_LAST_WORK)
	if last_work:
		Log.Log (LogLevel.MANDATORY, "Will find the last working version")
		if collect_builds:
			Log.Log (LogLevel.MANDATORY, "All builds will be kept")
		githandler.getLastWorkVersion(repo,config)
	else:
		Log.Log (LogLevel.MANDATORY, "Will collect builds from given gitid range")
		githandler.collectBuilds(repo, config)

	if active_branch != None:
		githandler.getRevision(repo, active_branch, True)

if __name__ == "__main__":
	main()

'''
TODO:
1) Add ability to track changes only from specific folders
2) Add ability to collect builds from different branches as well
'''



