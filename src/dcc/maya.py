"""This module contains code to manipulate nodes and attributes in Maya.
Support for new texture types can be added by adding a new class by inherting
it form _BaseTexture and implementing the abstact methods.
"""

import os

import pymel.core as pc
from PySide2.QtWidgets import qApp

from TexMan.src.core import _BaseTexture

def getMainWindow():
    """Returns Maya main window widget
    """
    for widget in qApp.topLevelWidgets():
        if widget.objectName().lower().startswith("mayawindow"):
            return widget

class FileNode(_BaseTexture):
    """This class represents a file node texture in Maya
    """
    def __init__(self, node):
        """Initializer
        node -- a file node object in Maya
        """
        super(FileNode, self).__init__()

        self._node = node
    
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
                if fileNode.ftn.get() # if it does have a texture
                ]

class AiImage(_BaseTexture):
    """This class represents a AiImage texture of Arnold in Maya.
    """
    def __init__(self, node):
        """Initilizer
        node -- an aiImage node object in Maya.
        """
        
        self._node = node
    
    def setPath(self, filePath):
        """Sets the texture path to filePath.
        """
        self._node.filename.set(filePath.replace("\\", '/'))
    
    def getPath(self):
        """Returns the file path of the texture.
        """
        return os.path.normpath(self._node.filename.get())
    
    @classmethod
    def getAllObjects(cls):
        """Returns all the objects of this texture type from the scene.
        return -- list
        """

        return [cls(node) for node in pc.ls(et=pc.nt.AiImage)
                if node.filename.get() # if it does have a texture
                ]