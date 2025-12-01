import cadquery as cq

# Parameters defining the impeller geometry
hub_diameter = 20.0
hub_thickness = 5.0
blade_count = 12
blade_length = 15.0
blade_width = 7.0
blade_thickness = 1.2
blade_pitch_angle = 45.0
cutout_offset = 5.0  # Radial distance to cutout center
cutout_size = 6.0    # Diameter of the circumcircle for the triangular cutout

# 1. Create the central hub
# Start with a simple cylinder
hub = cq.Workplane("XY").circle(hub_diameter / 2).extrude(hub_thickness)

# 2. Create the triangular cutouts
# Subtract the cutouts from the hub in a pattern
for i in range(4):
    angle = i * 90
    cutout_tool = (
        cq.Workplane("XY")
        .polygon(3, cutout_size)
        .extrude(hub_thickness * 2)          # Extra length to ensure full cut
        .translate((0, 0, -hub_thickness))   # Center vertically relative to hub
        .rotate((0, 0, 0), (0, 0, 1), 180)   # Rotate to point inward
        .translate((cutout_offset, 0, 0))    # Move radially outward
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    hub = hub.cut(cutout_tool)

# 3. Create the fan blades
# Union the blades onto the hub in a polar pattern
result = hub
for i in range(blade_count):
    angle = i * (360.0 / blade_count)
    blade_instance = (
        cq.Workplane("XY")
        .box(blade_length, blade_width, blade_thickness)
        .rotate((0, 0, 0), (1, 0, 0), blade_pitch_angle) # Apply pitch twist
        # Move to the edge of the hub with a slight overlap (-1.0) for union
        .translate((hub_diameter / 2 + blade_length / 2 - 1.0, 0, hub_thickness / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(blade_instance)