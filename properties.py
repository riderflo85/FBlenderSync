import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty


EMPTY_ENUM = [("-1", "", "",)]

def sanitize_path(path: str) -> str:
    return path[1:] if path.startswith("/") else path


def get_dynamique_cloud_items(self, context):
    wm = context.window_manager
    available_items = []
    if not wm.cloud_data:
        return EMPTY_ENUM

    for cloud_data in wm.cloud_data:
        item_name = sanitize_path(cloud_data.path_display)
        available_items.append(
            (
                cloud_data.id,
                item_name,
                cloud_data.name,
            )
        )

    return available_items


def get_dynamique_cloud_folders(self, context):
    wm = context.window_manager
    available_cloud_folders = []
    if not wm.cloud_data:
        return EMPTY_ENUM

    for cloud_data in wm.cloud_data:
        if not cloud_data.is_folder:
            continue
        folder_name = sanitize_path(cloud_data.path_display)
        available_cloud_folders.append(
            (
                cloud_data.id,
                folder_name,
                cloud_data.path_lower,
            )
        )

    return available_cloud_folders


class SaveOnCloudProperties(bpy.types.PropertyGroup):
    folders: EnumProperty(
        name="Dossier cible",
        description="Available folders on cloud",
        items=get_dynamique_cloud_folders,
    )


class RemoveCloudItemProperties(bpy.types.PropertyGroup):
    item: EnumProperty(
        name="Item",
        description="Item à supprimer",
        items=get_dynamique_cloud_items
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


class StorageCloudProperties(bpy.types.PropertyGroup):
    used: FloatProperty(name="Space used", precision=2)
    allocated: FloatProperty(name="Space Left", precision=2)
    factor: FloatProperty(name="Factor for progress bar", precision=2)
    unit_u: StringProperty(name="Unit used", default="Octet")
    unit_a: StringProperty(name="Unit allocated", default="Octet")
