# -*- coding: utf-8 -*-
import os
import subprocess
import time

import PyV8


def needUpdate():
    if not (os.path.isfile('gfwlist.pac')):
        return True

    mtime = os.path.getmtime('gfwlist.pac')

    now = time.time()

    if (now - mtime) / 3600 / 24 > 7:
        return True

    return False


def updateGfwListPAC():
    cmd = "genpac --pac-proxy 'SOCKS5 127.0.0.1:1080' -o gfwlist.pac"
    subprocess.call(cmd, shell=True)


def isBlocked(domain):
    findProxyForURL = getFunctionFindProxyForURL()

    return 'DIRECT' != findProxyForURL(domain, domain)


# pacEngine = None


def getFunctionFindProxyForURL():
    # global pacEngine

    if needUpdate():
        updateGfwListPAC()
        # pacEngine = newPacEngine()

    # if (pacEngine is None):
    pacEngine = newPacEngine()

    return pacEngine.locals.FindProxyForURL


def newPacEngine():
    with open('gfwlist.pac', 'r') as f:
        gfwListPac = f.read()
        print 'ok'
        engine = PyV8.JSContext()
        print 'ok2'
        engine.enter()
        engine.eval(gfwListPac)
        return engine
