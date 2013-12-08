
#import Database as _Database
#import MayaFunction as _MayaFunction
import PyQt4.QtGui as _QtGui
import functools as _functools

class AssetManagerWindow(object):
    def __init__(self):
        self._dialog = _QtGui.QDialog()
        self._dialog.setWindowTitle('Asset Manager')
        self._dialog.show()
        
a = AssetManagerWindow()

'''class AssetManagerWindow(object):
    _window = None
    def __init__(self):
        self._uiWidget = {}
        self._currentSelectedAsset = None
        self._newAssetWindow = None
        self._currentSelectedBackground = [0.5, 0.5, 0.5]
        # Set the default background color for now.
        self._defaultBackground = [0.25, 0.25, 0.25]
        self._createAssetManagerWindow()

    def _createAssetManagerWindow(self):
        if self._window and _cmds.dockControl(self._window, exists=True):
            _cmds.deleteUI(self._window, control=True)
            
        window = _cmds.window(title='Asset Manager')
        _cmds.columnLayout()
        self._window = _cmds.dockControl(content=window, area='right', allowedArea=('right', 'left'), label='Asset Manager')
        tabLayout = _cmds.tabLayout()
        for category in _Database.getCategoryList():
            self._uiWidget[category] = self._addCategoryTab(category, tabLayout)
        _cmds.setParent('..')
    
        self._uiWidget['sceneNameTextField'] = _cmds.textFieldGrp(label='Scene Name: ', width=300, columnAlign2=['left', 'left'], columnWidth2=[100, 195])
        self._uiWidget['filePathTextField'] = _cmds.textFieldGrp(label='File Path: ', width=300, columnAlign2=['left', 'left'], columnWidth2=[100, 195])
        self._uiWidget['versionNumberField'] = _cmds.intSliderGrp(label='Current Version:', width=300, field=True, columnAlign3=['left', 'left', 'left'], columnAttach3=['left', 'left', 'left'], columnWidth3=[100, 50, 145])
        _cmds.text(label='Description: ')
        self._uiWidget['descriptionTextField'] = _cmds.scrollField(width=300, height=50)
       
        _cmds.separator(style='single', horizontal=True)
        _cmds.gridLayout(numberOfColumns=2, cellWidth=150)
        self._uiWidget['addAssetButton'] = _cmds.button(label='Add New Asset', command=self._addNewAsset)
        self._uiWidget['deleteAssetButton'] = _cmds.button(label='Delete Current Asset', command=self._deleteAsset)
        self._uiWidget['addVersionButton'] = _cmds.button(label='Add Version', command=self._addVersion)
        self._uiWidget['updateAssetButton'] = _cmds.button(label='Update Current Version', command = self._updateCurrentVersion)
        self._uiWidget['viewVersionButton'] = _cmds.button(label='View Version List', command = self._viewVersionList)
        self._uiWidget['updateAssetInfoButton'] = _cmds.button(label='Update Asset Info', command = self.updateAssetInfo)
        self._uiWidget['editCategory'] = _cmds.button(label='Edit category')
        _cmds.setParent('..')
        
    def _addCategoryTab(self, category, tabLayout):
        iconSize = 85
        childLayout = _cmds.scrollLayout(width=300, height=200, childResizable=True)
        gridLayout = _cmds.gridLayout(numberOfColumns=3, cellHeight = iconSize, cellWidth=iconSize)
        for asset in _Database.getAssetsUnderCategory(category):
            self._addAssetButton(asset, iconSize)
        _cmds.tabLayout(tabLayout, tabLabel=((childLayout, category),), edit=True)
        _cmds.setParent('..')
        _cmds.setParent('..')
        return gridLayout
        
    def _addAssetButton(self, asset, iconSize):
        icon = asset.get('thumbnail')
        if not icon:
            icon = 'cube.png'
        button = _cmds.iconTextButton(style='iconAndTextVertical', image1=icon, height=iconSize, width=iconSize, label=asset['sceneName'])
        _cmds.iconTextButton(button, edit=True, command=_functools.partial(self._assetSelected, asset))
        self._uiWidget[self._assetButtonKey(asset['uid'])] = button
        if not self._defaultBackground:
            self._defaultBackground = _cmds.iconTextButton(button, query=True, backgroundColor=True)
        _cmds.popupMenu()
        self._uiWidget[self._assetButtonMenuOpenKey(asset['uid'])] = _cmds.menuItem(label='Open')
        self._uiWidget[self._assetButtonMenuImportKey(asset['uid'])] = _cmds.menuItem(label='Import')
        self._uiWidget[self._assetButtonMenuReferenceKey(asset['uid'])] = _cmds.menuItem(label='Reference')
        
    def _assetSelected(self, assetInfo):
        if self._currentSelectedAsset != None:
            _cmds.iconTextButton(self._uiWidget[self._assetButtonKey(self._currentSelectedAsset)], edit=True, backgroundColor=self._defaultBackground)
        _cmds.textFieldGrp(self._uiWidget['sceneNameTextField'], edit=True, text=assetInfo['sceneName'])
        _cmds.textFieldGrp(self._uiWidget['filePathTextField'], edit=True, text=assetInfo['filePath'])
        _cmds.scrollField(self._uiWidget['descriptionTextField'], edit=True, text=assetInfo['description'])
        versionList = _Database.getVersions(assetInfo['uid'])
        _cmds.intSliderGrp(self._uiWidget['versionNumberField'], edit=True, minValue=1, maxValue=len(versionList), value=int(assetInfo['currentVersion']))
        _cmds.iconTextButton(self._uiWidget[self._assetButtonKey(assetInfo['uid'])], edit=True, backgroundColor=self._currentSelectedBackground)
        self._currentSelectedAsset = assetInfo['uid']
        
    def _addNewAsset(self, args):
        # This brings up a new window for type in new asset name.
        if self._newAssetWindow and _cmds.window(self._newAssetWindow, exists=True):
            _cmds.deleteUI(self._newAssetWindow)
        self._newAssetWindow = _cmds.window(title='Enter New Asset Info')
        _cmds.columnLayout()
        sceneNameText = _cmds.textFieldGrp(label='Scene Name: ', columnAlign2=('left', 'left'), columnWidth2=(80, 185))
        _cmds.rowLayout(numberOfColumns=2)
        directoryText = _cmds.textFieldGrp(label='Directory: ', columnAlign2 = ('left', 'left'), columnWidth2=(80, 185))
        _cmds.button(label='...', width=20, command=_functools.partial(self._directorySelection, directoryText))
        _cmds.setParent('..')
        categoryMenu = _cmds.optionMenu(label='Category:   ')
        for category in _Database.getCategoryList():
            _cmds.menuItem(label=category)
        _cmds.text(label='Description: ')
        descriptionText = _cmds.scrollField(width = 300, height=100)
        _cmds.rowLayout(numberOfColumns=2)
        _cmds.button(label='OK', width=150, align='left', command=_functools.partial(self._newAssetInfoConfirmed, (sceneNameText, directoryText, descriptionText, categoryMenu)))
        _cmds.button(label='Cancel', width=150, align='left', command=self._newAssetInfoClose)
        _cmds.showWindow(self._newAssetWindow)
        
    def _directorySelection(self, directoryText, args):
        directory = _cmds.fileDialog2(fileMode=3)
        _cmds.textFieldGrp(directoryText, edit=True, text=str(directory[0]))
        
    def _newAssetInfoConfirmed(self, textWidgetList, args):
        sceneName = _cmds.textFieldGrp(textWidgetList[0], query=True, text=True)
        directory = _cmds.textFieldGrp(textWidgetList[1], query=True, text=True)
        description = _cmds.scrollField(textWidgetList[2], query=True, text=True)
        category = _cmds.optionMenu(textWidgetList[3], value=True, query=True)
        if not sceneName or not directory or not description:
            _cmds.confirmDialog(title='Invalid Asset Info', message='Asset info for "Scene Name", "Directory" and "Description" can not be empty.', button='OK')
            return
        self._newAssetInfoClose()
        _MayaFunction.saveScene(sceneName, directory, description, category)
        self._updateAssetList(category, _Database.getAsset(_Database.getUuid(sceneName)))
        
    def _newAssetInfoClose(self, *arg):
        _cmds.deleteUI(self._newAssetWindow)
        
    def _updateAssetList(self, category, asset):
        _cmds.setParent(self._uiWidget[category])
        self._addAssetButton(asset, 85)
        
    def _deleteAsset(self, *args):
        if not self._currentSelectedAsset:
            return
        print self._currentSelectedAsset
        _Database.removeFile(self._currentSelectedAsset)
        _cmds.deleteUI(self._uiWidget.pop(self._assetButtonMenuOpenKey(self._currentSelectedAsset)))
        _cmds.deleteUI(self._uiWidget.pop(self._assetButtonMenuImportKey(self._currentSelectedAsset)))
        _cmds.deleteUI(self._uiWidget.pop(self._assetButtonMenuReferenceKey(self._currentSelectedAsset)))
        _cmds.deleteUI(self._uiWidget.pop(self._assetButtonKey(self._currentSelectedAsset)))
        self._currentSelectedAsset = None
        
    def _addVersion(self, *args):
        if not self._currentSelectedAsset:
            return
        _MayaFunction.saveSceneOnAddVersion(self._currentSelectedAsset)
        versionList = _Database.getVersions(self._currentSelectedAsset)
        currentVersion = _Database.getCurrentVersion(self._currentSelectedAsset)
        _cmds.intSliderGrp(self._uiWidget['versionNumberField'], edit=True, minValue=1, maxValue=len(versionList), value=int(currentVersion))
        
    def _updateCurrentVersion(self, *args):
        if not self._currentSelectedAsset:
            return
        currentVersion = _cmds.intSliderGrp(self._uiWidget['versionNumberField'], query=True, value=True)
        _MayaFunction.saveSceneOnUpdateVersion(self._currentSelectedAsset, currentVersion)
        
    def updateAssetInfo(self, *args):
        if not self._currentSelectedAsset:
            return
        newSceneName = _cmds.textFieldGrp(self._uiWidget['sceneNameTextField'], query=True, text=True)
        newDescription = _cmds.scrollField(self._uiWidget['descriptionTextField'], query=True, text=True)
        newFilepath = _cmds.textFieldGrp(self._uiWidget['filePathTextField'], query=True, text=True)
        _Database.setSceneName(self._currentSelectedAsset, newSceneName)
        _Database.setFilepath(self._currentSelectedAsset, newFilepath)
        _Database.setDescription(self._currentSelectedAsset, newDescription)
        
    def _viewVersionList(self, *args):
        if not self._currentSelectedAsset:
            return
       
    def _assetButtonKey(self, uid):
        return 'assetButton' + str(uid)
    
    def _assetButtonMenuOpenKey(self, uid):
        return 'assetButton' + str(uid) + '_open'
    
    def _assetButtonMenuImportKey(self, uid):
        return 'assetButton' + str(uid) + '_import'

    def _assetButtonMenuReferenceKey(self, uid):
        return 'assetButton' + str(uid) + '_reference'
        '''
    
    
    

