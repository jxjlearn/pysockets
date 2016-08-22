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

gminHome = '~/gmin-quilt-representation/'
localRepo = '~/test/'
remoteUrl = 'https://xjjiao@github.com/intel-otcak/test.git'
kernelType = 'cht-m1stable'



sha1 = '4200ebb7bb687dbfa1391ae6d615542fa8c741db'


#need to sync
tmp = 'mkdir'
subprocess.check_call([tmp, '~/tmp'])
#subprocess.check_call([gminHome + 'bin/akquiltsync', '-k', kernelType, sha1])

#clone the remote repo
subprocess.call(['git', 'clone', remoteUrl])

#After akquiltsync finishes, the repo is on a specific branch created by the script.
#Copy the patches to github repo.
subprocess.call(['rm', '-rf', localRepo + 'uefi/cht-m1stable/patches'])
subprocess.call(['cd', gminHome + 'uefi/cht-m1stable'])
res = subprocess.Popen(['find', 'patches'], stdout=subprocess.PIPE)
subprocess.check_call(['cpio', '-pdmuv', localRepo + 'uefi/cht-m1stable'], stdin=res.stdout)

#Update technical debt report
subprocess.call(['cd', gminHome])
subprocess.call(['./bin/akgroup', '-c', '-d', 'uefi/cht-m1stable/patches', '>', localrepo + 'uefi/cht-m1stable/TechnicalDebtSummary.csv'])
subprocess.call(['./bin/akgroup', '-cv', '-d', 'uefi/cht-m1stable/patches', '>', localrepo + 'uefi/cht-m1stable/TechnicalDebt.csv'])
