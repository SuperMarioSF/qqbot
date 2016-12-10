# -*- coding: utf-8 -*-

import sys
import logging

class CodingWrappedWriter:
    def __init__(self, coding, writer):
        self.flush = getattr(writer, 'flush', lambda : None)
        self.write = \
            lambda s: writer.write(s.decode(coding).encode(writer.encoding))

def equalUtf8(coding):
    return coding is None or coding.lower() in ('utf8', 'utf-8', 'utf_8')

if equalUtf8(sys.stderr.encoding):
    utf8Stderr = sys.stderr
else:
    # utf8Stderr.write("中文") <==> 
    # sys.stderr.write("中文".decode('utf8').encode(sys.stderr.encoding))
    utf8Stderr = CodingWrappedWriter('utf8', sys.stderr)

def Utf8Logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(utf8Stderr)
        fmt = '[%(asctime)s] [%(levelname)s] %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        ch.setFormatter(logging.Formatter(fmt, datefmt))
        logger.addHandler(ch)
    return logger

logging.getLogger("").setLevel(logging.CRITICAL)

utf8Logger = Utf8Logger('Utf8Logger')

def SetLogLevel(level):
    utf8Logger.setLevel(getattr(logging, level.upper()))

_thisDict = globals()

for name in ('ERROR', 'WARN', 'INFO'):
    _thisDict[name] = getattr(utf8Logger, name.lower())

def CRITICAL(*args, **kw):
    utf8Logger.critical(*args, **kw)
    sys.exit(1)

DEBUG = lambda *args, **kw : utf8Logger.debug(exc_info=True, *args, **kw)

def RAWINPUT(msg):
    utf8Stderr.write(msg)
    utf8Stderr.flush()
    return sys.stdin.readline()