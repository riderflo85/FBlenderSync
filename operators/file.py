import time

import bpy
from bpy.props import StringProperty

from ..mixins import FDropBoxMixin
from ..helpers import write_file, check_or_create_local_root_path


class GetCloudButton(FDropBoxMixin, bpy.types.Operator):
    bl_idname = "fblender_sync.get_cloud"
    bl_label = "Get the content first root Dropbox"
    
    root_drb_path: StringProperty(name="Root path to DropBox cloud", default="")

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.get_cloud(context, self.root_drb_path)
        bpy.context.window.cursor_set("DEFAULT")
        wm = context.window_manager
        if len(wm.cloud_data) > 0:
            wm.cloud_data.clear()
            wm.available_folders.clear()
        self.add_ui_list_with_dropbox_data(res, context)
        return {'FINISHED'}


class DownloadFileOperator(FDropBoxMixin, bpy.types.Operator):
    bl_idname = "fblender_sync.download_file"
    bl_label = "Download this Dropbox file"

    file_drb_path: StringProperty(name="File path to DropBox cloud", default="")

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        file_infos, file_bytes = self.dl_file(context, self.file_drb_path)
        path_sync_folder = self.addon_prefs(context).local_filepath
        file_path_name = f"{path_sync_folder}{self.file_drb_path}"
        file_path_name = file_path_name.replace("//", "/")
        bpy.context.window.cursor_set("DEFAULT")
        root_path_file = file_path_name.replace(file_infos.get("name"), "")
        check_or_create_local_root_path(root_path_file)
        file_is_writed = write_file(file_path_name, file_bytes)
        if file_is_writed:
            self.report({"INFO"}, "Successfuly writed file !")
        else:
            self.report({"ERROR"}, "Error with wirted file !")
        return {"FINISHED"}


class UploadCurrentFile(bpy.types.Operator):
    """Upload the current file into DropBox"""
    bl_idname = "fblender_sync.upload_current_file"
    bl_label = "Export Some Data TEST"

    filepath: StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        self.report({'INFO'}, "TEST LOG 1 path file %s" % self.filepath)
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        time.sleep(2) # Simulate the request api timer
        return {'FINISHED'}

    def invoke(self, context, event):
        self.report({'INFO'}, "TEST LOG 2")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(DownloadFileOperator)
    bpy.utils.register_class(UploadCurrentFile)
    bpy.utils.register_class(GetCloudButton)

def unregister():
    bpy.utils.unregister_class(DownloadFileOperator)
    bpy.utils.unregister_class(UploadCurrentFile)
    bpy.utils.unregister_class(GetCloudButton)

