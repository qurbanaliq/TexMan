"""This module contains code to manipulate nodes and attributes in Maya.
Support for new texture types can be added by adding a new class by inherting
it form _BaseTexture and implementing the abstact methods.
"""

import os

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
        self._node.ftn.set(filePath.replace("\\", "/"))

    def getPath(self):
        """Returns the file path of the texture
        """
        return os.path.normpath(self._node.ftn.get())
    
    @classmethod
    def getAllObjects(cls):
        """Returns all the objects of this texture type from the scene
        return -- list
        """
        return [cls(fileNode) for fileNode in pc.ls(et=pc.nt.File)
                if fileNode.ftn.get()]