import os,sys,subprocess

'''
os.system('python ./Waiau/test.py')

os.system('python ./Waiau/dc-legislation/newLegislationPull.py')
os.chdir(sys.path[0])
os.system('python ./Waiau/dc-legislation/processLeg.py')
os.chdir(sys.path[0])
'''



os.chdir(sys.path[0])
print(sys.path[0])
subprocess.call('python3 %s/Waiau/dc-legislation/newLegislationPull.py'%(str(sys.path[0])))
os.chdir(sys.path[0])
subprocess.call('python3 ./Waiau/dc-legislation/processLeg.py')
os.chdir(sys.path[0])
git_command_add = 'git add --all'
git_command_commit = "git commit -m 'Automated push from rambuDrive...'"
git_command_push = 'git push --all'

subprocess.call(git_command_add)
subprocess.call(git_command_commit)
subprocess.call(git_command_push)
