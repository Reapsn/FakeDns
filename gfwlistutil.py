# -*- coding: utf-8 -*-
import os
import subprocess
import time

import PyV8

lastCheckTime = 0

def needUpdate():

    global lastCheckTime

    now = time.time()

    if (now - lastCheckTime) / 3600 / 24 < 1:
        return False

    if not (os.path.isfile('gfwlist.pac')):
        return True

    mtime = os.path.getmtime('gfwlist.pac')

    lastCheckTime = now

    if (now - mtime) / 3600 / 24 > 7:
        return True

    return False


def updateGfwListPAC():
    cmd = 'genpac --pac-proxy "SOCKS5 127.0.0.1:1080" -o gfwlist.pac'
    subprocess.call(cmd, shell=True)


def isBlocked(domain):
    findProxyForURL = getFunctionFindProxyForURL()

    return 'DIRECT' != findProxyForURL(domain, domain)


pacEngine = None

def getFunctionFindProxyForURL():
    global pacEngine

    if needUpdate():
        updateGfwListPAC()
        pacEngine = newPacEngine()

    if (pacEngine is None):
        pacEngine = newPacEngine()

    return pacEngine.locals.FindProxyForURL


def newPacEngine():
    with open('gfwlist.pac', 'r') as f:
        gfwListPac = f.read()
        engine = PyV8.JSContext()
        engine.enter()
        engine.eval(gfwListPac)
        return engine

if __name__ == '__main__':

    print 'www.baidu.com is blocked ? %s' % isBlocked('www.baidu.com')
    print 'www.google.com is blocked ? %s' % isBlocked('www.google.com')