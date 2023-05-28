from .statics import APP_NAME


class FContextMixin:
    @staticmethod
    def addon_prefs(context):
        try:
            prefs = context.preferences
        except AttributeError:
            prefs = context.user_preferences

        addon_prefs = prefs.addons[APP_NAME].preferences
        return addon_prefs
