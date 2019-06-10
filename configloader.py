# -*- coding: utf-8 -*-
try:
    from configparser import ConfigParser #python3
except:
    from ConfigParser import ConfigParser #python2
import codecs,os
BASE_CONFIG_FILE = "config/global.cfg"
SECTION_DEFAULT = "GLOBAL"
class Config():
    def put(self,section,option,value):
        if not self.conf.has_section(section):
            self.conf.add_section(section)
        self.conf.set(section,option,str(value))

    def get(self,section,option,default=None):
        if not self.conf.has_section(section):
            return default
        if not self.conf.has_option(section,option):
            return default
        return self.conf.get(section,option)

    def getint(self,section,option,default=0):
        if not self.conf.has_section(section):
            return default
        if not self.conf.has_option(section,option):
            return default
        return self.conf.getint(section,option)

    def getfloat(self,section,option,default=0.0):
        if not self.conf.has_section(section):
            return default
        if not self.conf.has_option(section,option):
            return default
        return self.conf.getfloat(section,option)

    def getboolean(self,section,option,default=False):
        if not self.conf.has_section(section):
            return default
        if not self.conf.has_option(section,option):
            return default
        return self.conf.getboolean(section,option)

    def clear(self):
        self.conf = ConfigParser()

    def load(self,filename=None):
        if filename == None:
            filename = self.filename
        else:
            self.filename = filename
        self.clear()
        with codecs.open(filename,"r","utf-8") as fp:
            self.conf.readfp(fp)

    def saveas(self,filename):
        with codecs.open(filename,"w","utf-8") as fp:
            self.conf.write(fp)

    def save(self,filename=None):
        if filename == None:
            filename = self.filename
        else:
            self.filename = filename
        dirn = os.path.dirname(filename)
        if not os.path.exists(dirn):
            os.makedirs(dirn)
        with codecs.open(filename,"w","utf-8") as fp:
            self.conf.write(fp)
    
    def __init__(self,filename):
        self.conf = ConfigParser()
        self.filename = filename
        if os.path.exists(filename):
            self.load()

# init
global_conf = Config(BASE_CONFIG_FILE)
string = None
config = None
def init_string(resfile):
    global string
    string = Config(resfile)
def init_config(resfile):
    global config
    config = Config(resfile)

if __name__ == "__main__":
    global_conf.put("GLOBAL","config","config/config.cfg")
    global_conf.put("GLOBAL","local","local/zh-cn.cfg")
    global_conf.save()
    pass