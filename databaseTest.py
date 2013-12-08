import Database as _Database
reload(_Database)

'''mayaUuid = _Database.addFile('test', 
                         r'//Users//juewang//GoogleDrive//AssetManager//testAsset//test.mb', 
                         'my first test maya file', 
                         None, 
                         'Prop', 
                         )

psdUuid = _Database.addFile('testPSD',
                            r"//Users//juewang//GoogleDrive//AssetManager//testAsset//test.psd",
                            'my first psd file',
                            None,
                            'Environment',
                            )'''


#_Database.addNewVersion(2, r'//Users//juewang//GoogleDrive//AssetManager//backup//test//test2.mb', None)

#_Database.setCategory(1, 'Character')
'''print _Database.getCategory(2)
print _Database.getCategoryList()
print _Database.getCurrentVersion(2)
#_Database.setDescription(1, 'new description')
print _Database.getDescription(1)
#_Database.setThumbnailPath(1, "thumbnailPath")
print _Database.getThumbnailPath(1)
#_Database.setCurrentVersion(2, 1)
print _Database.getCurrentVersion(2)
print _Database.getSpecifiedVersion(2, 1)
print _Database.getApplicationType(1)
print _Database.getAssetsUnderCategory('Environment')

#_Database.removeVersion(2, 2)

#print _Database.getVersions(2)
#_Database.removeFile(2)'''

#print _Database.getAsset(4)
for verion in _Database.getVersions(14):
    print verion