import bpy, time
from bpy.props import StringProperty, CollectionProperty, BoolProperty, IntProperty

from .mixins import FMenuMixin, FDropBoxMixin


class Item(bpy.types.PropertyGroup):
    tag: StringProperty(name="Type of document (file or folder)")
    name: StringProperty(name="Item Name")
    path_lower: StringProperty(name="Dropbox path lower")
    path_display: StringProperty(name="Dropbox path display")
    id: StringProperty(name="Dropbox ID")
    client_modified: StringProperty(name="Iso datetime")
    server_modified: StringProperty(name="Iso datetime")
    size: IntProperty(name="File size in Dropbox. In Octet", default=0)
    content_hash: StringProperty(name="Content hash Dropbox")
    is_downloadable: BoolProperty(name="File is downloadable from Dropbox", default=False)
    is_expanded: BoolProperty(name="Expanded", default=False)
    is_folder: BoolProperty(name="Folder", default=False)
    children_as_requested: BoolProperty(name="If children as requested or not", default=False)
    parent_id: StringProperty(name="Folder parent")
    indent_level: IntProperty(name="Indentation", default=0)
    # index: IntProperty(name="Index in collection", default=-1)


class ItemUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        column = layout.column(align=True)

        main_row = column.row()

        section_1 = main_row.row(align=True)
        section_1.alignment = 'LEFT'

        section_2 = main_row.row(align=True)
        section_2.alignment = 'RIGHT'

        row = section_1
        row.separator()

        if item.indent_level:
            for _ in range(item.indent_level):
                row.label(icon='BLANK1')

        if item.is_folder:
            child_op = row.operator(GetSubMenu.bl_idname, text="", emboss=False, icon='TRIA_DOWN' if item.is_expanded else 'TRIA_RIGHT')
            child_op.item_ui_list_index = index

        row.label(
            text=item.name,
            icon="FILE_FOLDER" if item.is_folder else "FILE_BLANK",
        )
        # row.label(text=item.id)


class GetSubMenu(FDropBoxMixin, bpy.types.Operator):
    """Create the new button with API data response"""
    bl_idname = "fblender_sync.create_button"
    bl_label = "Get the content sub menu Dropbox"
    
    item_ui_list_index: IntProperty(name="Index of folder")

    def execute(self, context):
        folder = context.scene.custom_items[self.item_ui_list_index]
        if not folder.children_as_requested:
            bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
            res = self.get_cloud(context, folder.path_lower)
            bpy.context.window.cursor_set("DEFAULT")
            new_items = self.add_ui_list_with_dropbox_data(res, context)
            self.move_ui_items(
                moving_items=new_items,
                insert_in=self.item_ui_list_index+1,
                items=context.scene.custom_items,
                parent=folder,
            )
            folder.children_as_requested = True
        folder.is_expanded = not folder.is_expanded
        # print("res SubMenu : ", res)
        return {'FINISHED'}


class GetCloudButton(FDropBoxMixin, bpy.types.Operator):
    bl_idname = "fblender_sync.get_cloud"
    bl_label = "Get the content first root Dropbox"
    
    root_drb_path: StringProperty(name="Root path to DropBox cloud", default="")

    def execute(self, context):
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res = self.get_cloud(context, self.root_drb_path)
        bpy.context.window.cursor_set("DEFAULT")
        if len(context.scene.custom_items) > 0:
            context.scene.custom_items.clear()
        print("response get folder API : ", res)
        self.add_ui_list_with_dropbox_data(res, context)
        return {'FINISHED'}


class UploadCurrentFile(bpy.types.Operator):
    """Upload the current file into DropBox"""
    bl_idname = "fblender_sync.upload_current_file"
    bl_label = "Export Some Data TEST"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        self.report({'INFO'}, "TEST LOG 1 path file %s" % self.filepath)
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        time.sleep(2) # Simulate the request api timer
        return {'FINISHED'}

    def invoke(self, context, event):
        self.report({'INFO'}, "TEST LOG 2")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# Définir une classe de menu personnalisée
class MyMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Menu principal"
    bl_idname = "fblender_sync.menu"

    button_label = "" # TEST Upload

    def draw(self, context):
        layout = self.layout

        # Ajouter des éléments de menu
        layout.operator(UploadCurrentFile.bl_idname, text="Envoyer le fichier actuel")
        layout.operator(GetCloudButton.bl_idname, text="Consulter le cloud")
        if self.button_label:
            layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


class ExplorerMenu(FMenuMixin, bpy.types.Panel):
    bl_label = "Fichiers Cloud"
    bl_idname = "fblender_sync.menu.explorer"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("ItemUIList", "", scene, "custom_items", scene, "custom_items_index")


# Enregistrer le menu personnalisé
def register():
    bpy.utils.register_class(Item)
    bpy.utils.register_class(ItemUIList)
    bpy.utils.register_class(GetSubMenu)
    bpy.utils.register_class(GetCloudButton)
    bpy.utils.register_class(UploadCurrentFile)
    bpy.utils.register_class(MyMenu)
    bpy.utils.register_class(ExplorerMenu)

    bpy.types.Scene.custom_items = CollectionProperty(type=Item)
    bpy.types.Scene.custom_items_index = IntProperty(name="Index for custom_items", default=-1)
    # for index, folder in enumerate(folders):
    #     id_name = "fblender_sync.menu.%s" % index

    #     new_menu = type(
    #         "MyMenu%s" % index,
    #         (bpy.types.Panel, ),
    #         {
    #             "bl_idname": id_name,
    #             "bl_label": folder[1],
    #             "bl_category": "Test Florent",
    #             "bl_space_type": 'VIEW_3D',
    #             "bl_region_type": 'UI',
    #             "button_label": folder[0],
    #             "draw": draw
    #         }
    #     )
    #     bpy.utils.register_class(new_menu)

# Supprimer le menu personnalisé
def unregister():
    bpy.utils.unregister_class(Item)
    bpy.utils.unregister_class(ItemUIList)
    bpy.utils.unregister_class(GetSubMenu)
    bpy.utils.unregister_class(GetCloudButton)
    bpy.utils.unregister_class(UploadCurrentFile)
    bpy.utils.unregister_class(MyMenu)
    bpy.utils.unregister_class(ExplorerMenu)
    
    del bpy.types.Scene.custom_items
    del bpy.types.Scene.custom_items_index


# Exécuter l'enregistrement du menu lors de l'exécution du script
if __name__ == "__main__":
    register()
    # unregister()
