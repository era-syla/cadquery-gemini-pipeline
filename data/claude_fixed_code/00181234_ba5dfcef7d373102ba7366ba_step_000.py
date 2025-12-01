import cadquery as cq

# Dimensions estimated from the image
base_od = 60.0          # Outer diameter of the bottom flange
top_od = 50.0           # Outer diameter of the top section
bore_id = 44.0          # Inner diameter (through hole)
base_height = 20.0      # Height of the bottom flange
top_height = 25.0       # Height of the top section
total_height = base_height + top_height
slit_width = 1.5        # Width of the vertical cut
relief_hole_dia = 4.0   # Diameter of the hole at the shoulder

# 1. Create the Base Cylinder
# We start on the XY plane and extrude the wider base.
base = cq.Workplane("XY").circle(base_od / 2.0).extrude(base_height)

# 2. Create the Top Cylinder
# Create a workplane on top of the base (offset by base_height) and extrude the narrower top.
top = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(top_od / 2.0)
    .extrude(top_height)
)

# 3. Fuse the parts
# Combine the base and top cylinders into one solid.
body = base.union(top)

# 4. Create the Central Bore
# Cut the inner diameter through the entire object.
body = body.faces(">Z").workplane().circle(bore_id / 2.0).cutThruAll()

# 5. Create the Vertical Slit Cutter
# A rectangular box positioned to cut the wall on one side (aligned with +X axis).
# The box is centered at (Radius, 0, Z-center) to cut through the wall thickness.
slit_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height / 2.0)
    .center(base_od / 2.0, 0)
    .rect(base_od, slit_width)
    .extrude(total_height, both=True)
)

# 6. Create the Relief Hole Cutter
# A cylinder oriented radially to drill the hole at the step intersection.
# We use the YZ plane (normal to X) and center it at the step height.
# Local coords on YZ: X=Global Y, Y=Global Z.
hole_cutter = (
    cq.Workplane("YZ")
    .center(0, base_height)
    .circle(relief_hole_dia / 2.0)
    .extrude(base_od)
)

# 7. Apply the Cuts
# Subtract the slit and the hole from the main body.
result = body.cut(slit_cutter).cut(hole_cutter)