# -*- coding: utf-8 -*-
import time

import PyV8

lastCheckTime = 0
pacEngine = None

def needUpdate():
    global lastCheckTime
    global pacEngine

    if (pacEngine is None):
        return True

    now = time.time()

    if (now - lastCheckTime) / 3600 / 24 < 2:
        return False

    lastCheckTime = now

    return True


def isBlocked(domain, pac_path):
    findProxyForURL = getFunctionFindProxyForURL(pac_path)

    return 'DIRECT' != findProxyForURL(domain, domain)


def getFunctionFindProxyForURL(pac_path):
    global pacEngine

    if needUpdate():
        pacEngine = newPacEngine(pac_path)

    return pacEngine.locals.FindProxyForURL


def newPacEngine(pac_path):
    with open(pac_path, 'r') as f:
        gfwListPac = f.read()
        engine = PyV8.JSContext()
        engine.enter()
        engine.eval(gfwListPac)
        return engine


if __name__ == '__main__':
    print 'www.baidu.com is blocked ? %s' % isBlocked('www.baidu.com', 'gfwlist.pac')
    print 'www.google.com is blocked ? %s' % isBlocked('www.google.com', 'gfwlist.pac')
