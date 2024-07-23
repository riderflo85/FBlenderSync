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
from .helper import HelpOperator
from .helper import register as helper_register
from .helper import unregister as helper_unregister


def register():
    helper_register()
    file_register()
    folder_register()

def unregister():
    helper_unregister()
    file_unregister()
    folder_unregister()
