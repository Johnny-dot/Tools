import subprocess
import multiprocessing
import time, os, sys
import glob, shutil

def work(cmd):
	if cmd:
		print(cmd)

def pvr(f):
	if f:
		p = subprocess.Popen(f)
		p.wait()

def etc(f):
	if f:
		p = subprocess.Popen(f)
		p.wait()

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

if __name__ == '__main__':
	if sys.argv[1] == 'pvr-start':
		if os.path.exists('pvr2.log'):
			os.remvoe('pvr2.log')
		f = open('pvr2.log', 'w')
		f.write('start time = ' + GetNowTime() + '\n')
		f.close()
	elif sys.argv[1] == 'pvr-run':
		f = open('temp-pvr.txt')
		ls = f.readlines()
		ls = map(lambda x:x.strip(), ls) # all trim
		pool = multiprocessing.Pool(multiprocessing.cpu_count()+2)
		r = pool.imap(pvr, ls)
		pool.close()
		pool.join()
	elif sys.argv[1] == 'pvr-done':
		if os.path.exists('temp-pvr.txt'):
			os.remove('temp-pvr.txt')
		if os.path.exists('temp-backsize-pvr.txt'):
			os.remove('temp-backsize-pvr.txt')
		f = open('pvr2.log', 'a')
		f.write('done time = ' + GetNowTime())
		f.close()
	elif sys.argv[1] == 'etc-start':
		if os.path.exists('etc-exclude.txt'):
			os.remove('etc-exclude.txt')
		if os.path.exists('etc2.log'):
			os.remvoe('etc2.log')
		f = open('etc2.log', 'w')
		f.write('start time = ' + GetNowTime() + '\n')
		f.close()
	elif sys.argv[1] == 'etc-run':
		f = open('temp-etc.txt')
		ls = f.readlines()
		ls = map(lambda x:x.strip(), ls) # all trim
		pool = multiprocessing.Pool(multiprocessing.cpu_count())
		r = pool.imap(etc, ls)
		pool.close()
		pool.join()
	elif sys.argv[1] == 'etc-done':
		if os.path.exists('temp-etc.txt'):
			os.remove('temp-etc.txt')
		if os.path.exists('temp-backsize-etc.txt'):
			os.remove('temp-backsize-etc.txt')
		for j in range(1, 8):
			if os.path.exists('temp-fancy-etc' + j + '.txt'):
				os.remove('temp-fancy-etc' + j + '.txt')
		f = open('etc2.log', 'a')
		f.write('done time = ' + GetNowTime())
		f.close()
	else:
		args = sys.argv[1].split(',')
		pool = multiprocessing.Pool()
		r = pool.imap(work, args)
		pool.close()
		pool.join()