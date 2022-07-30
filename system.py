import os
class booter:
    def shutdown(self): os.system("sudo halt")
    def reboot(self): os.system("sudo reboot")
boot=booter()

sudo="sudo "
currectUser=""
class Run:
    def python(self,file,mode=sudo):
        os.system(mode+"python "+file)
    def bash(self,file,mode=sudo):
        os.system(mode+"bash "+file)
run=Run()

def addWIFIoption(SSID,passwd):
    #NOTE:This options requires ROOT.
    with open("/etc/wpa_supplicant.conf","r") as f:
        data=f.read()
        p=len([0 for i in range(len(data)-7) if data[i:i+7]=="network"])
    with open("/etc/wpa_supplicant.conf","a") as f:
        f.write(f'''\nnetwork={{\n  ssid="{SSID}"\n    scan_ssid=1\n  psk="{passwd}"\n priority={p}\n}}      \n''')

from hashlib import *
def hash(data:bytes):
    def fiveHash(d:bytes):
        def shas(func,data_):return func(data_).digest()
        for i in range(5):
            d=md5(shas(sha1,shas(sha224,shas(sha256,shas(sha512,d))))).digest()
        return d
    fd=fiveHash(data)
    return fd,fiveHash(fd)
