import maya.cmds as _cmds
import Database as _Database
import os as _os
import shutil as _shutil

def openScene(uuid, version=None):
    filePath = _Database.getFilepath(uuid)
    _cmds.file(filePath, open=True)

def createReference(uuid, version=None):
    filePath = _Database.getFilepath(uuid)
    _cmds.file(filePath, reference=True, namespace=_os.path.basename(filePath))

def importScene(uuid, version=None):
    filePath = _Database.getFilepath(uuid)
    _cmds.file(filePath, i=True, namespace=_os.path.basename(filePath))

def createTextureNode(texturePath, version=None):
    textureNode = _cmds.shadingNode(asTexture=True)
    _cmds.setAttr(textureNode + '.file', texturePath)

def _makeThumbnail(xRes, yRes, imagePath):
    ## NEED TO WORK THROUGH THE RENDER SETTINGS.
    #tempImagePath = _cmds.renderSettings(firstImageName=True, fullPath=True)[0]
    #print tempImagePath
    #tempExt = _os.path.splitext(tempImagePath)[1]
    print imagePath
    _cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
    _cmds.setAttr('defaultRenderGlobals.imageFilePrefix', imagePath, type='string')
    _cmds.setAttr('defaultRenderGlobals.outFormatControl', 1)
    _cmds.setAttr('defaultResolution.width', xRes)
    _cmds.setAttr('defaultResolution.height', yRes)
    _cmds.render(_cmds.lookThru(q=True))
    #thumbNailPath = imagePath + tempExt
    #_shutil.copyfile(tempImagePath, thumbNailPath)
    #_os.remove(tempImagePath)
    #return thumbNailPath

def saveScene(sceneName, directory, description, category):
    fullScenePath = _os.path.join(directory, sceneName+'.mb')
    _cmds.file(rename=fullScenePath)
    savedFile = _cmds.file(save=True)
    version = 0
    _Database.addFile(sceneName, savedFile, description, None, category)
    uid = _Database.getUuid(sceneName)
    thumbNailImage = _os.path.join(_Database.getBackupDirectory(uid), str(version) +'.png')
    _Database.setThumbnailPath(uid, thumbNailImage)   
    _makeThumbnail(128, 128, thumbNailImage)
    
def saveSceneOnAddVersion(uid):
    version = len(_Database.getVersions(uid)) + 1
    thumbNailImage = _os.path.join(_Database.getBackupDirectory(uid), str(version) + '.png')
    savedFile = _cmds.file(save=True)
    _Database.addNewVersion(uid, savedFile, thumbNailImage)
    _makeThumbnail(128, 128, thumbNailImage)
    return thumbNailImage
    
def saveSceneOnUpdateVersion(uid, currentVersion):
    versions = _Database.getVersions(uid)
    if len(versions) < currentVersion:
        raise RuntimeError('Can not find version {0}.'.format(currentVersion))
    version = versions[currentVersion - 1]
    savedFile = _cmds.file(save=True)
    _shutil.copyfile(savedFile, version[1])
    _makeThumbnail(128, 128, version[2])
    
    