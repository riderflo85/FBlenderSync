import bpy
from bpy.props import StringProperty

from ..statics import APP_NAME


class HelpOperator(bpy.types.Operator):
    bl_idname = f"{APP_NAME}.help"
    bl_label = "Infos"

    message: StringProperty(name="Help message", default="")

    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message, icon="INFO")


def register():
    bpy.utils.register_class(HelpOperator)

def unregister():
    bpy.utils.unregister_class(HelpOperator)
