# FBlenderSync created by Florent GRENAILLE

bl_info = {
    'name': 'FBlenderSync',
    'author': 'Florent Grenaille',
    'version': (1, 0),
    'blender': (3, 0, 0),
    'location': '3D View > Sidebar',
    'description': 'Add the Dropbox Cloud to upload or download blender file.',
    'doc_url': 'https://github.com/riderflo85/FBlenderSync',
    'category': 'System'
}

import bpy


if 'preference' in locals():
    import importlib
    preference = importlib.reload(preference)
    profiles = importlib.reload(profiles)
    mixins = importlib.reload(mixins)
    FBlenderSyncPreferences = preference.FBlenderSyncPreferences
    FBlenderSyncLoginDropbox = preference.FBlenderSyncLoginDropbox
    FContextMixin = mixins.FContextMixin

else:
    from . import profiles
    from .preference import FBlenderSyncPreferences
    from .preference import FBlenderSyncLoginDropbox
    from .mixins import FContextMixin


def register():
    profiles_path, profiles_file = profiles.make_profiles_path()
    profiles_data = profiles.get_profiles_data(profiles_path, profiles_file)

    bpy.utils.register_class(FBlenderSyncPreferences)
    bpy.utils.register_class(FBlenderSyncLoginDropbox)

    preferences = FContextMixin.addon_prefs(bpy.context)

    preferences.local_filepath = profiles_data['LOCAL_STORAGE_FOLDER'] if profiles_data.get('LOCAL_STORAGE_FOLDER') else ''
    preferences.dropbox_app_key = profiles_data['APP_KEY'] if profiles_data.get('APP_KEY') else ''
    preferences.dropbox_app_secret = profiles_data['APP_SECRET'] if profiles_data.get('APP_SECRET') else ''


def unregister():
    bpy.utils.unregister_class(FBlenderSyncPreferences)
    bpy.utils.unregister_class(FBlenderSyncLoginDropbox)


if __name__ == "__main__":
    register()
