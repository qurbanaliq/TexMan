"""This module contains the code to create GUI for managing textures.
"""

import os

from PySide2.QtWidgets import QMainWindow, QTreeWidgetItem
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
                # loop through all the texture files in this path
                for texFile in allTextures[texClassName][texPath]:
                    texFileItem = QTreeWidgetItem(texPathItem)
                    texFileItem.setText(0, texFile.getFilename())
                    if texFile.exists():
                        texFileItem.setIcon(0, QIcon(os.path.join(_iconPath, "check.png")))
                    else:
                        texFileItem.setIcon(0, QIcon(os.path.join(_iconPath, "cross.png")))
            self.treeWidget.addTopLevelItem(texClassNameItem)