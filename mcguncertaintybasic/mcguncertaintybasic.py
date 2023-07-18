bl_info = {
    "name": "MCG Uncertainty Basic",
    "category": "Object",
    "location": "View3D > Sidebar > MCG Uncertainty Basic",
    "author": "MCG-Artan Salihu",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Uncertainty Model in paper https://arxiv.org/pdf/2203.10506.pdf",
    "warning": "",
    "wiki_url": "www.artansaliu.com",
    "tracker_url": "https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/",
    "support": "MCG-Artna Salihu",
}

import bpy
import random
from mathutils import Vector
from bpy.props import FloatVectorProperty
import math

class NoiseGeneratorProperties(bpy.types.PropertyGroup):
    T: bpy.props.IntProperty(name="T", description="Key frames for the uncertainty model", default=100)
    std_dev: bpy.props.FloatProperty(name="sigma", description="std dev (Only Gaussian noise for now)", default=0.1)

class OBJECT_OT_add_noise(bpy.types.Operator):
    bl_idname = "object.add_noise"
    bl_label = "Add Noise"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ng_tool = scene.ng_tool

        mean = 0 #Lets keep mean constant here for now. Can be changed later

        bpy.ops.object.select_all(action='SELECT')

        # Over selected objects, add noise to their location
        for obj in bpy.context.selected_objects:
            initial_loc = obj.location.copy()
            if obj.animation_data is None:
                obj.animation_data_create()

            # create a new anim if nothing exist
            if obj.animation_data.action is None:
                obj.animation_data.action = bpy.data.actions.new(name="UncertaintyAction")

            for i in range(ng_tool.T):
                n_x = random.gauss(mean, ng_tool.std_dev)
                n_y = random.gauss(mean, ng_tool.std_dev)
                n_z = random.gauss(mean, ng_tool.std_dev)

                obj.location = Vector((initial_loc.x + n_x, initial_loc.y + n_y, initial_loc.z + n_z))

                obj.keyframe_insert(data_path='location', frame=i)

        bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}

class OBJECT_PT_noise_generator(bpy.types.Panel):
    bl_idname = "MCG Uncertainty Basic"
    bl_label = "MCG Uncertainty Basic"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"  # This should be 'UI' for the sidebar
    bl_category = "MCG Uncertainty Basic"  # The name of the tab in the sidebar

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ng_tool = scene.ng_tool

        layout.prop(ng_tool, "T")
        layout.prop(ng_tool, "std_dev")
        layout.operator("object.add_noise")

def register():
    bpy.utils.register_class(NoiseGeneratorProperties)
    bpy.utils.register_class(OBJECT_OT_add_noise)
    bpy.utils.register_class(OBJECT_PT_noise_generator)
    bpy.types.Scene.ng_tool = bpy.props.PointerProperty(type=NoiseGeneratorProperties)

def unregister():
    bpy.utils.unregister_class(NoiseGeneratorProperties)
    bpy.utils.unregister_class(OBJECT_OT_add_noise)
    bpy.utils.unregister_class(OBJECT_PT_noise_generator)
    del bpy.types.Scene.ng_tool

if __name__ == "__main__":
    register()
