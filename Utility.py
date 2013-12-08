'''
Created on Sep 29, 2013

@author: juewang
'''
import os as _os

def getFileNameFromPath(filePath):
    return _os.path.basename(filePath)
    #name, _ = name.rsplit('.', 1)
    #return name
