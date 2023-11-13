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
    FBlenderSyncSaveSettings = preference.FBlenderSyncSaveSettings
    FContextMixin = mixins.FContextMixin

else:
    from .profiles import make_profiles_path
    from .profiles import FBlenderProfile
    from .preference import FBlenderSyncPreferences
    from .preference import FBlenderSyncLoginDropbox
    from .preference import FBlenderSyncSaveSettings
    from .mixins import FContextMixin


klass = (
    FBlenderSyncPreferences,
    FBlenderSyncLoginDropbox,
    FBlenderSyncSaveSettings,
)

def register():
    make_profiles_path()
    # profiles_data = profiles.get_profiles_data(profiles_path, profiles_file)
    FBlenderProfile.read_json()

    for kls in klass:
        bpy.utils.register_class(kls)

    preferences = FContextMixin.addon_prefs(bpy.context)

    preferences.local_filepath = FBlenderProfile.LOCAL_STORAGE_FOLDER
    preferences.dropbox_app_key = FBlenderProfile.APP_KEY
    preferences.dropbox_app_secret = FBlenderProfile.APP_SECRET
    preferences.token = FBlenderProfile.ACCESS_TOKEN or 'NOT-SET'
    preferences.refresh_token = FBlenderProfile.REFRESH_TOKEN or 'NOT-SET'
    preferences.expire_token = FBlenderProfile.EXPIRE_TOKEN or 'NOT-SET'



def unregister():
    for kls in klass:
        bpy.utils.unregister_class(kls)


if __name__ == "__main__":
    register()
