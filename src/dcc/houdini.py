"""This module contains code to manipulate nodes and attributes in Houdini.
Support for new texture types can be added by adding a new class by inherting
it form _BaseTexture and implementing the abstact methods.
"""

import os

import hou
from PySide2.QtWidgets import qApp

from TexMan.src.core import _BaseTexture

def getMainWindow():
    """Returns Maya main window widget
    """
    return hou.qt.mainWindow()

class PrincipledShader(_BaseTexture):
    """This class represents a texture of a principledshader in Houdini
    """

    # get principledshader node type
    _sType = hou.nodeType(hou.vopNodeTypeCategory(), "principledshader::2.0")
    # add supported texture attributes
    _attrNames = ["basecolor_texture", "ior_texture", "rough_texture"]

    def __init__(self, node, texAttr):
        """Initializer
        node -- a file node object in Maya
        texAttr -- texture attribute name
        """
        super(PrincipledShader, self).__init__()

        self._node = node
        self._texAttr = texAttr
    
    def setPath(self, filePath):
        """Sets the texture path to filePath
        """
        self._node.parm(self._texAttr).set(filePath.replace("\\", "/"))

    def getPath(self):
        """Returns the file path of the texture
        """
        return os.path.normpath(self._node.parm(self._texAttr).eval())
    
    @classmethod
    def getAllObjects(cls):
        """Returns all the objects of this texture type from the scene
        return -- list
        """

        # create of list textures objects to be returned
        return [
                cls(node, attrName) for node in cls._sType.instances()
                for attrName in cls._attrNames
                if node.parm(attrName).eval() # if it does have a texture
                ]