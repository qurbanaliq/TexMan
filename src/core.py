"""This module contains abstract base class for texture
"""

import abc

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


