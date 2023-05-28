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
    FBlenderSyncPreferences = preference.FBlenderSyncPreferences
    FBlenderSyncLoginDropbox = preference.FBlenderSyncLoginDropbox

else:
    from .preference import FBlenderSyncPreferences
    from .preference import FBlenderSyncLoginDropbox


def register():
    bpy.utils.register_class(FBlenderSyncPreferences)
    bpy.utils.register_class(FBlenderSyncLoginDropbox)

def unregister():
    bpy.utils.unregister_class(FBlenderSyncPreferences)
    bpy.utils.unregister_class(FBlenderSyncLoginDropbox)


if __name__ == "__main__":
    register()
