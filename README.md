# TexMan
TexMan is a tool for managing textures in DCC applications such as Maya, Houdini, etc. It is designed to support any DCC application and any texture type, such as Maya's File node, Arnold's AiImage node, etc. Adding support for a new DCC application is as simple as adding a new Python module in the *dcc* package. Similarly, adding support for a new texture type is as simple as adding a new Python class in the corresponding module in the *dcc* package.
## Features
Here are all the features that are currently offered by this tool and the ones which will be offered in the future.
### Supported
- List all texture folders from which the textures are linked in the scene.
- List all the texture file names linked from the listed folders.
- Support for Houdini textures.
- Support for Maya textures.
- Highlight missing textures (the ones that doesn't exist in the file system).
- Browse texture folder (right-click on folder path or texture to browse).
- Copy selected folder path(s) and texture name(s) to the clipboard.
### To be supported
- Replace folder path to link the same textures from a new folder.
- Remove textures from the scene (optionally from file system).
- Export All or Selected textures to a folder.
