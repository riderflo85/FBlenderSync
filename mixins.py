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
    def attribute_data(ui_item, data: dict, new_av_folder=None):
        ui_item.tag = data[".tag"]
        ui_item.name = data["name"]
        ui_item.id = data["id"]
        ui_item.path_lower = data["path_lower"]
        ui_item.path_display = data["path_display"]
        if data[".tag"] == "folder":
            ui_item.is_folder = True
            new_av_folder.id = data["id"]
            new_av_folder.name = data["path_display"]
            new_av_folder.desc = data["name"]
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
            if data[".tag"] == "folder":
                new_available_folder = wm.available_folders.add()
                self.attribute_data(new_item, data, new_av_folder=new_available_folder)
            else:
                self.attribute_data(new_item, data)
            new_items.append(new_item)
        self._set_items_index(wm.cloud_data)
        return new_items

    def move_ui_items(self, moving_items: list, insert_in: int, items: CollectionProperty, parent):
        next_index = insert_in
        for item in moving_items:
            item.parent_id = parent.id
            item_index = items.find(item.name)
            if item_index >= 0:
                items.move(item_index, next_index)
                next_index += 1
        self._set_items_index(items)


class FDropBoxMixin(FContextMixin):
    def get_cloud(self, context, path):
        addon_prefs = self.addon_prefs(context)
        drb = DropboxAPI(
            app_key=addon_prefs.dropbox_app_key,
            app_secret=addon_prefs.dropbox_app_secret,
            in_blender=True,
            fbl_profile_klass=FBlenderProfile,
            bl_preferences=addon_prefs,
        )
        return drb.get_content_folder(addon_prefs.token, path)

    def dl_file(self, context, cloud_path):
        addon_prefs = self.addon_prefs(context)
        drb = DropboxAPI(
            app_key=addon_prefs.dropbox_app_key,
            app_secret=addon_prefs.dropbox_app_secret,
            in_blender=True,
            fbl_profile_klass=FBlenderProfile,
            bl_preferences=addon_prefs,
        )
        return drb.download_file(addon_prefs.token, cloud_path)

    def upl_file(self, context, cloud_path, path_file, file_exist):
        mode = "overwrite" if file_exist else "add"
        addon_prefs = self.addon_prefs(context)
        drb = DropboxAPI(
            app_key=addon_prefs.dropbox_app_key,
            app_secret=addon_prefs.dropbox_app_secret,
            in_blender=True,
            fbl_profile_klass=FBlenderProfile,
            bl_preferences=addon_prefs,
        )
        return drb.upload_file(
            addon_prefs.token,
            path_file,
            cloud_path,
            mode,
        )
