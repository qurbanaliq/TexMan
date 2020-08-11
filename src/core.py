"""This module contains abstract base class for texture
"""

import abc
import os
import importlib

class _BaseTexture(object):
    """Base class for a texture, contains methods to be implemented in
    child classes defined in dcc directory.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, node):
        """Initializer
        node -- the underlying node in a dcc application
        """
        super(_BaseTexture, self).__init__()
        self._node = node

    @abc.abstractmethod
    def setPath(self, filePath):
        """Sets the texture path to filePath
        """
        pass

    @abc.abstractmethod
    def getPath(self):
        """Returns the file path of the texture
        """
        pass

class Application(object):
    """This class represents a DCC application, such as Maya. It imports the
    relavant module from the dcc package based on which application the code
    is running in  and registers all the texture classes to be used in the GUI.
    """

    __textures = {} # registered textures

    def __init__(self):
        super(Application, self).__init__()
    
    @classmethod
    def registerTexture(cls, textureClass):
        """Register a texture class from dcc package to be used in the GUI
        textureClass -- A class type representing a texture
        """
        cls.__textures[textureClass.__name__] = textureClass
    
    def importDCCModule(self):
        """Imports the relavant dcc module from dcc package and registers it's
        textures classes
        """
        # get the dcc package path
        dccPath = os.path.join(os.path.dirname(__file__), "dcc")
        # list the dcc application modules
        modules = [os.path.splitext(m)[0] for m in os.listdir(dccPath)]
        # try to import modules in order to register the texture classes
        for mod in modules:
            try:
                _ = importlib.import_module("TexMan.src.dcc." + mod)
            except ImportError:
                continue
            # register the texture classes
            for cl in _BaseTexture.__subclasses__():
                Application.registerTexture(cl)

    def __dir__(self):
        _dir = self.__dict__.keys()
        _dir.extend(self.__class__.__dict__.keys())
        # also return the registered textures
        _dir.extend(self.__textures.keys())
        return _dir

    def __getattr__(self, name):
        return self.__textures[name]