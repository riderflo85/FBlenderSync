# import bpy, time


import bpy


class MATERIAL_UL_cloud_content(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        ma = slot.material
        print("item : ", item)
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


# And now we can use this list everywhere in Blender. Here is a small example panel.
class MyMenuUIList(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Menu principal"
    bl_idname = "MENU_PT_fblender_sync.menu"
    bl_category = "Test UIList"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        # template_list now takes two new args.
        # The first one is the identifier of the registered UIList to use (if you want only the default list,
        # with no custom draw code, use "UI_UL_list").
        layout.template_list("MATERIAL_UL_cloud_content", "", obj, "material_slots", obj, "active_material_index")

        # The second one can usually be left as an empty string.
        # It's an additional ID used to distinguish lists in case you
        # use the same list several times in a given area.
        layout.template_list("MATERIAL_UL_cloud_content", "compact", obj, "material_slots",
                             obj, "active_material_index", type='COMPACT')


def register():
    bpy.utils.register_class(MATERIAL_UL_cloud_content)
    bpy.utils.register_class(MyMenuUIList)


def unregister():
    bpy.utils.unregister_class(MATERIAL_UL_cloud_content)
    bpy.utils.unregister_class(MyMenuUIList)


if __name__ == "__main__":
    register()











# class MixinMenu:
#     bl_category = "Test Florent"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'


# def get_api():
#     time.sleep(2)
#     return [{'path_name': '/test', 'type': 'folder', 'name': 'Test'}]


# def add_menu_button(api_data, operator_class):
#     def draw(self, context):
#         layout = self.layout
#         layout.operator(operator_class.bl_idname)

#     for index, data in enumerate(api_data):
#         if data.get('type') == 'folder':
#             bl_idname = "fblender_sync.sub_menu%s" % index

#             new_menu = type(
#                 "SubMenu%s" % index,
#                 (MixinMenu, bpy.types.Panel, ),
#                 {
#                     "bl_idname": bl_idname,
#                     "bl_label": data.get('path_name'),
#                     "bl_options": {'DEFAULT_CLOSED'},
#                     "button_label": bpy.props.StringProperty(default=data.get('name')),
#                     "draw": draw
#                 }
#             )
#             bpy.utils.register_class(new_menu)
        


# class GetSubMenu(bpy.types.Operator):
#     """Create the new button with API data response"""
#     bl_idname = "fblender_sync.create_button"
#     bl_label = "Get the content sub menu Dropbox"

    
#     def execute(self, context):
#         print('ok created')
#         return {'FINISHED'}


# class GetCloudButton(bpy.types.Operator):
#     bl_idname = "fblender_sync.get_cloud"
#     bl_label = "Get the content first root Dropbox"
    
#     def execute(self, context):
        
#         preferences = context.preferences
#         addon_prefs = preferences.addons['fblender_sync'].preferences
        
#         info = f'local_filepath -> {addon_prefs.local_filepath} | app key -> {addon_prefs.dropbox_app_key} | app secret -> {addon_prefs.dropbox_app_secret}'
#         self.report({'INFO'}, info)
#         print('context in GetCloudButton : ', info)
        
#         bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
#         res_api = get_api()
#         add_menu_button(res_api, GetSubMenu)
#         return {'FINISHED'}
    
#     def draw(self, context):
#         pass



# class UploadCurrentFile(bpy.types.Operator):
#     """Upload the current file into DropBox"""
#     bl_idname = "fblender_sync.upload_current_file"
#     bl_label = "Export Some Data TEST"

#     filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
#     # Obtenir le chemin absolu du fichier .blend en cours d'édition
#     # bpy.data.filepath
#     # Savoir si le fichier en cours est sauvegarder ou pas
#     # bpy.data.is_saved

#     @classmethod
#     def poll(cls, context):
#         return context.object is not None

#     def execute(self, context):
#         self.report({'INFO'}, "TEST LOG 1 path file %s" % self.filepath)
#         bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
#         time.sleep(2) # Simulate the request api timer
#         print('context -> ', context)
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         self.report({'INFO'}, "TEST LOG 2")
#         context.window_manager.fileselect_add(self)
#         return {'RUNNING_MODAL'}


# # Définir une classe de menu personnalisée
# class MyMenu(MixinMenu, bpy.types.Panel):
#     bl_label = "Menu principal"
#     bl_idname = "fblender_sync.menu"

#     button_label = "test" # TEST

#     def draw(self, context):
#         layout = self.layout

#         print("test print context addon_pref : ", context.preferences.addons["fblender_sync"].preferences.token)

#         # Ajouter des éléments de menu
#         # layout.operator("mesh.primitive_cube_add", text="Ajouter un cube")
#         # layout.operator("mesh.primitive_uv_sphere_add", text="Ajouter une sphère")
#         layout.operator(UploadCurrentFile.bl_idname, text="Envoyer le fichier actuel")
#         layout.operator(GetCloudButton.bl_idname, text="Consulter le cloud")
#         if self.button_label:
#             layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


# # Enregistrer le menu personnalisé
# def register(folders):

#     # def draw(self, context):
#     #     layout = self.layout
#     #     if self.button_label:
#     #         layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


#     bpy.utils.register_class(GetSubMenu)
#     bpy.utils.register_class(GetCloudButton)
#     bpy.utils.register_class(UploadCurrentFile)
#     bpy.utils.register_class(MyMenu)
#     # for index, folder in enumerate(folders):
#     #     id_name = "fblender_sync.menu.%s" % index

#     #     new_menu = type(
#     #         "MyMenu%s" % index,
#     #         (bpy.types.Panel, ),
#     #         {
#     #             "bl_idname": id_name,
#     #             "bl_label": folder[1],
#     #             "bl_category": "Test Florent",
#     #             "bl_space_type": 'VIEW_3D',
#     #             "bl_region_type": 'UI',
#     #             "button_label": folder[0],
#     #             "draw": draw
#     #         }
#     #     )
#     #     bpy.utils.register_class(new_menu)

# # Supprimer le menu personnalisé
# def unregister(folders):
#     bpy.utils.register_class(GetSubMenu)
#     bpy.utils.register_class(GetCloudButton)
#     bpy.utils.unregister_class(UploadCurrentFile)
#     bpy.utils.unregister_class(MyMenu)


# # Exécuter l'enregistrement du menu lors de l'exécution du script
# if __name__ == "__main__":
#     folder_list = [('folder1', 'Dossier parent'), ('folder2', 'Dossier Toto')]
#     register(folder_list)
#     print(dir(bpy.data))
#     # unregister()
