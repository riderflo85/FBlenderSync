import time

import bpy
from bpy.props import StringProperty

from ..mixins import FDropBoxMixin


class GetCloudButton(FDropBoxMixin, bpy.types.Operator):
    bl_idname = "fblender_sync.get_cloud"
    bl_label = "Get the content first root Dropbox"
    
    root_drb_path: StringProperty(name="Root path to DropBox cloud", default="")

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.get_cloud(context, self.root_drb_path)
        bpy.context.window.cursor_set("DEFAULT")
        if len(context.scene.custom_items) > 0:
            context.scene.custom_items.clear()
        self.add_ui_list_with_dropbox_data(res, context)
        return {'FINISHED'}


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
    bpy.utils.register_class(UploadCurrentFile)
    bpy.utils.register_class(GetCloudButton)

def unregister():
    bpy.utils.unregister_class(UploadCurrentFile)
    bpy.utils.unregister_class(GetCloudButton)

