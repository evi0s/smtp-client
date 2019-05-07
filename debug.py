"""Debug"""
import os


DEBUG = True if 'DEBUG' in os.environ else False


def debug(message):
    if DEBUG:
        print("\033[0;33;40m[Debug]\033[0m: %s" % message)


def error(message):
    print("\033[0;31;40m[Error]\033[0m: %s" % message)
