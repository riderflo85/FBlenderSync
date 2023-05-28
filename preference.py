from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty


FR = {
    'Drb-App-Key': 'Clé publique de votre application Dropbox.',
    'Drb-App-Secret': 'Clé secrète de votre application Dropbox.',
    'Pref-Header-Inputs': 'Entrez vous clés secrètes que vous pouvez retrouvez sur votre compte Dropbox.',
    'Local-Storage-Folder': 'Dossier dans lequel sera téléchargé vos fichiers de votre cloud.',
    'Bl-Label-Login': 'Connexion à l\'API Dropbox.',
}


class FBlenderSyncPreferences(AddonPreferences):
    bl_idname = 'fblender_sync'
    
    dropbox_app_key: StringProperty(
        name=FR['Drb-App-Key'],
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    dropbox_app_secret: StringProperty(
        name=FR['Drb-App-Secret'],
        default='',
        options={'HIDDEN', 'SKIP_SAVE'},
        subtype='PASSWORD'
    )
    local_filepath: StringProperty(
        name=FR['Local-Storage-Folder'],
        default='',
        options={'HIDDEN'},
        subtype='DIR_PATH'
    )
    
    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text=FR['Pref-Header-Inputs'], icon='WORLD')

        layout.prop(self, 'dropbox_app_key')
        layout.prop(self, 'dropbox_app_secret')
        layout.prop(self, 'local_filepath')
        layout.operator(FBlenderSyncLoginDropbox.bl_idname)


class FBlenderSyncLoginDropbox(Operator):
    bl_idname = 'fblender_sync.login_drb'
    bl_label = FR['Bl-Label-Login']

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons['fblender_sync'].preferences
        
        info = f'local_filepath -> {addon_prefs.local_filepath} | app key -> {addon_prefs.dropbox_app_key} | app secret -> {addon_prefs.dropbox_app_secret}'
        
        self.report({'INFO'}, info)
        print(info)
        
        return {'FINISHED'}
