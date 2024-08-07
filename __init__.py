# FBlenderSync created by Florent GRENAILLE

bl_info = {
    'name': 'FBlenderSync',
    'author': 'Florent Grenaille',
    'version': (2, 1, 1),
    'blender': (3, 0, 0),
    'location': '3D View > Sidebar',
    'description': 'Add the Dropbox Cloud to upload or download blender file.',
    'doc_url': 'https://github.com/riderflo85/FBlenderSync',
    'category': 'System'
}

import bpy
from bpy.props import CollectionProperty, IntProperty, PointerProperty


if 'preference' in locals():
    import importlib
    preference = importlib.reload(preference)
    profiles = importlib.reload(profiles)
    mixins = importlib.reload(mixins)
    menu = importlib.reload(menu)
    history = importlib.reload(history)
    operators = importlib.reload(operators)
    properties = importlib.reload(properties)
    # handlers = importlib.reload(handlers)
    FBlenderSyncPreferences = preference.FBlenderSyncPreferences
    FBlenderSyncLoginDropbox = preference.FBlenderSyncLoginDropbox
    FBlenderSyncSaveSettings = preference.FBlenderSyncSaveSettings
    FContextMixin = mixins.FContextMixin
    register_menu = menu.register
    unregister_menu = menu.unregister
    register_history = history.register
    unregister_history = history.unregister
    register_operators = operators.register
    unregister_operators = operators.unregister

else:
    from .profiles import make_profiles_path
    from .profiles import FBlenderProfile
    from .properties import ItemExplorerProperties
    from .properties import SaveOnCloudProperties
    from .properties import StorageCloudProperties
    from .properties import RemoveCloudItemProperties
    from .preference import FBlenderSyncPreferences
    from .preference import FBlenderSyncLoginDropbox
    from .preference import FBlenderSyncSaveSettings
    from .mixins import FContextMixin
    from .menu import register as register_menu
    from .menu import unregister as unregister_menu
    from .history import register as register_history
    from .history import unregister as unregister_history
    from .operators import register as register_operators
    from .operators import unregister as unregister_operators
    # from .handlers import pre_save_handler


klass = (
    FBlenderSyncPreferences,
    FBlenderSyncLoginDropbox,
    FBlenderSyncSaveSettings,
    ItemExplorerProperties,
    SaveOnCloudProperties,
    StorageCloudProperties,
    RemoveCloudItemProperties,
)

# functions = (
#     pre_save_handler,
# )

def register():
    make_profiles_path()
    FBlenderProfile.read_json()

    # for klfs in klass + functions:
    #     bpy.utils.register_class(klfs)

    for kls in klass:
        bpy.utils.register_class(kls)

    preferences = FContextMixin.addon_prefs(bpy.context)

    preferences.local_filepath = FBlenderProfile.LOCAL_STORAGE_FOLDER
    preferences.dropbox_app_key = FBlenderProfile.APP_KEY
    preferences.dropbox_app_secret = FBlenderProfile.APP_SECRET
    preferences.token = FBlenderProfile.ACCESS_TOKEN or 'NOT-SET'
    preferences.refresh_token = FBlenderProfile.REFRESH_TOKEN or 'NOT-SET'
    preferences.expire_token = FBlenderProfile.EXPIRE_TOKEN or 'NOT-SET'
    preferences.download_mode = FBlenderProfile.DOWNLOAD_MODE

    register_history()
    register_operators()
    register_menu()

    bpy.types.WindowManager.cloud_data = CollectionProperty(type=ItemExplorerProperties)
    bpy.types.WindowManager.cloud_data_index = IntProperty(name="Index for cloud_data", default=-1)
    bpy.types.WindowManager.save_on_cloud = PointerProperty(type=SaveOnCloudProperties)
    bpy.types.WindowManager.cloud_storage = PointerProperty(type=StorageCloudProperties)
    bpy.types.WindowManager.items_to_delete = PointerProperty(type=RemoveCloudItemProperties)


def unregister():
    # for klfs in klass + functions:
    #     bpy.utils.unregister_class(klfs)
    for kls in klass:
        bpy.utils.unregister_class(kls)
    unregister_history()
    unregister_operators()
    unregister_menu()

    del bpy.types.WindowManager.cloud_data
    del bpy.types.WindowManager.cloud_data_index
    del bpy.types.WindowManager.save_on_cloud
    del bpy.types.WindowManager.cloud_storage
    del bpy.types.WindowManager.items_to_delete


if __name__ == "__main__":
    register()
