from git import Repo
from git import Git
import git
import shutil
from enum import Enum

import utils
from bblogger import Logger, LogLevel
import scripthandler
import settings


STR_STASH_ERROR = "Please, commit your changes or stash them before you can merge."
STR_STASH_ERROR_BRANCH = "Please, commit your changes or stash them before you can switch branches"
STR_CLEAN_ERROR = "Please move or remove them before you can switch branches"

class GitErrorType(Enum):
	UknownError = 1
	StashError = 2,
	ErrorClean = 3,

Log = Logger()

def handleGitError(str_error):
	lines_list = str(str_error).split('\n')
	for line in lines_list:
		if line.find(STR_STASH_ERROR) != -1 or line.find(STR_STASH_ERROR_BRANCH) != -1:
			Log.Log (LogLevel.DEBUG, "Found stash")
			return GitErrorType.StashError
		if line.find(STR_CLEAN_ERROR) != -1:
			Log.Log (LogLevel.DEBUG, "Found clear error")
			return GitErrorType.ErrorClean
	return GitErrorType.UknownError

def getRevision(repo, rev_name, force = False):
	try:
		if type(rev_name) == git.refs.head.Head:
			Log.Log (LogLevel.MANDATORY, "Switching to ", rev_name)
		else:
			Log.Log (LogLevel.MANDATORY, ("Switching to commit id {}, author {}, date {} ...").format(rev_name, rev_name.author, utils.convertTimeDate(rev_name.committed_date)))
		repo.git.checkout(rev_name)
	except git.exc.GitCommandError as error:
		Log.Log (LogLevel.MANDATORY, "Following error during checkout - [{}]".format(error))
		gitError = handleGitError(error)

		if gitError == GitErrorType.StashError:
			try:
				Log.Log (LogLevel.MANDATORY, "Stashing...")
				repo.git.stash("save")
				repo.git.checkout(rev_name)
			except git.exc.GitCommandError as error:
				Log.Log (LogLevel.MANDATORY, "Following error during stash and checkout - [{}]".format(error))
		elif gitError == GitErrorType.ErrorClean and force:
			try:
				Log.Log (LogLevel.MANDATORY, "Cleaning unversioned files...")
				repo.git.clean("-xdf")
				repo.git.checkout(rev_name)
			except git.exc.GitCommandError as error:
				Log.Log (LogLevel.MANDATORY, "Failed to get {} revision".format(rev_name))
				return False
		else:
			Log.Log (LogLevel.MANDATORY, "Error is currently unknown. Please check your git repo manually. Thanks for understanding")	
			return

	return True


def collectBuilds(repo, config_dict):
	start_interval = config_dict[settings.START_INTERVAL]
	end_interval = config_dict[settings.END_INTERVAL]
	
	if utils.checkDate(end_interval) != None:
		seconds = utils.convertDateToSec(end_interval)
		end_interval = getFirstDateCommit(repo, seconds)
	if utils.checkDate(start_interval) != None:
		seconds = utils.convertDateToSec(start_interval)
		start_interval = getFirstDateCommit(repo, seconds)

	if start_interval == None:
		str_interval = "master..." + config_dict[settings.END_INTERVAL]
	else:
		str_interval = start_interval + "..." + end_interval
	all_commits = repo.iter_commits(str_interval)
	for commit in all_commits:
		if not getRevision(repo, commit, True if config_dict.get(settings.FORCE_PULL, False) == True else False):
			continue
		scripthandler.runBuildScript(config_dict[settings.BUILD_SCRIPT], config_dict[settings.OUTPUT_DIR], commit)

def handleIndex(index, bIsFailed):
	if not bIsFailed:
		if index < 2:
			index += 1
		else:
			index += int(index / 2)
	else:
		if index < 2:
			index -= 1
		else:
			index -= int(index / 2)

	return index

def checkIndexExtreme(index):
	if index >= len(all_commits):
		Log.Log(LogLevel.MANDATORY, "There are no working versions in the git range set")
		return False
	if index < 0:
		Log.Log(LogLevel.MANDATORY, "All checked versions are working")
		return False

	return True

def getLastWorkVersion(repo, config_dict, bKeepBuilds = False):
	work_commit = config_dict[settings.LAST_WORK]
	if utils.checkDate(work_commit) != None:
		seconds = utils.convertDateToSec(work_commit)
		work_commit = getFirstDateCommit(repo, seconds)
	str_interval = "master..." + config_dict[settings.LAST_WORK]
	all_commits = list(repo.iter_commits(str_interval))
	
	bLoop = True
	bPreviosCall = True #consider that the first call is trully successfull
	prev_index = len(all_commits)
	index = int(prev_index / 2)
	while bLoop:
		Log.Log(LogLevel.DEBUG, "prev_index {}, index {}".format(prev_index, index))
		commit = all_commits[index]
		if not getRevision(repo, commit, True if config_dict.get(settings.FORCE_PULL, '0') == '1' else False):
			break
		
		sBuildPath = scripthandler.runBuildScript(config_dict[settings.BUILD_SCRIPT], config_dict[settings.OUTPUT_DIR], commit)
		if sBuildPath == None:
			continue
		bCurrentCall = scripthandler.runTestScript(config_dict[settings.TEST_SCRIPT])
		if not bCurrentCall:
			Log.Log(LogLevel.DEBUG, "Index is {}".format(abs(prev_index-index)))
			if bPreviosCall and abs(prev_index-index) == 1:
				bLoop = False
				Log.Log(LogLevel.MANDATORY, "The last working version is {}".format(all_commits[prev_index]))	
				Log.Log(LogLevel.MANDATORY, "System is broken since {}, author {}, message '{}', date {}".format(commit, commit.author, commit.message, utils.convertTimeDate(commit.committed_date)))
				break
		else:
			if not bPreviosCall and abs(prev_index-index)== 1:
				Log.Log(LogLevel.MANDATORY, "The previos call was successfull. This one breaks everything")
			
		bPreviosCall = bCurrentCall
		prev_index = index
		index = handleIndex(index, bCurrentCall)
		if not checkIndexExtreme(index):
			break

		if not bKeepBuilds:
			shutil.rmtree(sBuildPath, True)


#NOTE: the last commit has zero index 
def getFirstDateCommit(repo, seconds):
	all_commits = list(repo.iter_commits())
	commit_index = int(len(all_commits) / 2)
	
	index_list = list()
	while abs(all_commits[commit_index].committed_date-seconds) > utils.SECONDS_IN_DAY:
		
		if all_commits[commit_index].committed_date < seconds:
			commit_index -= int(commit_index / 2)
		else:
			commit_index += int(commit_index / 2)

		if commit_index in index_list:
			Log.Log (LogLevel.MANDATORY, "Did not find commit for {} date. Will find the closest one for previous date {}".format(utils.convertTimeDate(seconds), utils.convertTimeDate(seconds - utils.SECONDS_IN_DAY)))
			seconds -= utils.SECONDS_IN_DAY
			getFirstDateCommit(repo, seconds)
			return
		index_list.append(commit_index) #TODO: think about search interval how, unability to find a proper commit could be found sooner

		if commit_index > len(all_commits) or commit_index < 0:
			return
		#Log.Log (LogLevel.DEBUG,"Found commit id {} for commit date {}".format(all_commits[commit_index], utils.convertTimeDate(all_commits[commit_index].committed_date)))

	commit = all_commits[commit_index]
	Log.Log(LogLevel.MANDATORY,"Git id is {}, author {}, message '{}', date {}".format(commit, commit.author, commit.message, utils.convertTimeDate(commit.committed_date)))
	return commit

