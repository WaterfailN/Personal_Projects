import csv
import bpy

bar_spacing = 1.5
bar_width = 1

filepath = "D:\Code Projects\Python Projects\Blender X Python\Simple Bars Visualisation\sample.csv"
with open(filepath) as f:
    readout = list(csv.reader(f))
    
for idx, a in enumerate(readout):
    bpy.ops.mesh.primitive_plane_add(size=1)
    new_bar = bpy.context.object
    
    for vert in new_bar.data.vertices:
        vert.co[1] += 0.5
        vert.co[0] += idx * bar_spacing + 0.5
    
    new_bar.scale = (bar_width, float(a[1]), 1)
    
    bpy.ops.object.text_add()
    bpy.context.object.data.align_x = 'RIGHT'
    bpy.context.object.data.align_y = 'CENTER'
    bpy.ops.transform.rotate(value=1)
    bpy.ops.transform.translate(value=(idx * bar_spacing + 0.5, -0.5, 0))
    bpy.context.object.data.body = a[0]



        