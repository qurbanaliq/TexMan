"""This module contains the code to create GUI for managing textures.
"""

from PySide2.QtWidgets import QMainWindow, QTreeWidgetItem
from PySide2.QtGui import QApplication

from TexMan.ui.ui_main_window import Ui_MainWindow
from TexMan.src.core import Application

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

        self._populate()

    def _populate(self):
        """Populates the window with available folder paths and texture
        file names
        """
        allTextures = self.__app.getAllTextures()
        for texClassName in allTextures: # loop through all texture types
            texClassNameItem = QTreeWidgetItem(self.treeWidget)
            texClassNameItem.setText(0, texClassName)
            # loop through all folder paths
            for texPath in allTextures[texClassName]:
                texPathItem = QTreeWidgetItem(texClassNameItem)
                texPathItem.setText(0, texPath)
                # loop through all the texture files in this path
                for texFile in allTextures[texClassName][texPath]:
                    texFileItem = QTreeWidgetItem(texPathItem)
                    texFileItem.setText(0, texFile.getFilename())
            self.treeWidget.addTopLevelItem(texClassNameItem)