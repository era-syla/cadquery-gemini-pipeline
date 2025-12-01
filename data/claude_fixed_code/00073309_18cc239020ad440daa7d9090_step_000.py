import cadquery as cq

# Geometric parameters derived from image analysis
height = 50.0
max_radius = 22.0
belly_z = 20.0        # Height of the widest part of the egg
wall_thickness = 1.5  # Thickness of the shell
side_hole_dia = 26.0  # Diameter of the large side hole
top_hole_dia = 7.0    # Diameter of the small top hole

# 1. Create the Egg Shell
# We define the profile on the XZ plane and revolve it around the Z axis.
# The profile is a spline starting at (0,0), going through the widest point, and ending at (0, height).
# Tangents are defined to ensure the shape is rounded at the bottom/top and vertical at the belly.
pts = [(max_radius, belly_z), (0, height)]
tangents = [(0, 1), (1, 0), (0, 1), (-1, 0)]

base_egg = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(pts, tangents=tangents, includeCurrent=True)
    .close()  # Connects the top point back to (0,0) to close the profile
    .revolve() # Defaults to revolving around the Z axis (relative Y of XZ plane)
)

# Hollow out the solid egg to create a shell
# A negative offset creates the shell inwards, preserving outer dimensions
shell = base_egg.shell(-wall_thickness)

# 2. Create the Side Hole Cutter
# We create a cylinder oriented along the Y axis.
# Drawing on the XZ plane and extruding creates a shape along the Y axis (normal to XZ).
side_cutter = (
    cq.Workplane("XZ")
    .moveTo(0, belly_z)
    .circle(side_hole_dia / 2.0)
    .extrude(max_radius * 3, both=True) # Ensure it passes through the entire object
)

# 3. Create the Top Hole Cutter
# We create a cylinder oriented along the Z axis to cut the tip.
top_cutter = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .circle(top_hole_dia / 2.0)
    .extrude(height * 2, both=True)
)

# 4. Apply the Cuts
# Subtract the cutters from the hollow shell
result = shell.cut(side_cutter).cut(top_cutter)