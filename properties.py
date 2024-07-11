import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty


def get_dynamique_cloud_folders(self, context):
    wm = context.window_manager
    available_cloud_folders_obj = wm.available_folders
    available_cloud_folders = []
    if not available_cloud_folders_obj:
        return [
            ("-1", "", "",)
        ]
    for cloud_folder in available_cloud_folders_obj:
        available_cloud_folders.append(
            (
                cloud_folder.id,
                cloud_folder.name,
                cloud_folder.desc,
            )
        )
    return available_cloud_folders

class EnumFolderProperties(bpy.types.PropertyGroup):
    id: StringProperty(name="id cloud")
    name: StringProperty(name="folder name")
    desc: StringProperty(name="description")


class SaveOnCloudProperties(bpy.types.PropertyGroup):
    folders: EnumProperty(
        name="Dossier cible",
        description="Available folders on cloud",
        items=get_dynamique_cloud_folders,
    )


class ItemExplorerProperties(bpy.types.PropertyGroup):
    tag: StringProperty(name="Type of document (file or folder)")
    name: StringProperty(name="Item Name")
    path_lower: StringProperty(name="Dropbox path lower")
    path_display: StringProperty(name="Dropbox path display")
    id: StringProperty(name="Dropbox ID")
    client_modified: StringProperty(name="Iso datetime")
    server_modified: StringProperty(name="Iso datetime")
    size: IntProperty(name="File size in Dropbox. In Octet", default=0)
    content_hash: StringProperty(name="Content hash Dropbox")
    is_downloadable: BoolProperty(name="File is downloadable from Dropbox", default=False)
    is_expanded: BoolProperty(name="Expanded", default=False)
    is_folder: BoolProperty(name="Folder", default=False)
    children_as_requested: BoolProperty(name="If children as requested or not", default=False)
    parent_id: StringProperty(name="Folder parent")
    indent_level: IntProperty(name="Indentation", default=0)
    index: IntProperty(name="Index in collection", default=-1)
