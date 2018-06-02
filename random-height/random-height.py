bl_info = {
    "name": "Random shrink/fatten per face",
    "category": "Mesh",
}

import bpy
import bmesh
import random


class RandomShrinkFattenPerFace(bpy.types.Operator):
    """Random shrink/fatten per selected face""" 
    bl_idname = "object.random_shrink_fatten_per_face"        # unique identifier for buttons and menu items to reference.
    bl_label = "Random height"         						  # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  	
    scale = bpy.props.FloatProperty(name="scale", default=1, min=0, max=100)
    seed = bpy.props.IntProperty(name="seed", default=1, min=0, max=10000)
	
    def execute(self, context):        # execute() is called by blender when running the operator.

        rand = random.Random()
        rand.seed(a=self.seed)
        
        obj = bpy.context.edit_object
        mesh = obj.data
        bmes = bmesh.from_edit_mesh(mesh)

        selectedFaces = []

        for face in bmes.faces:
        	if face.select:
        		selectedFaces.append(face)
        		face.select = False

        for face in selectedFaces:
        	face.select = True
        	amount = self.scale * (rand.random() + rand.random() + rand.random() + rand.random() - 2) / 20
        	bpy.ops.transform.shrink_fatten(value=amount)
        	face.select = False
        	
        for face in selectedFaces:
        	face.select = True

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(RandomShrinkFattenPerFace.bl_idname)		
		
def register():
    bpy.utils.register_class(RandomShrinkFattenPerFace)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(RandomShrinkFattenPerFace)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()