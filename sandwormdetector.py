#!/usr/bin/env python

__author__ = 'El3ct71k'
import os
import re
import zipfile
from shutil import copy, rmtree
from argparse import ArgumentParser

#Global variable
FILES = list()

def sandworm_detactor(name):
	if not os.path.exists(name):
		print("File not found")
		exit(-1)

	tmp_dir = os.environ["TMP"]
	copy(name, "exploit.zip")
	try:
		with open('exploit.zip', 'rb') as fh:
			z = zipfile.ZipFile(fh)
			for name in z.namelist():
				z.extract(name, tmp_dir)
	except zipfile.BadZipfile:
		print("Break file.")
		exit(-1)
	cur_files = '%s/ppt/embeddings/' % tmp_dir
	locations = ['%s/oleObject1.bin' % cur_files, '%s/oleObject2.bin' % cur_files]
	for loc in locations:
		if os.path.exists(loc):
			with open(loc, "rb") as ole:
				mal_file = re.search(r"(?P<host>\\\\\S{1,}[\\/]\S{1,})", str(ole.read()))
				if mal_file:
					FILES.append(mal_file.group('host').strip('\x00'))
	os.remove('exploit.zip')
	rmtree("%s/ppt" % tmp_dir)
	if FILES:
		return True
	return False

if __name__ == '__main__':
	parser = ArgumentParser(prog=os.path.basename(__file__))
	parser.add_argument("target", help="Office file to check")
	args = parser.parse_args()
	if sandworm_detactor(args.target):
		print("Sandworm vector attack detacted!\nEvil files:")
		for malware in FILES:
			print(malware)
	else:
		print("Sandworm vector not found")