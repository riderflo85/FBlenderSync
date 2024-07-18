from .file import GetCloudButton
from .file import UploadCurrentFile
from .file import DownloadFileOperator
from .file import register as file_register
from .file import unregister as file_unregister
from .folder import RefreshFolderContent
from .folder import FolderContentOpMenu
from .folder import NewFolderCloud
from .folder import register as folder_register
from .folder import unregister as folder_unregister


def register():
    file_register()
    folder_register()

def unregister():
    file_unregister()
    folder_unregister()
