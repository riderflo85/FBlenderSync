from bpy.props import CollectionProperty

from .statics import APP_NAME
from .server import DropboxAPI
from .profiles import FBlenderProfile


class FMenuMixin:
    bl_category = "Cloud service"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


class FContextMixin:
    @staticmethod
    def addon_prefs(context):
        try:
            prefs = context.preferences
        except AttributeError:
            prefs = context.user_preferences

        addon_prefs = prefs.addons[APP_NAME].preferences
        return addon_prefs
    
    @staticmethod
    def attribute_data(ui_item, data: dict):
        ui_item.tag = data[".tag"]
        ui_item.name = data["name"]
        ui_item.id = data["id"]
        ui_item.path_lower = data["path_lower"]
        ui_item.path_display = data["path_display"]
        if data[".tag"] == "folder":
            ui_item.is_folder = True
        elif data[".tag"] == "file":
            ui_item.client_modified = data["client_modified"]
            ui_item.server_modified = data["server_modified"]
            ui_item.size = data["size"]
            ui_item.is_downloadable = data["is_downloadable"]
            ui_item.content_hash = data["content_hash"]
        splited_path = data["path_lower"].split("/")
        splited_path.pop(0)
        ui_item.indent_level = len(splited_path) - 1

    @staticmethod
    def _set_items_index(collection):
        for index, item in enumerate(collection):
            item.index = index

    def set_storage_infos(self, context, allocated: bytes, used: bytes):
        wm = context.window_manager
        # 1 gigaoctet = 1 073 741 824 bytes
        giga_in_bytes = 1073741824
        allocated_go = allocated / giga_in_bytes
        used_go = used / giga_in_bytes
        wm.cloud_storage.allocated = allocated_go
        wm.cloud_storage.used = used_go
        wm.cloud_storage.factor = (used_go * 100) / allocated_go

    @staticmethod
    def collection_to_dict_index(collection: CollectionProperty) -> dict:
        return {
            i.id: index
            for index, i in enumerate(collection)
        }

    @staticmethod
    def get_childs(folder, folder_index: int, find_in: CollectionProperty):
        childrens = []
        for item in find_in:
            if item.id == folder.id or item.index < folder_index:
                continue
            if item.indent_level == folder.indent_level:
                break
            if item.indent_level > folder.indent_level:
                childrens.append({k: v for k, v in item.items()})
        return childrens

    def add_ui_list_with_dropbox_data(self, drb_data: dict, context):
        new_items = []
        wm = context.window_manager
        for data in drb_data:
            new_item = wm.cloud_data.add()
            self.attribute_data(new_item, data)
            new_items.append(new_item)
        self._set_items_index(wm.cloud_data)
        return new_items

    def move_ui_items(self, moving_items: list, insert_in: int, items: CollectionProperty, parent):
        next_index = insert_in
        for item in moving_items:
            dict_collection = self.collection_to_dict_index(items)
            item.parent_id = parent.id
            item_index = dict_collection.get(item.id)
            if item_index >= 0:
                items.move(item_index, next_index)
                next_index += 1
        self._set_items_index(items)


class FDropBoxMixin(FContextMixin):
    def cloud_action(self, context, action: str, **kwargs):
        addon_prefs = self.addon_prefs(context)
        drb = DropboxAPI(
            app_key=addon_prefs.dropbox_app_key,
            app_secret=addon_prefs.dropbox_app_secret,
            in_blender=True,
            fbl_profile_klass=FBlenderProfile,
            bl_preferences=addon_prefs,
        )
        if not hasattr(drb, action):
            raise AttributeError(f"'{DropboxAPI}' object has not attribute '{action}'")
        drb_action = getattr(drb, action)
        kwargs["token"] = addon_prefs.token
        return drb_action(**kwargs)
