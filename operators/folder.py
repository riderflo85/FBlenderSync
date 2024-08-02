from datetime import datetime

import bpy
from bpy.props import IntProperty, StringProperty

from ..mixins import FDropBoxMixin
from ..history import MenuOperatorHistory, OperatorHistoryType
from ..statics import APP_NAME


class RefreshFolderContent(FDropBoxMixin, bpy.types.Operator):
    """Refresh the folder content with Dropbox API request response"""
    bl_idname = f"{APP_NAME}.refresh_folder_content"
    bl_label = "Refresh folder content"

    item_ui_list_index: IntProperty(name="Index of folder")

    def execute(self, context):
        wm = context.window_manager
        folder = wm.cloud_data[self.item_ui_list_index]

        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.cloud_action(context, "get_content_folder", path=folder.path_lower)
        b_allocated, b_used = self.cloud_action(context, "get_storage_infos")
        self.set_storage_infos(context, b_allocated, b_used)
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
    bl_idname = f"{APP_NAME}.folder_content_op_menu"
    bl_label = "Content of folder"

    item_ui_list_index: IntProperty(name="Index of folder")

    def execute(self, context):
        wm = context.window_manager
        folder = wm.cloud_data[self.item_ui_list_index]
        if not folder.children_as_requested:
            bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
            res = self.cloud_action(context, "get_content_folder", path=folder.path_lower)
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
            wm.menu_history.append(history_op)
        else:
            history_op_objs = [
                op for op in wm.menu_history
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
            wm.menu_history.append(history_op)
        folder.is_expanded = not folder.is_expanded
        return {'FINISHED'}


class NewFolderCloud(FDropBoxMixin, bpy.types.Operator):
    """Create a new folder on cloud and Blender UI menu."""
    bl_idname = f"{APP_NAME}.new_folder_op"
    bl_label = "Create a new folder"

    item_ui_list_index: IntProperty(name="Index of folder", default=-1)
    folder_name: StringProperty(name="Nom du dossier")

    @staticmethod
    def _add_folder(wm, data):
        new_folder = wm.cloud_data.add()
        new_folder.tag = "folder"
        new_folder.is_folder = True
        new_folder.name = data["name"]
        new_folder.id = data["id"]
        new_folder.path_lower = data["path_lower"]
        new_folder.path_display = data["path_display"]
        splited_path = data["path_lower"].split("/")
        splited_path.pop(0)
        new_folder.indent_level = len(splited_path) - 1
        return new_folder

    @classmethod
    def poll(cls, context):
        return len(context.window_manager.cloud_data) > 0

    def execute(self, context):
        if self.folder_name == "":
            return {"CANCELLED"}
        wm = context.window_manager
        if self.item_ui_list_index == -1:
            root_path = "/%s" % self.folder_name
            folder_parent = None
        else:
            folder_parent = wm.cloud_data[self.item_ui_list_index]
            root_path = "%s/%s" % (folder_parent.path_display, self.folder_name)
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        cloud_response = self.cloud_action(context, "create_folder", path=root_path)
        bpy.context.window.cursor_set("DEFAULT")
        if folder_parent:
            if folder_parent.is_expanded:
                new_folder = self._add_folder(wm, cloud_response)
                self.move_ui_items(
                    moving_items=[new_folder],
                    insert_in=self.item_ui_list_index+1,
                    items=wm.cloud_data,
                    parent=folder_parent,
                )
            else:
                app_ops = getattr(bpy.ops, APP_NAME)
                folder_content_op_id = FolderContentOpMenu.bl_idname.split(".")[-1]
                folder_content_operator = getattr(app_ops, folder_content_op_id)
                folder_content_operator(item_ui_list_index=self.item_ui_list_index)
        else:
            self._add_folder(wm, cloud_response)

        self.folder_name = ""
        self.item_ui_list_index = -1
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Créer un dossier")
        layout.separator()
        col = layout.column()
        col.prop(self, "folder_name")


def register():
    bpy.utils.register_class(RefreshFolderContent)
    bpy.utils.register_class(FolderContentOpMenu)
    bpy.utils.register_class(NewFolderCloud)

def unregister():
    bpy.utils.unregister_class(RefreshFolderContent)
    bpy.utils.unregister_class(FolderContentOpMenu)
    bpy.utils.unregister_class(NewFolderCloud)
