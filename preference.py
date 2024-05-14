from datetime import datetime

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty

from .server import DropboxAPI
from .server import DropboxError
from .helpers import next_expire_time
from .mixins import FContextMixin
from .statics import APP_NAME
from .i18n import get_label as gt_
from .profiles import FBlenderProfile


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
    success_msg: StringProperty(
        name='success-msg',
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )
    error_msg: StringProperty(
        name='error-msg',
        default='',
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text=gt_('Pref-Header-Inputs'), icon='WORLD')

        if self.success_msg:
            col.label(text=self.success_msg, icon='FAKE_USER_ON')

        if self.error_msg:
            col.label(text=self.error_msg, icon='ERROR')

        if self.token in ['NOT-SET', '']:
            col.label(text=gt_('Ms-Not-Token'), icon='BLANK1')
        elif self.expire_token and (
            datetime.now() > datetime.fromisoformat(self.expire_token)
        ):
            expire_token_msg = f"{gt_('Ms-Token-Expires-Out')} {self.expire_token}"
            row_tok = col.row()
            row_tok.label(text=gt_('Ms-Expired-Token'), icon='CANCEL')
            row_tok.label(text=expire_token_msg)
        else:
            expire_token_msg = f"{gt_('Ms-Token-Expires-In')} {self.expire_token}"
            row_tok = col.row()
            row_tok.label(text=gt_('Ms-Valide-Token'), icon='FAKE_USER_ON')
            row_tok.label(text=expire_token_msg)


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

        FBlenderProfile.APP_KEY = addon_prefs.dropbox_app_key
        FBlenderProfile.APP_SECRET = addon_prefs.dropbox_app_secret
        FBlenderProfile.LOCAL_STORAGE_FOLDER = addon_prefs.local_filepath
        FBlenderProfile.EXPIRE_TOKEN = addon_prefs.expire_token
        FBlenderProfile.save_profiles_data()

        return {'FINISHED'}


class FBlenderSyncLoginDropbox(FContextMixin, Operator):
    bl_idname = f'{APP_NAME}.login_drb'
    bl_label = gt_('Bt-Label-Login')

    def execute(self, context):
        addon_prefs = self.addon_prefs(context) # Defined in FContextMixin

        drb = DropboxAPI(addon_prefs.dropbox_app_key, addon_prefs.dropbox_app_secret)

        bpy.context.window.cursor_set('WAIT')
        try:
            token_data = drb.get_access_token()
            print('token data is : ', token_data)
            expire_token_obj = next_expire_time(token_data['expires_in'])
            expire_token = expire_token_obj.isoformat()
            addon_prefs.success_msg = 'Token correctement récupéré !'
            addon_prefs.token = token_data['access_token']
            addon_prefs.refresh_token = token_data['refresh_token']
            addon_prefs.expire_token = expire_token
            FBlenderProfile.ACCESS_TOKEN = token_data['access_token']
            FBlenderProfile.REFRESH_TOKEN = token_data['refresh_token']
            FBlenderProfile.EXPIRE_TOKEN = expire_token
            self.report({'INFO'}, 'Login success')
        except DropboxError as error:
            addon_prefs.error_msg = f"Une erreur c'est produite ! \n{error}"
            addon_prefs.token = 'NOT-SET'
            addon_prefs.refresh_token = ''
            addon_prefs.expire_token = ''
            FBlenderProfile.ACCESS_TOKEN = ''
            FBlenderProfile.REFRESH_TOKEN = ''
            FBlenderProfile.EXPIRE_TOKEN = ''
            self.report({'ERROR'}, f'Login failed {error}')

        FBlenderProfile.save_profiles_data()

        return {'FINISHED'}
