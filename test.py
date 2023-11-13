import bpy, time


class MixinMenu:
    bl_category = "Test Florent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


def get_api():
    time.sleep(2)
    return [{'path_name': '/test', 'type': 'folder', 'name': 'Test'}]


def add_menu_button(api_data, operator_class):
    def draw(self, context):
        layout = self.layout
        layout.operator(operator_class.bl_idname)

    for index, data in enumerate(api_data):
        if data.get('type') == 'folder':
            bl_idname = "fblender_sync.sub_menu%s" % index

            new_menu = type(
                "SubMenu%s" % index,
                (MixinMenu, bpy.types.Panel, ),
                {
                    "bl_idname": bl_idname,
                    "bl_label": data.get('path_name'),
                    "bl_options": {'DEFAULT_CLOSED'},
                    "button_label": bpy.props.StringProperty(default=data.get('name')),
                    "draw": draw
                }
            )
            bpy.utils.register_class(new_menu)
        


class GetSubMenu(bpy.types.Operator):
    """Create the new button with API data response"""
    bl_idname = "fblender_sync.create_button"
    bl_label = "Get the content sub menu Dropbox"

    
    def execute(self, context):
        print('ok created')
        return {'FINISHED'}


class GetCloudButton(bpy.types.Operator):
    bl_idname = "fblender_sync.get_cloud"
    bl_label = "Get the content first root Dropbox"
    
    def execute(self, context):
        
        preferences = context.preferences
        addon_prefs = preferences.addons['fblender_sync'].preferences
        
        info = f'local_filepath -> {addon_prefs.local_filepath} | app key -> {addon_prefs.dropbox_app_key} | app secret -> {addon_prefs.dropbox_app_secret}'
        self.report({'INFO'}, info)
        print('context in GetCloudButton : ', info)
        
        bpy.context.window.cursor_set("WAIT") # Set the mouse cursor to WAIT icon
        res_api = get_api()
        add_menu_button(res_api, GetSubMenu)
        return {'FINISHED'}
    
    def draw(self, context):
        pass



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
        print('context -> ', context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.report({'INFO'}, "TEST LOG 2")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# Définir une classe de menu personnalisée
class MyMenu(MixinMenu, bpy.types.Panel):
    bl_label = "Menu principal"
    bl_idname = "fblender_sync.menu"

    button_label = "" # TEST

    def draw(self, context):
        layout = self.layout

        # Ajouter des éléments de menu
        layout.operator("mesh.primitive_cube_add", text="Ajouter un cube")
        layout.operator("mesh.primitive_uv_sphere_add", text="Ajouter une sphère")
        layout.operator(UploadCurrentFile.bl_idname, text="Envoyer le fichier actuel")
        layout.operator(GetCloudButton.bl_idname, text="Consulter le cloud")
        if self.button_label:
            layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


# Enregistrer le menu personnalisé
def register(folders):

    # def draw(self, context):
    #     layout = self.layout
    #     if self.button_label:
    #         layout.operator(UploadCurrentFile.bl_idname, text=self.button_label)


    bpy.utils.register_class(GetSubMenu)
    bpy.utils.register_class(GetCloudButton)
    bpy.utils.register_class(UploadCurrentFile)
    bpy.utils.register_class(MyMenu)
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
def unregister(folders):
    bpy.utils.unregister_class(UploadCurrentFile)
    bpy.utils.unregister_class(MyMenu)


# Exécuter l'enregistrement du menu lors de l'exécution du script
if __name__ == "__main__":
    folder_list = [('folder1', 'Dossier parent'), ('folder2', 'Dossier Toto')]
    register(folder_list)
    # unregister()
