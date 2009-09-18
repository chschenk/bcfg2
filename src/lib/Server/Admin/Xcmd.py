import Bcfg2.Options
import Bcfg2.Proxy
import Bcfg2.Server.Admin

import sys
import xmlrpclib

class Xcmd(Bcfg2.Server.Admin.Mode):
    __shorthelp__ = ("XML-RPC Command Interface")
    __longhelp__ = (__shorthelp__ + "\n\nbcfg2-admin xcmd command")
    __usage__ = ("bcfg2-admin xcmd <command>")

    def __init__(self, configfile):
        Bcfg2.Server.Admin.Mode.__init__(self, configfile)

    def __call__(self, args):
        optinfo = {
            'server': Bcfg2.Options.SERVER_LOCATION,
            'user': Bcfg2.Options.CLIENT_USER,
            'password': Bcfg2.Options.SERVER_PASSWORD,
            'key': Bcfg2.Options.SERVER_KEY,
            'certificate'     : Bcfg2.Options.CLIENT_CERT,
            'ca'              : Bcfg2.Options.CLIENT_CA
            }
        setup = Bcfg2.Options.OptionParser(optinfo)
        setup.parse(sys.argv[2:])
        Bcfg2.Proxy.RetryMethod.max_retries = 1
        proxy = Bcfg2.Proxy.ComponentProxy(setup['server'],
                                           setup['user'],
                                           setup['password'],
                                           key = setup['key'],
                                           cert = setup['certificate'],
                                           ca = setup['ca'], timeout=180)
        if len(setup['args']) == 0:
            print("Usage: xcmd <xmlrpc method> <optional arguments>")
            return
        cmd = setup['args'][0]
        args = ()
        if len(setup['args']) > 1:
            args = tuple(setup['args'][1:])
        try:
            data = apply(getattr(proxy, cmd), args)
        except xmlrpclib.Fault, flt:
            if flt.faultCode == 1:
                print("Unknown method %s" % cmd)
                return
            else:
                raise
        if data != None:
            print data
