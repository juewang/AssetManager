import contextlib as _contextlib
import os as _os
import shutil as _shutil
import sqlite3 as _sqlite3
import Utility as _Utility

_BASE_FOLDER = r"//Users//juewang//GoogleDrive//AssetManager"
_DATA_BASE_FILE = r"//Users//juewang//GoogleDrive//AssetManager//main.db"
_MAIN_TABLE = 'AssetManagerTable'
_VERSION_TABLE_EXT = '_VersionTable'
_FILE_TYPE_MAPPING = {'mb': 'Maya',
                      'ma': 'Maya',
                      'tga': 'Photoshop',
                      'psd': 'Photoshop',
                      }
_MAIN_TABLE_COLUMN = ('uid',
                      'sceneName', 
                      'filePath', 
                      'currentVersion', 
                      'description', 
                      'thumbnail', 
                      'category', 
                      'fileType',
                      )

def removeFile(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        _shutil.rmtree(getBackupDirectory(uuid))
        c.execute('DELETE FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid,))
        c.execute('DROP TABLE [' + _getVersionTable(uuid) + ']')

def removeVersion(uuid, version):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('DELETE FROM [' + _getVersionTable(uuid) + '] WHERE versionNumber = ?', (version, ))

def getCategoryList():
    with _databaseConnection(_DATA_BASE_FILE) as c:
        if not checkTableExists(c, _MAIN_TABLE):
            return ()
        c.execute('SELECT category FROM ' + _MAIN_TABLE)
        resultList = c.fetchall()
        resultSet = set()
        for result in resultList:
            resultSet.add(result[0])
        return tuple(resultSet)
    
def getAssetsUnderCategory(category):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT * FROM ' + _MAIN_TABLE + ' WHERE category=?', (category,))
        assetList = []
        for item in c.fetchall():
            assetDict = {}
            for index, columnName in enumerate(_MAIN_TABLE_COLUMN):
                assetDict[columnName] = item[index]
            assetList.append(assetDict)
        return tuple(assetList)
    
def checkTableExists(c, tableName):
    c.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table" AND name=?', (tableName,))
    result = c.fetchone()
    print result
    if result[0]:
        return True
    return False
    
def getAsset(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT * FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        assetDict = {}
        for index, columnName in enumerate(_MAIN_TABLE_COLUMN):
            assetDict[columnName] = result[index]
        return assetDict
    
def getUuid(sceneName):
    # Get uuid from scene name, if scene name does not exist, return None.
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT uid FROM ' + _MAIN_TABLE + ' WHERE sceneName = ?', (sceneName,))
        result = c.fetchone()
        if not result:
            return None
        return result[0]
    
def getSceneName(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT sceneName FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid,))
        result = c.fetchone()
        if not result:
            return None
        return result[0]
    
def getFilepath(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT filePath FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]

def getCategory(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT category FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]

def getVersions(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT * FROM [' + _getVersionTable(uuid) + ']')
        return c.fetchall()

def getDescription(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT description FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]

def getThumbnailPath(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT thumbnail FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]

def getApplicationType(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT fileType FROM ' + _MAIN_TABLE + ' WHERE uid = ?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]

def getCurrentVersion(uuid):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT currentVersion FROM ' + _MAIN_TABLE + ' WHERE uid=?', (uuid, ))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find a record with uuid {0}.'.format(uuid))
        return result[0]
        
def getSpecifiedVersion(uuid, version):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('SELECT filePath FROM [' + _getVersionTable(uuid)  + '] WHERE versionNumber = ?', (version,))
        result = c.fetchone()
        if not result:
            raise RuntimeError('Can not find version {0} in file with uuid {1}.'.format(version, uuid))
        return result[0]
    
def checkExistingFilePath(path, table, c):
    # Check if a scene with file path already exists in the database.
    c.execute('SELECT * FROM [' + table + '] WHERE filePath=?', (path,))
    if c.fetchone():
        return True
    return False

def addFile(sceneName, path, description, thumbnail, category):
    # File type is defined by ext automatically.
    # Every sceneName will have a db for storing versions and version paths and thumbnail path.
    with _databaseConnection(_DATA_BASE_FILE) as c:
        sql = 'create table if not exists ' + _MAIN_TABLE + ' ({0} INTEGER PRIMARY KEY AUTOINCREMENT, '.format(_MAIN_TABLE_COLUMN[0]) + ', '.join(_MAIN_TABLE_COLUMN[1:]) + ');'
        c.execute(sql)
        if checkExistingFilePath(path, _MAIN_TABLE, c):
            raise RuntimeError('Filepath {0} already exists.'.format(path))
        
        fileType = path.rsplit('.', 1)[-1]
        if fileType not in _FILE_TYPE_MAPPING:
            raise RuntimeError('{0} does not exist in file type mapping.'.format(fileType))
        c.execute('INSERT INTO ' + _MAIN_TABLE + ' VALUES (NULL,?,?,?,?,?,?,?);', (sceneName, path, 1, description, thumbnail, category, fileType))
        
        c.execute('SELECT uid FROM [' + _MAIN_TABLE + '] WHERE sceneName = ?', (sceneName,))
        uuid = c.fetchone()[0]
        versionTable = _getVersionTable(uuid)
        backupDir = getBackupDirectory(uuid)
        if not _os.path.exists(backupDir):
            _os.mkdir(backupDir)
        tempFilepath = _os.path.join(getBackupDirectory(uuid), '0' + _os.path.splitext(path)[-1])
        print path, tempFilepath
        _shutil.copyfile(path, tempFilepath)
        
        c.execute('create table if not exists [' + versionTable + '] (versionNumber, filePath, thumbNail)')
        c.execute('INSERT INTO [' + versionTable + '] VALUES (?,?, ?)', (1, tempFilepath, thumbnail))
        return uuid
    
def getBackupDirectory(uuid):
    return _os.path.join(_BASE_FOLDER, 'backup', str(uuid))

def setCategory(uuid, category):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE ' + _MAIN_TABLE + ' SET category = ? WHERE uid = ?', (category, uuid))

def addNewVersion(uuid, filePath, thumbnail):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        versionTable = _getVersionTable(uuid)
        c.execute('SELECT  COUNT(*) FROM [' + versionTable + ']')
        result = c.fetchone()
        if not result:
            raise RuntimeError('No version has been added to record with uuid {0}.'.format(uuid))
        currentVersion = result[0] + 1
        tempFilepath = _os.path.join(getBackupDirectory(uuid), str(currentVersion) + _os.path.splitext(filePath)[1])
        _shutil.copyfile(filePath, tempFilepath)
        c.execute('INSERT INTO [' + _getVersionTable(uuid) + '] VALUES (?,?,?)', (currentVersion, tempFilepath, thumbnail))
    setCurrentVersion(uuid, currentVersion)

def setCurrentVersion(uuid, currentVersion):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE [' + _MAIN_TABLE + '] SET currentVersion = ? WHERE uid = ?', (currentVersion, uuid))
        
def setDescription(uuid, description):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE [' + _MAIN_TABLE + '] SET description = ? WHERE uid = ?', (description, uuid))

def setThumbnailPath(uuid, thumbnailPath):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE [' + _MAIN_TABLE + '] SET thumbnail = ? WHERE uid = ?', (thumbnailPath, uuid))
        
def setSceneName(uuid, sceneName):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE [' + _MAIN_TABLE + '] SET sceneName = ? WHERE uid = ?', (sceneName, uuid))
        
def setFilepath(uuid, filePath):
    with _databaseConnection(_DATA_BASE_FILE) as c:
        c.execute('UPDATE [' + _MAIN_TABLE + '] SET filePath = ? WHERE uid = ?', (filePath, uuid))

@_contextlib.contextmanager
def _databaseConnection(dataBaseFile):
    connection = _sqlite3.connect(dataBaseFile)
    c = connection.cursor()
    try:
        yield c
        connection.commit()
    finally:
        connection.close()
    
def _getVersionTable(version):
    return str(version) + _VERSION_TABLE_EXT

    