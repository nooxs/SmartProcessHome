# -*- coding: utf8 -*

from class_profiles import profilePython

config = profilePython('/etc/config/nooxs.config')

config.set_profile('DB','db','MySQL')
config.set_profile('MySQL','host','localhost')
config.set_profile('MySQL','DB','nooxsense')
config.set_profile('MySQL','USER','root')
config.set_profile('MySQL','PASS','jfajardo1')
config.set_profile('SQLite','DB','/home/pi/nooxs/nooxsense.db')
config.set_profile('SQLite','host','localhost')
config.set_profile('procesa','miIP')

config.save_profile(False)