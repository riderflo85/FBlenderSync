import bpy


def pre_save_handler(dummy):
    """
    Versionning file before save.
    """
    if bpy.context.scene.get("metadata", False):
        bpy.context.scene["metadata"]["scene_version"] += 1
