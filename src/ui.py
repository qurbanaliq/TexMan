"""This module contains the code to create GUI for managing textures.
"""

import os
import subprocess

from PySide2.QtWidgets import QMainWindow, QTreeWidgetItem, QMenu
from PySide2.QtGui import QIcon

from TexMan.ui.ui_main_window import Ui_MainWindow
from TexMan.src.core import Application

_rootPath = os.path.dirname(os.path.dirname(__file__))
_iconPath = os.path.join(_rootPath, 'icons')

class Window(QMainWindow, Ui_MainWindow):
    """Mian window for managing textures. The window lists all the folders
    from which the textures are linked in a scene. It also lists
    all the textures file names linked in the scene.
    """

    # create the application object
    __app = Application()

    def __init__(self, parent=__app.getMainWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TexMan")

        self._folderItems = [] # tree widget items representing folders
        self._fileItems = [] # tree widget items representing file names
        self._contextMenu = None

        # override the contex menu event
        self.treeWidget.contextMenuEvent = self._showContextMenu

        # show info label if parent doesn't exist
        if parent is None:
            self._showInfoLabel("This DCC application isn't supported")
        else:
            # populate the window with available textures
            self._populate()

    def _showInfoLabel(self, message):
        """Displays an info label if no texture found or DCC not supported.
        """
        self.infoLabel.show()
        self.infoLabel.setText(message)
        self.treeWidget.hide()

    def _populate(self):
        """Populates the window with available folder paths and texture
        file names
        """

        # get all the available textures
        allTextures = self.__app.getAllTextures()

        # show info label if textures not found
        if not allTextures:
            self._showInfoLabel("No textures found in the scene")

        for texClassName in allTextures: # loop through all texture types
            texClassNameItem = QTreeWidgetItem(self.treeWidget)
            texClassNameItem.setText(0, texClassName)
            # loop through all folder paths
            for texPath in allTextures[texClassName]:
                texPathItem = QTreeWidgetItem(texClassNameItem)
                texPathItem.setText(0, texPath)
                texPathItem.setIcon(0, QIcon(os.path.join(_iconPath, 'folder.png')))
                self._folderItems.append(texPathItem)
                # loop through all the texture files in this path
                for texFile in allTextures[texClassName][texPath]:
                    texFileItem = QTreeWidgetItem(texPathItem)
                    texFileItem.setText(0, texFile.getFilename())
                    if texFile.exists():
                        texFileItem.setIcon(0, QIcon(os.path.join(_iconPath, "check.png")))
                    else:
                        texFileItem.setIcon(0, QIcon(os.path.join(_iconPath, "cross.png")))
                    self._fileItems.append(texFileItem)
            self.treeWidget.addTopLevelItem(texClassNameItem)
    
    def _selectedItems(self):
        """Returns selected tree widget items
        """
        return self.treeWidget.selectedItems()
        
    def _showContextMenu(self, event):
        """Creates and shows a context menu
        """
        if not self._contextMenu:
            self._contextMenu = QMenu(self)
            action = self._contextMenu.addAction("Browse Folder")
            action.triggered.connect(self._browseFolder)
        self._contextMenu.popup(event.globalPos())

    def _browseFolder(self):
        """Opens the folder for selected tree widget item
        """
        selectedItem = self._selectedItems()
        if selectedItem:
            folderPath = ""
            selectedItem = selectedItem[0]
            # check if the selected item is a folder path
            # tree widget item cannot checked using 'in' operator due to a bug
            # in PySide2, using 'id' function
            if id(selectedItem) in map(id, self._folderItems):
                folderPath = selectedItem.text(0)
            elif id(selectedItem) in map(id, self._fileItems):
                folderPath = selectedItem.parent().text(0)
                
            if folderPath != "":
                subprocess.Popen("explorer %s"%os.path.normpath(folderPath))
