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
cmd = gminHome + 'bin/akquiltsync' + ' -k' + ' kernelType' + ' sha1'
subprocess.check_call(cmd, shell=True)
#subprocess.check_call([gminHome + 'bin/akquiltsync', '-k', kernelType, sha1])

#clone the remote repo
subprocess.call(['git', 'clone', remoteUrl])

#After akquiltsync finishes, the repo is on a specific branch created by the script.
#Copy the patches to github repo.
cmd = 'rm' + ' -rf ' + localRepo + 'uefi/cht-m1stable/patches'
subprocess.call(cmd, shell=True)

cmd = 'cd ' + gminHome + 'uefi/cht-m1stable'
subprocess.call(cmd, shell=True)

res = subprocess.Popen(['find', 'patches'], stdout=subprocess.PIPE)
cmd = 'cpio ' + '-pdmuv ' + localRepo + 'uefi/cht-m1stable'
subprocess.check_call(cmd, stdin=res.stdout, shell=True)

#Update technical debt report
subprocess.call('cd ' + gminHome, shell=True)
subprocess.call('./bin/akgroup ' + '-c ', '-d ' + 'uefi/cht-m1stable/patches ', '> ' + localrepo + 'uefi/cht-m1stable/TechnicalDebtSummary.csv', shell=True)
subprocess.call('./bin/akgroup ' + '-cv ' + '-di ' + 'uefi/cht-m1stable/patchesi ' + '> ' + localrepo + 'uefi/cht-m1stable/TechnicalDebt.csv', shell=True)
