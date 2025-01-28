# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_import_lst

import random
import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel, Scene
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Import LST",
    "description": "Add the Default Cube for each line of reading file and apply the format from this line to the created cube",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Import LST",
    "doc_url": "https://github.com/Korchy/1d_import_lst",
    "tracker_url": "https://github.com/Korchy/1d_import_lst",
    "category": "All"
}


# MAIN CLASS

class ImportLST:

    @classmethod
    def import_lst(cls, context, lst_filepath, op):

        import time
        start_time = time.time()

        # add the Default Cube for each line of reading file and apply the format from this line to the created cube
        lines_processed = 0
        try:
            # read from lst_filepath file line by line
            with open(lst_filepath, mode='rb') as lst_file:
                for line in lst_file:
                    # apply UTF-8 to enable cyrillic
                    line = line.decode('utf-8')
                    # remove line breaks
                    line = line.replace('\n', '').replace('\r', '')
                    # process each line
                    cls._process_lst_line(context=context, line=line)
                    # counting
                    lines_processed += 1
            # show message on finish
            op.report(
                type={'INFO'},
                message='Processed LST: ' + str(lines_processed) + ' lines.'
            )
        except IOError as e:
            op.report(
                type={'INFO'},
                message='Error reading LST file'
            )

        print("--- %s seconds ---" % (time.time() - start_time))

    @classmethod
    def _process_lst_line(cls, context, line):
        # process single lst line
        # format: (object_name object_coord object_scale object_rotation_by_z material_name)
        # ex: (R9,25 (181.966 349.558 0.0) (2.5 2.5 2.5) 5.4862 крона)
        if line:
            line_data = line.split(' ')
            # print(line_data)
            if line_data:
                obj_name = line_data[0][1:]
                obj_co = (float(line_data[1][1:]), float(line_data[2]), float(line_data[3][:-1]))
                obj_scale = (float(line_data[4][1:]), float(line_data[5]), float(line_data[6][:-1]))
                obj_r_z = float(line_data[7][:-1]) if len(line_data) == 8 else float(line_data[7])
                obj_mat = line_data[8][:-1] if len(line_data) == 9 else None
                # print(obj_name, obj_co, obj_scale, obj_r_z, obj_mat)
                # add the default cube
                bpy.ops.mesh.primitive_cube_add(
                    location=obj_co,
                    rotation=(0.0, 0.0, obj_r_z)
                )
                # set name
                context.active_object.name = obj_name
                # set scale
                context.active_object.scale = obj_scale
                # set material
                if obj_mat:
                    if obj_mat not in context.blend_data.materials:
                        cls._add_material(material_name=obj_mat)
                    context.active_object.data.materials.append(context.blend_data.materials[obj_mat])

    @staticmethod
    def _add_material(material_name):
        # add material to the scene
        # material
        material = bpy.data.materials.get(material_name)
        if not material:
            material = bpy.data.materials.new(name=material_name)
        # nodes
        material.use_nodes = True
        material_output = material.node_tree.nodes.get('Material Output')
        if not material_output:
            material_output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
        material_output.location = (500.0, 200.0)
        principled_bsdf = material.node_tree.nodes.get('Principled BSDF')
        if not principled_bsdf:
            principled_bsdf = material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        principled_bsdf.location = (0.0, 0.0)
        principled_bsdf.inputs[0].default_value = (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), 1.0)
        # links
        material.node_tree.links.new(principled_bsdf.outputs[0], material_output.inputs[0])

    @staticmethod
    def ui(layout, context):
        # ui panel
        layout.prop(
            data=context.scene,
            property='importlst_pref_lst_file_path',
            text=''
        )
        layout.operator(
            operator='importlst.import_lst',
            icon='OBJECT_DATA'
        )

# OPERATORS

class ImportLST_OT_import_lst(Operator):
    bl_idname = 'importlst.import_lst'
    bl_label = 'Import LST'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ImportLST.import_lst(
            context=context,
            lst_filepath=bpy.path.abspath(context.scene.importlst_pref_lst_file_path),
            op=self
        )
        return {'FINISHED'}


# PANELS

class ImportLST_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'ImportLST'
    bl_category = '1D'

    def draw(self, context):
        ImportLST.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    Scene.importlst_pref_lst_file_path = StringProperty(
        name='LST File Path',
        subtype='FILE_PATH'
    )
    register_class(ImportLST_OT_import_lst)
    if ui:
        register_class(ImportLST_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(ImportLST_PT_panel)
    unregister_class(ImportLST_OT_import_lst)
    del Scene.importlst_pref_lst_file_path


if __name__ == '__main__':
    register()
