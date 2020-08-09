import bpy

bl_info = {
    "name": "Cursor to AE Position",
    "description": "Copy the Blender 3D cursor position to the clipboard as After Effects keyframe data",
    "author": "adroitwhiz",
    "blender": (2, 80, 0),
    "category": "3D View",
    "version": (1, 0)
}


class CursorToAEPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    multiply_coords_by_100: bpy.props.BoolProperty(
        name="Multiply coordinates by 100",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "multiply_coords_by_100")

class CursorToAE(bpy.types.Operator):
    """Cursor to AE Position Script"""
    bl_idname = "view3d.cursor_to_ae_position"
    bl_label = "Cursor to AE Position"

    def execute(self, context):
        addon_prefs = context.preferences.addons[__name__].preferences
        scale_factor = 100 if addon_prefs.multiply_coords_by_100 else 1

        loc = context.scene.cursor.location
        loc_ae = (loc[0] * scale_factor, loc[2] * -scale_factor, loc[1] * scale_factor)
        context.window_manager.clipboard = """Adobe After Effects 8.0 Keyframe Data

Transform	Position
	Frame	X pixels	Y pixels	Z pixels
		{}	{}	{}


End of Keyframe Data""".format(loc_ae[0], loc_ae[1], loc_ae[2])


        self.report({'INFO'}, 'Copied cursor position to clipboard as AE keyframe data')
        return {'FINISHED'}

def render_panel(self, context):
    layout = self.layout
    row = layout.row()
    row.operator(CursorToAE.bl_idname)

def register():
    bpy.utils.register_class(CursorToAE)
    bpy.utils.register_class(CursorToAEPrefs)
    bpy.types.VIEW3D_PT_view3d_cursor.append(render_panel)


def unregister():
    bpy.utils.unregister_class(CursorToAE)
    bpy.utils.unregister_class(CursorToAEPrefs)
    bpy.types.VIEW3D_PT_view3d_cursor.remove(render_panel)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
