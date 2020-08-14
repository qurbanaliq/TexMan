"""This module contains abstract base class to represent a texture and
Application class to represent a DCC application. Support for new DCC
application can be added by adding a new module in the dcc package and support
for new texture types can be added by adding a new class in those modules.
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

    def getFolderPath(self):
        """Returns the folder path texture is loaded from
        """
        return os.path.dirname(self.getPath())

    def getFilename(self):
        """Return the filename of the texture
        """
        return os.path.basename(self.getPath())

    @abc.abstractmethod
    def getAllObjects(cls):
        """Returns all the objects of this texture type from the scene
        IMPORTANT: override this method using @classmethod
        return -- list
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
        self._module = None # module to deal with DCC application
        self._importDCCModule()
    
    @classmethod
    def _registerTexture(cls, textureClass):
        """Register a texture class from dcc package to be used in the GUI
        textureClass -- A class type representing a texture
        """
        cls.__textures[textureClass.__name__] = textureClass
    
    def getMainWindow(self):
        """Returns the main window widget to be used a parent widget
        """
        if self._module:
            return self._module.getMainWindow()
    
    def _importDCCModule(self):
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
                self._module = importlib.import_module("TexMan.src.dcc." + mod)
            except ImportError:
                continue
            else: # break the loop if the module gets imported
                break
        # register the texture classes
        for cl in _BaseTexture.__subclasses__():
            Application._registerTexture(cl)
    
    def getAllTextures(self):
        """Returns all the textures from the scene.
        return -- dict of textures {textureClassName:
                                {"folderPath": [listOfTextureObjects]}}
        """
        pathTextureMappings = {}
        for texClassName, texClass in Application.__textures.items():
            for texObj in texClass.getAllObjects():
                texFolderPath = texObj.getFolderPath()
                if texClassName not in pathTextureMappings:
                    # add the first entry for this textureClassName
                    pathTextureMappings[texClassName] = {
                        texFolderPath: [texObj]
                    }
                else:
                    if texFolderPath not in pathTextureMappings[texClassName]:
                        # add the first entry for this folder
                        pathTextureMappings[texClassName][texFolderPath] = [texObj]
                    else:
                        pathTextureMappings[texClassName][texFolderPath].append(texObj)
        return pathTextureMappings

    def __dir__(self):
        _dir = self.__dict__.keys()
        _dir.extend(self.__class__.__dict__.keys())
        # return also the registered textures
        _dir.extend(self.__textures.keys())
        return _dir

    def __getattr__(self, name):
        # add the registered textures as attrs to the application
        if name in Application.__textures:
            return self.__textures[name]
        raise AttributeError("Attribute not found")