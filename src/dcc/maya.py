"""This module contains code to manipulate nodes and attributes in Maya
"""

import pymel.core as pc
from TexMan.src.core import _BaseTexture

class FileNode(_BaseTexture):
    """This class represents a file node texture in Maya
    """
    def __init__(self, node):
        """Initializer
        node -- a file node object in Maya
        """
        super(FileNode, self).__init__(node)
    
    def setPath(self, filePath):
        """Sets the texture path to filePath
        """
        self._node.ftn.set(filePath)

    def getPath(self):
        """Returns the file path of the texture
        """
        self._node.ftn.get()

# add support for new texture types here