SMTPFuzzer
==================
The SMTP Fuzzer will connect to a given mail server and use a wordlist to enumerate users that are present on the remote system. 

#####Examples:

* Fuzzing 127.0.0.1 with `users.txt` file:

`smtpfuzzer.py 127.0.0.1 users.txt`

* Fuzzing 127.0.0.1 with `users.txt` file verbosely:

`smtpfuzzer.py 127.0.0.1 users.txt -v`

* Fuzzing 127.0.0.1 with `users.txt` file verbosely with 100 threads:

`smtpfuzzer.py 127.0.0.1 users.txt -v -t 100`


Requirements:
===============
###Linux Installation:
1. sudo apt-get install python-dev python-pip
2. sudo pip install -r requirements.txt
3. easy_install prettytable

###MacOSx Installation:
1. Install Xcode Command Line Tools (AppStore)
2. sudo easy_install pip, prettytable
3. sudo pip install -r requirements.txt

###Windows Installation:
1. Install [gevent](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gevent)
2. Open Command Prompt(cmd) as Administrator -> Goto python folder -> Scripts (cd c:\Python27\Scripts)
3. pip install -r (Full Path To requirements.txt)
4. easy_install prettytable