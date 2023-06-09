from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty

from .mixins import FContextMixin
from .statics import APP_NAME
from .i18n import get_label as gt_
from .profiles import make_profiles_path
from .profiles import get_profiles_data
from .profiles import save_profiles_data


class FBlenderSyncPreferences(AddonPreferences):
    bl_idname = APP_NAME

    dropbox_app_key: StringProperty(
        name=gt_('Drb-App-Key'),
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    dropbox_app_secret: StringProperty(
        name=gt_('Drb-App-Secret'),
        default='',
        options={'HIDDEN', 'SKIP_SAVE'},
        subtype='PASSWORD'
    )
    local_filepath: StringProperty(
        name=gt_('Local-Storage-Folder'),
        default='',
        options={'HIDDEN'},
        subtype='DIR_PATH'
    )
    token: StringProperty(
        name='token',
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    refresh_token: StringProperty(
        name='refresh-token',
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    expire_token: StringProperty(
        name='expire-token',
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text=gt_('Pref-Header-Inputs'), icon='WORLD')
    
        if self.token == 'NOT-SET':
            row_col = col.row()
            row_col.label(text='Token non récupéré !', icon='BLANK1')
            row_col.operator(FBlenderSyncLoginDropbox.bl_idname) # À remplacer par un vrai bouton, la c'est pour un test
        # Faire le check pour la validation du token
        # elif ....:
        else:
            col.label(text='Token encore valide', icon='FAKE_USER_ON')
            

        layout.prop(self, 'dropbox_app_key')
        layout.prop(self, 'dropbox_app_secret')
        layout.prop(self, 'local_filepath')
        row = layout.row()
        row.operator(FBlenderSyncSaveSettings.bl_idname)
        row.operator(FBlenderSyncLoginDropbox.bl_idname)


class FBlenderSyncSaveSettings(FContextMixin, Operator):
    bl_idname = f'{APP_NAME}.save_settings'
    bl_label = gt_('Bt-Save-Settings')

    def execute(self, context):
        addon_prefs = self.addon_prefs(context) # Defined in FContextMixin

        self.report({'INFO'}, gt_('FB-Success-Write-Pref'))

        profiles_path, profiles_file = make_profiles_path()
        profiles_data = get_profiles_data(profiles_path, profiles_file)
        profiles_data.update({
            'APP_KEY': addon_prefs.dropbox_app_key,
            'APP_SECRET': addon_prefs.dropbox_app_secret,
            'LOCAL_STORAGE_FOLDER': addon_prefs.local_filepath
        })
        save_profiles_data(profiles_file, profiles_data)

        return {'FINISHED'}


class FBlenderSyncLoginDropbox(FContextMixin, Operator):
    bl_idname = f'{APP_NAME}.login_drb'
    bl_label = gt_('Bl-Label-Login')

    def execute(self, context):
        addon_prefs = self.addon_prefs(context) # Defined in FContextMixin

        self.report({'INFO'}, 'Login success')

        return {'FINISHED'}
