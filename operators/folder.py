from datetime import datetime

import bpy
from bpy.props import IntProperty

from ..mixins import FDropBoxMixin
from ..history import MenuOperatorHistory, OperatorHistoryType


class RefreshFolderContent(FDropBoxMixin, bpy.types.Operator):
    """Refresh the folder content with Dropbox API request response"""
    bl_idname = "fblender_sync.refresh_folder_content"
    bl_label = "Refresh folder content"

    item_ui_list_index: IntProperty(name="Index of folder")

    def execute(self, context):
        wm = context.window_manager
        folder = wm.cloud_data[self.item_ui_list_index]

        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.get_cloud(context, folder.path_lower)
        bpy.context.window.cursor_set("DEFAULT")

        if folder.is_expanded:
            childrens = self.get_childs(folder, self.item_ui_list_index, wm.cloud_data)
            history_op = MenuOperatorHistory(
                type=OperatorHistoryType.REFRESH,
                item_id=folder.id,
                item_index=self.item_ui_list_index,
                childs=childrens,
                collection=wm.cloud_data,
                timestamp=datetime.now(),
            )
            history_op.exec_callback()

        new_items = self.add_ui_list_with_dropbox_data(res, context)
        self.move_ui_items(
            moving_items=new_items,
            insert_in=self.item_ui_list_index+1,
            items=wm.cloud_data,
            parent=folder,
        )
        folder.children_as_requested = True
        folder.is_expanded = True
        return {'FINISHED'}


class FolderContentOpMenu(FDropBoxMixin, bpy.types.Operator):
    """Request the Dropbox cloud to get the content of folder"""
    bl_idname = "fblender_sync.folder_content_op_menu"
    bl_label = "Content of folder"

    item_ui_list_index: IntProperty(name="Index of folder")

    def execute(self, context):
        wm = context.window_manager
        folder = wm.cloud_data[self.item_ui_list_index]
        if not folder.children_as_requested:
            bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
            res = self.get_cloud(context, folder.path_lower)
            bpy.context.window.cursor_set("DEFAULT")
            new_items = self.add_ui_list_with_dropbox_data(res, context)
            self.move_ui_items(
                moving_items=new_items,
                insert_in=self.item_ui_list_index+1,
                items=wm.cloud_data,
                parent=folder,
            )
            folder.children_as_requested = True
            folder.is_expanded = not folder.is_expanded
            return {'FINISHED'}

        if folder.is_expanded:
            childrens = self.get_childs(folder, self.item_ui_list_index, wm.cloud_data)
            history_op = MenuOperatorHistory(
                type=OperatorHistoryType.FOLDING,
                item_id=folder.id,
                item_index=self.item_ui_list_index,
                childs=childrens,
                collection=wm.cloud_data,
                timestamp=datetime.now(),
            )
            history_op.exec_callback()
            context.scene.menu_history.append(history_op)
        else:
            history_op_objs = [
                op for op in context.scene.menu_history
                if op.item_id == folder.id and op.op_datetime < datetime.now()
            ]
            history_op_objs.sort(key=lambda i: i.op_datetime, reverse=True)
            last_operation = history_op_objs[0]
            history_op = MenuOperatorHistory(
                type=OperatorHistoryType.UNFOLDING,
                item_id=folder.id,
                item_index=self.item_ui_list_index,
                childs=last_operation.childrens,
                collection=wm.cloud_data,
                timestamp=datetime.now(),
            )
            history_op.exec_callback()
            context.scene.menu_history.append(history_op)
        folder.is_expanded = not folder.is_expanded
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RefreshFolderContent)
    bpy.utils.register_class(FolderContentOpMenu)

def unregister():
    bpy.utils.unregister_class(RefreshFolderContent)
    bpy.utils.unregister_class(FolderContentOpMenu)
