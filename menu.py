from datetime import datetime

import bpy
from bpy.props import StringProperty, CollectionProperty, BoolProperty, IntProperty

from .helpers import get_modified_date_file
from .helpers import check_local_path_file
from .settings import FileMoreRecentIn
from .mixins import FMenuMixin, FContextMixin
from .operators import UploadCurrentFile
from .operators import FolderContentOpMenu
from .operators import RefreshFolderContent
from .operators import GetCloudButton
from .operators import DownloadFileOperator


class Item(bpy.types.PropertyGroup):
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


class ItemUIList(bpy.types.UIList):
    @staticmethod
    def _must_updated(context, item):
        try:
            # For python v3.11 and later
            client_modified_datetime = datetime.fromisoformat(item.client_modified)
            server_modified_datetime = datetime.fromisoformat(item.server_modified)
        except ValueError:
            # For python before v3.11
            client_modified_datetime = datetime.fromisoformat(
                item.client_modified.replace("Z", "")
            )
            server_modified_datetime = datetime.fromisoformat(
                item.server_modified.replace("Z", "")
            )
        item_modified_at = max(client_modified_datetime, server_modified_datetime)

        addon_prefs = FContextMixin.addon_prefs(context)
        root_prefix = addon_prefs.local_filepath

        local_file_path = f"{root_prefix}{item.path_lower}"
        local_file_modified_at = get_modified_date_file(local_file_path)

        if local_file_modified_at > item_modified_at:
            return FileMoreRecentIn.LOCAL.value
        else:
            return FileMoreRecentIn.DRB.value

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        main_column = layout.column()

        file_state_column = layout.column()

        btn_column = layout.column()

        row = main_column.row(align=True)

        row_file_state = file_state_column.row()

        row_btn = btn_column.row()

        for _ in range(item.indent_level):
            row.label(icon='BLANK1')

        if item.is_folder:
            child_op = row.operator(
                FolderContentOpMenu.bl_idname,
                text="",
                emboss=False,
                icon='TRIA_DOWN' if item.is_expanded else 'TRIA_RIGHT',
            )
            child_op.item_ui_list_index = index

            refresh_op = row_btn.operator(
                RefreshFolderContent.bl_idname,
                text="",
                # emboss=False,
                icon="FILE_REFRESH",
            )
            refresh_op.item_ui_list_index = index

        else:
            addon_prefs = FContextMixin.addon_prefs(context)
            root_prefix = addon_prefs.local_filepath
            item_in_local = check_local_path_file(f"{root_prefix}{item.path_lower}")

            if item_in_local:
                version_state_icon = self._must_updated(context, item)["icon"]
            else:
                version_state_icon = FileMoreRecentIn.MISSING_LOCAL.value["icon"]

            row_file_state.label(text="", icon=version_state_icon)

            download_file_op = row_btn.operator(
                DownloadFileOperator.bl_idname,
                text="",
                icon="IMPORT"
            )
            download_file_op.file_drb_path = item.path_display

        row.label(
            text=item.name,
            icon="FILE_FOLDER" if item.is_folder else "FILE_BLANK",
        )


# Définir une classe de menu personnalisée
class MyMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Menu principal"
    bl_idname = "fblender_sync.menu"

    button_label = "" # TEST Upload

    def draw(self, context):
        layout = self.layout

        # Ajouter des éléments de menu
        layout.operator(UploadCurrentFile.bl_idname, text="Envoyer le fichier actuel")
        layout.operator(GetCloudButton.bl_idname, text="Consulter le cloud")
        if self.button_label:
            layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


class ExplorerMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Fichiers Cloud"
    bl_idname = "fblender_sync.menu.explorer"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("ItemUIList", "", scene, "custom_items", scene, "custom_items_index")
        
        col = layout.column()
        col.separator()

        for state in FileMoreRecentIn.values():
            col.label(text=state["description"], icon=state["icon"])


# Enregistrer le menu personnalisé
def register():
    bpy.utils.register_class(Item)
    bpy.utils.register_class(ItemUIList)
    bpy.utils.register_class(MyMenu)
    bpy.utils.register_class(ExplorerMenu)

    bpy.types.Scene.custom_items = CollectionProperty(type=Item)
    bpy.types.Scene.custom_items_index = IntProperty(name="Index for custom_items", default=-1)

    # if not bpy.context.scene.get("metadata", False):
    #     bpy.context.scene["metadata"] = {
    #         "scene_version": 1,
    #     }


# Supprimer le menu personnalisé
def unregister():
    bpy.utils.unregister_class(Item)
    bpy.utils.unregister_class(ItemUIList)
    bpy.utils.unregister_class(MyMenu)
    bpy.utils.unregister_class(ExplorerMenu)
    
    del bpy.types.Scene.custom_items
    del bpy.types.Scene.custom_items_index


# Exécuter l'enregistrement du menu lors de l'exécution du script
if __name__ == "__main__":
    register()
    # unregister()
