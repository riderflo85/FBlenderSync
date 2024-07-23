from datetime import datetime

import bpy

from .helpers import get_modified_date_file
from .helpers import check_local_path_file
from .settings import FileMoreRecentIn
from .mixins import FMenuMixin, FContextMixin
from .operators import UploadCurrentFile
from .operators import FolderContentOpMenu
from .operators import RefreshFolderContent
from .operators import NewFolderCloud
from .operators import GetCloudButton
from .operators import DownloadFileOperator
from .statics import APP_NAME


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
        item_modified_at = item_modified_at.replace(tzinfo=None)

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

            create_folder_op = row_btn.operator(
                NewFolderCloud.bl_idname,
                text="",
                icon="NEWFOLDER",
            )
            create_folder_op.item_ui_list_index = index

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

        if item.is_folder:
            icon_item = "FILE_FOLDER"
        elif item.name.split(".")[-1] == "blend":
            icon_item = "FILE_BLEND"
        else:
            icon_item = "FILE_BLANK"
        row.label(
            text=item.name,
            icon=icon_item,
        )


class MyMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Cloud"
    bl_idname = f"{APP_NAME}.menu"

    def draw(self, context):
        layout = self.layout

        layout.operator(GetCloudButton.bl_idname, text="Consulter le cloud", icon="URL")
        layout.operator(NewFolderCloud.bl_idname, text="Créer un dossier à la racine", icon="NEWFOLDER")


class ExplorerMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Fichiers Cloud"
    bl_idname = f"{APP_NAME}.menu.explorer"
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_list("ItemUIList", "", wm, "cloud_data", wm, "cloud_data_index")
        
        col = layout.column()
        col.separator()

        for state in FileMoreRecentIn.values():
            col.label(text=state["description"], icon=state["icon"])


class SaveOnCloudMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Sauvegarde sur le cloud"
    bl_idname = f"{APP_NAME}.menu.save_on_cloud"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        col = layout.column()
        col.prop(wm.save_on_cloud, "folders")
        col.separator()
        layout.operator(UploadCurrentFile.bl_idname, text="Enregistrer")


# Enregistrer le menu personnalisé
def register():
    bpy.utils.register_class(ItemUIList)
    bpy.utils.register_class(MyMenu)
    bpy.utils.register_class(ExplorerMenu)
    bpy.utils.register_class(SaveOnCloudMenu)

    # if not hasattr(bpy.types.BlendData, "metadata"):
    #     # metadata is custom property.
    #     # Access it to bpy.data.metadata
    #     # OR context.blend_data
    #     bpy.types.BlendData.metadata = {
    #         "file_version": 1
    #     }

# Supprimer le menu personnalisé
def unregister():
    bpy.utils.unregister_class(ItemUIList)
    bpy.utils.unregister_class(MyMenu)
    bpy.utils.unregister_class(ExplorerMenu)
    bpy.utils.unregister_class(SaveOnCloudMenu)
