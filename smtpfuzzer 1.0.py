#!/usr/bin/env python
#-*- coding:utf-8 -*-
########################################################
# Name: SMTP Fuzzer
# Site: http://nimrodlevy.co.il
__author__ = 'El3ct71k'
__license__ = 'GPL v3'
__version__ = '1.0'
__email__ = 'El3ct71k@gmail.com'
########################################################

from sys import argv
from os import path
from docopt import docopt
import socket, logging


__doc__ = \
"""
SMTP Fuzzer
Usage:
    {prog} <HOST> <FILE> [-o <OUTPUT> | --output <OUTPUT>] [-v | --verbose]
    {prog} (-h | --help)
    {prog} --version

Options:
    -h --help                                   Show basic help message and exit
    --version                                   Show version.
    -v --verbose                                Verbosely level
    -o <OUTPUT> --output <OUTPUT>               Saving the output at file [default: None]
Example:
    {prog} 192.168.1.2 users.txt                Displays only users existing
    {prog} 192.168.1.2 users.txt -o file.txt    Displays only users existing and saves a log file by name file.txt
    {prog} 192.168.1.2 users.txt -v             Displays all the procedure
    {prog} 192.168.1.2 users.txt -o file.txt -v Displays all the procedure and saves a log file by name file.txt
    {prog} --version                            Display the version
""".format(prog=path.basename(argv[0]))

def createLogger(verbose=False, output=None):
    #Logging format
    logging.basicConfig(
                    format='[%(asctime)s] %(message)s',
                    datefmt='%d-%m-%Y %H:%M',
                    )
    #Create logger
    logger = logging.getLogger()
    if output:
        formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%d-%m-%Y %H:%M')
        fh = logging.FileHandler(output)
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger

def SMTPFuzzer():
    arguments = docopt(__doc__, version="SmtpFuzeer: %s" % __version__)
    #Setting the logger
    logger = createLogger(arguments['--verbose'], arguments['--output'])
    logger.info("Connecting to %s.." % arguments['<HOST>'])
    try:
        smtp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smtp.connect((arguments['<HOST>'], 25))
        logger.info("Connected successfully to %s" % arguments['<HOST>'])
        banner = smtp.recv(1024).strip('\n')
        if(banner):
            logger.info("Banner Grabbing: %s" % banner)
        try:
            if arguments['--verbose']:
                logger.debug("Fuzzing users started.")
            with open(arguments['<FILE>'], 'r') as users_file:
                for user in (l.rstrip() for l in users_file):
                    smtp.send("VRFY %s\n" % user)
                    userDetails = smtp.recv(1024).rstrip()
                    if not userDetails.startswith('550'):
                        logger.info(userDetails)
                    elif arguments['--verbose']:
                        logger.debug(userDetails)
                logger.info("Finished!")
        except IOError as msg:
            logger.info(msg)
        smtp.close()
    except socket.error as msg:
        logger.info(msg)

if __name__ == '__main__':
    SMTPFuzzer()