import os
import shutil

import bpy
from bpy.props import BoolProperty

from ..mixins import FDropBoxMixin, FContextMixin
from ..statics import APP_NAME


class DeleteCloudItem(FDropBoxMixin, bpy.types.Operator):
    """Delete a cloud item."""
    bl_idname = f"{APP_NAME}.delete_cloud_item"
    bl_label = "Supprimer un élément"

    delete_locale: BoolProperty(
        name="Supprimer en local.",
        description="Supprimer l'élément de votre disque dur en même temps.",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return len(context.window_manager.cloud_data.keys()) > 0

    def execute(self, context):
        wm = context.window_manager
        cloud_id_to_delete = wm.items_to_delete.item
        if cloud_id_to_delete == "-1":
            return {"CANCELLED"}
        dict_items_index = self.collection_to_dict_index(wm.cloud_data)
        index_to_delete = dict_items_index.get(cloud_id_to_delete)
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.cloud_action(context, "delete_file_or_folder", id_target=cloud_id_to_delete)
        bpy.context.window.cursor_set("DEFAULT")
        if res == "done":
            b_allocated, b_used = self.cloud_action(context, "get_storage_infos")
            self.set_storage_infos(context, b_allocated, b_used)
            if self.delete_locale:
                addon_prefs = FContextMixin.addon_prefs(context)
                root_prefix = addon_prefs.local_filepath
                item = wm.cloud_data[index_to_delete]
                path = f"{root_prefix}{item.path_lower}"
                if item.is_folder and os.path.exists(path):
                    if len(os.listdir(path)) == 0:
                        os.rmdir(path)
                    else:
                        shutil.rmtree(path)
                        children_folders = self.get_childs(item, index_to_delete, wm.cloud_data)
                        for children in children_folders:
                            children_index = dict_items_index[children["id"]]
                            wm.cloud_data.remove(children_index)
                elif os.path.isfile(path):
                    os.remove(path)
            self.report({"INFO"}, "Item supprimé avec succès !")
            wm.cloud_data.remove(index_to_delete)
        return {"FINISHED"}


    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        layout.prop(self, "delete_locale")
        layout.prop(wm.items_to_delete, "item")
        


def register():
    bpy.utils.register_class(DeleteCloudItem)

def unregister():
    bpy.utils.unregister_class(DeleteCloudItem)