bl_info = {
    "name": "Random shake per connected mesh",
    "category": "Mesh",
}

import bpy
import bmesh
import random
import mathutils
from mathutils import Vector


class RandomShakeMesh(bpy.types.Operator):
    """Random shake per connected meshes"""
    bl_idname = "object.random_shake_mesh"        # unique identifier for buttons and menu items to reference.
    bl_label = "Random shake"         						  # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}
    seed = bpy.props.IntProperty(name="seed", default=1, min=0, max=10000)
    scaleTranslate = bpy.props.FloatProperty(name="scale translate", default=1, min=0, max=100)
    scale_rotate = bpy.props.FloatProperty(name="scale rotate", default=1, min=0, max=100)

    def execute(self, context):        # execute() is called by blender when running the operator.

        rand = random.Random()
        rand.seed(a=self.seed)

        obj = bpy.context.edit_object
        mesh = obj.data
        bmes = bmesh.from_edit_mesh(mesh)

        selected_faces = []
        visible_faces = []

        for face in bmes.faces:
            if face.select:
                selected_faces.append(face)
            if not face.hide:
                visible_faces.append(face)
            face.select = False


        for face in bmes.faces:
            if not face.hide:
                face.select = True
                #connect to other faces
                bpy.ops.mesh.select_linked()
                #find center of selected
                ob = bpy.context.object
                v = [v.co for v in bmes.verts if v.select]
                mat = ob.matrix_world
                loc = mat * (sum(v, Vector()) / len(v))
                selected_verts = [v for v in bmes.verts if v.select]

                #shake selected
                rotateX = (rand.random() - 0.5)
                rotateY = (rand.random() - 0.5)
                rotateZ = (rand.random() - 0.5)
                axis = mathutils.Vector((rotateX, rotateY, rotateZ))
                axis.normalize()
                axis.to_4d()
                mat_rot = mathutils.Matrix.Rotation(self.scale_rotate, 4, axis)
                bmesh.ops.rotate(bmes, cent=loc, matrix=mat_rot, verts=selected_verts)

                #hide selected
                bpy.ops.mesh.hide(unselected=False)

        for face in bmes.faces:
            face.hide = False
            face.select = False
        for vert in bmes.verts:
            vert.hide = False
        for face in selected_faces:
            face.select = True

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(RandomShakeMesh.bl_idname)

def register():
    bpy.utils.register_class(RandomShakeMesh)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(RandomShakeMesh)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()