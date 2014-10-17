#!/usr/bin/env python
#-*- coding:utf-8 -*-
########################################################
# Name: SMTP Fuzzer
# Site: http://nimrodlevy.co.il
__author__ = 'El3ct71k'
__license__ = 'GPL v3'
__version__ = '2.0'
__email__ = 'El3ct71k@gmail.com'
########################################################

from argparse import ArgumentParser
from gevent.monkey import patch_all
patch_all(socket=False)
from gevent.pool import Pool
from functools import partial
import os
import sys
import socket
import smtplib
import logging


#Setting the logger
LOGGER = logging.getLogger('SMTPFuzzer')


def configure_logger(verbose=False):
    """
        This function is responsible to configure logging object.
    """
    # Check if logger exist
    if ('LOGGER' not in globals()) or (not LOGGER):
        raise Exception('Logger does not exists, Nothing to configure...')

    # Set logging level
    LOGGER.setLevel(logging.DEBUG) if verbose else LOGGER.setLevel(logging.INFO)

    # Create console handler
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(message)s',
        datefmt='%d-%m-%Y %H:%M'
    )
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)

def get_users(users_file):
    """
		This function is responsible to parsing the users file
	"""
    if not os.path.exists(users_file):
        LOGGER.info("Users file not found")
        return
    with open(users_file) as users:
        for f in users:
            yield f.strip()

def vrfy_command(s, user):
    """
		This function is responsible to check if the user exist in the SMTP server
		if it exist, print the details
		if is not exist and the verbose flag is in false position, continue
	"""
    vrfy = s.vrfy(user)
    if str(vrfy[0]).startswith('25'):
        LOGGER.info(vrfy[1])
    else:
        LOGGER.debug(vrfy[1])

def main(target, users_file, pool_size=50, verbose=False):
    # Configure Logger
    configure_logger(verbose)
    p = Pool(size=pool_size)
    LOGGER.info("Trying to connect to %s" % target)
    try:
        s = smtplib.SMTP(target)
        LOGGER.info("Connected successfully!")
        vrfy = partial(vrfy_command, s)
        res = [res for res in p.imap_unordered(vrfy, get_users(users_file))]
		if res:
			LOGGER.info("Done!")

    except socket.error:
        LOGGER.info("Connection failed!")
if __name__ == '__main__':
    parser = ArgumentParser(prog=os.path.basename(__file__))
    parser.add_argument("target", help="Host to scan")
    parser.add_argument("users_file", help="Users list file")
    parser.add_argument("-t", "--pool_size", help="Max threads for scan", type=int, default=50)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    sys_args = vars(parser.parse_args())
    main(**sys_args)