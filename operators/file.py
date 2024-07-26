import bpy
from bpy.props import StringProperty

from ..mixins import FDropBoxMixin
from ..helpers import write_file, check_or_create_local_root_path
from ..statics import APP_NAME
from ..settings import DownloadMode


class GetCloudButton(FDropBoxMixin, bpy.types.Operator):
    bl_idname = f"{APP_NAME}.get_cloud"
    bl_label = "Get the content first root Dropbox"
    
    root_drb_path: StringProperty(name="Root path to DropBox cloud", default="")

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.cloud_action(context, "get_content_folder", path=self.root_drb_path)
        b_allocated, b_used = self.cloud_action(context, "get_storage_infos")
        self.set_storage_infos(context, b_allocated, b_used)
        bpy.context.window.cursor_set("DEFAULT")
        wm = context.window_manager
        if len(wm.cloud_data) > 0:
            wm.cloud_data.clear()
        self.add_ui_list_with_dropbox_data(res, context)
        return {'FINISHED'}


class DownloadFileOperator(FDropBoxMixin, bpy.types.Operator):
    bl_idname = f"{APP_NAME}.download_file"
    bl_label = "Download this Dropbox file"

    file_drb_path: StringProperty(name="File path to DropBox cloud", default="")
    file_name: StringProperty(name="File name", default="")
    dl_mode: DownloadMode

    @classmethod
    def poll(cls, context):
        return len(context.window_manager.cloud_data) > 0

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        file_infos, file_bytes = self.cloud_action(context, "download_file", path=self.file_drb_path)
        path_sync_folder = self.addon_prefs(context).local_filepath
        file_path_name = f"{path_sync_folder}{self.file_drb_path}"
        file_path_name = file_path_name.replace("//", "/")
        bpy.context.window.cursor_set("DEFAULT")
        root_path_file = file_path_name.replace(file_infos.get("name"), "")
        check_or_create_local_root_path(root_path_file)
        file_is_writed = write_file(file_path_name, file_bytes)
        if file_is_writed:
            self.report({"INFO"}, "Successfuly writed file !")
            if self.dl_mode == DownloadMode.STORE_OPEN:
                bpy.ops.wm.open_mainfile(filepath=file_path_name)
        else:
            self.report({"ERROR"}, "Error with wirted file !")
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        addon_prefs = FDropBoxMixin.addon_prefs(context)
        if self.file_name.endswith(".blend"):
            self.dl_mode = getattr(DownloadMode, addon_prefs.download_mode)
        else:
            self.dl_mode = DownloadMode.STORE
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="L'action `%s` vas être exécutée" % self.dl_mode.value.get("desc"))


class UploadCurrentFile(FDropBoxMixin, bpy.types.Operator):
    """Upload the current file into DropBox"""
    bl_idname = f"{APP_NAME}.upload_current_file"
    bl_label = "Export Some Data"

    cloud_folder_object: None
    local_pathfile: str = ""

    def _get_cloud_folder_obj(self, cloud_collection, folder_id):
        for item in cloud_collection.values():
            if folder_id == item.id:
                self.cloud_folder_object = item
                break
        return self.cloud_folder_object

    @classmethod
    def poll(cls, context):
        return (
            context.window_manager.save_on_cloud is not None
            and context.window_manager.save_on_cloud.folders != "-1"
            and bpy.data.is_saved
        )

    def execute(self, context):
        wm = context.window_manager
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        filename = self.local_pathfile.split("/")[-1]
        file_already_on_cloud = True if not wm.cloud_data.find(filename) == -1 else False
        mode = "overwrite" if file_already_on_cloud else "add"
        res = self.cloud_action(
            context,
            "upload_file",
            path_file=self.cloud_folder_object.path_lower,
            dropbox_path_folder=self.local_pathfile,
            mode=mode,
        )
        if res == "done":
            self.report({'INFO'}, "Fichier %s, envoyé avec succès !" % filename)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        self.local_pathfile = bpy.data.filepath
        layout = self.layout

        wm = context.window_manager
        cloud_folder_selected_id = wm.save_on_cloud.folders
        cloud_folder_selected = self._get_cloud_folder_obj(wm.cloud_data, cloud_folder_selected_id)

        layout.label(
            text="Attention l'envoi de fichier peut prendre",
            icon="ERROR",
        )
        layout.label(text="du temps et bloquer Blender !")
        layout.label(text="Merci de patienter !")
        layout.separator()
        col = layout.column()
        message_title = (
            "Enregistrer le fichier actuel %s"
            % self.local_pathfile.split("/")[-1]
        )
        message_subtitle = (
            "sur votre cloud dans le dossier %s"
            % cloud_folder_selected.name
        )
        col.label(text=message_title)
        col.label(text=message_subtitle)


def register():
    bpy.utils.register_class(DownloadFileOperator)
    bpy.utils.register_class(UploadCurrentFile)
    bpy.utils.register_class(GetCloudButton)

def unregister():
    bpy.utils.unregister_class(DownloadFileOperator)
    bpy.utils.unregister_class(UploadCurrentFile)
    bpy.utils.unregister_class(GetCloudButton)

