# buildblame
Script for control repository builds and its functionality

In order to run this script you need to have:
Python 3.4 version

GitPython installed on your system - https://github.com/gitpython-developers/GitPython

Current version is working and tested on Windows 10.

This script main goal is to control repository versions correctness.

Current version supports two major features:

1. Find the last working build if current functionality is broken.

2. Collect builds from range of git commits.

- To find the last working build you must be aware about the last version which works "for sure". It could be either gitid or date.
Then, by setting the build script and script for test functionality you can find the very last git commit which brakes certain functionality.(Please, refer to config for more detailed information.) Also you have to set such mandatory variables like output dir - place where builds will be kept(you can either set the option to kep each build or only to keep the last one) and repo path - path to your root repository folder.

- Also there is an ability to collect script for certain data range or gitid range(please, refer to config for more details). If such kind of functionality is choosen, then script will collect and store builds in output folder.


If you have any questions or remarks feel free to contact me. Enjoy :)
