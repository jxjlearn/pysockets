'''
need to run it at ~
#message as input
#string after [s] should be sha1
#check if  this sha has been synced
#run akquiltsync with sha1 as input
#then run step 3-5 of notes until change report generation
#send request to master
'''
import subprocess
import sys

gminHome = '~/gmin-quilt-representation/'
localRepo = '~/test/'
remoteUrl = 'https://xjjiao@github.com/intel-otcak/test.git'
kernelType = 'cht-m1stable'



sha1 = '4200ebb7bb687dbfa1391ae6d615542fa8c741db'
print >>sys.stderr, '>>sha1:%s' % sha1

#need to sync
print >>sys.stderr, '>>akquitsync is running...'
cmd = 'cd ' + gminHome + ' && ' + './bin/akquiltsync ' + '-k ' + kernelType + ' ' + sha1
subprocess.check_call(cmd, shell=True)
#subprocess.check_call([gminHome + 'bin/akquiltsync', '-k', kernelType, sha1])

#clone the remote repo
print >>sys.stderr, '>>removing the local repo %s...' % localRepo
subprocess.call('rm -rf ' + localRepo, shell=True)
print >>sys.stderr, '>>cloning github repo...'
cmd = 'cd ~ ' + '&& ' + 'git clone ' + remoteUrl
subprocess.call(cmd, shell=True)
#After akquiltsync finishes, the repo is on a specific branch created by the script.
#Copy the patches to github repo.
print >>sys.stderr, '>>updating the patches in github local copy...'
cmd = 'rm' + ' -rf ' + localRepo + 'uefi/cht-m1stable/patches'
subprocess.call(cmd, shell=True)

cmd1 = 'cd ' + gminHome + 'uefi/cht-m1stable '
cmd2 = 'find patches | cpio -pdmu ' + localRepo + 'uefi/cht-m1stable'
subprocess.call(cmd1 + '&& ' + cmd2, shell=True)

#Update technical debt report
cmd = 'cd ' + gminHome
print >>sys.stderr, '>>Generating TechnicalDebtSymmary.csv...'
subprocess.call(cmd + ' && ' + './bin/akgroup ' + '-c ' + '-d ' + 'uefi/cht-m1stable/patches ' + '> ' + localRepo + 'uefi/cht-m1stable/TechnicalDebtSummary.csv', shell=True)
print >>sys.stderr, '>>Generating TechnicalDebt.csv...'
subprocess.call(cmd + ' && ' + './bin/akgroup ' + '-cv ' + '-d ' + 'uefi/cht-m1stable/patches ' + '> ' + localRepo + 'uefi/cht-m1stable/TechnicalDebt.csv', shell=True)

#get the difference between updated series and github one
print >>sys.stderr, '>>saving the git diff into "git-diff.txt"...'
with open('git-diff.txt', 'w') as diffFile :
	subprocess.call('cd ' + localRepo + ' && ' + 'git diff uefi/cht-m1stable/patches/series', shell=True, stdout=diffFile, stderr=diffFile)

