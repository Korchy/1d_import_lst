# 1D Import LST

Blender add-on.

Add-on functionality
-
1. Read user file by specified path.

File format:
    
(object_name object_coord object_scale object_rotation_by_z material_name)

Ex:

    (R9,25 (181.966 349.558 0.0) (2.5 2.5 2.5) 5.4862 крона)
    (999 (685.686 357.373 0.0) (0.2 0.2 0.2) 0 2)
    ...

2. Each line describes one creating object
3. Add the "Default Cube" to the scene for each line of the file and apply data from this line to the created cube.

Blender version
-
2.79

Current version
-
1.0.2

Version history
-
1.0.2
- added material color for new materials to its diffuse_color property

1.0.1
- if material from processed line doesn't exists in the scene - create new and use it

1.0.0
- Release
