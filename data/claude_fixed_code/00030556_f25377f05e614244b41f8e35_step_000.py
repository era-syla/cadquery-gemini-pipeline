import cadquery as cq

# --- Parameters ---
# Base dimensions
base_len = 80.0
base_w_bottom = 50.0
base_w_top = 30.0
base_height = 30.0
wall_vertical_h = 15.0  # Height before the slope starts

# Feature dimensions
slot_width = 16.0
hole_height = 18.0
hole_dia = 8.0

# Tool (Floating Part) dimensions
tool_thickness = 10.0  # X dimension
tool_width = 16.0      # Y dimension (fits in slot)
tool_height = 24.0     # Z dimension
scoop_radius = 6.0
pin_len_stickout = 8.0

# --- 1. Create the Tool Geometry ---
# The tool is a rectangular block with concave cuts and a pin
# Modeled centered at origin
tool_solid = cq.Workplane("XY").box(tool_thickness, tool_width, tool_height)

# Create the scooping cylinder (along Y axis)
scoop = (
    cq.Workplane("XZ")
    .circle(scoop_radius)
    .extrude(tool_width + 5, both=True)
)

# Cut top and bottom scoops
tool_solid = (
    tool_solid
    .cut(scoop.translate((0, 0, tool_height / 2)))
    .cut(scoop.translate((0, 0, -tool_height / 2)))
)

# Add the pin (Cylinder along Y axis, sticking out one side)
pin = (
    cq.Workplane("XZ")
    .circle(hole_dia / 2)
    .extrude(tool_width / 2 + pin_len_stickout)
)
tool_solid = tool_solid.union(pin)

# --- 2. Create the Tool Cluster (Pattern) ---
# 3 tools arranged radially (-45, 0, 45 degrees) around the Y axis
# The pin axis (Y) is the center of rotation
cluster = (
    tool_solid
    .union(tool_solid.rotate((0, 0, 0), (0, 1, 0), 45))
    .union(tool_solid.rotate((0, 0, 0), (0, 1, 0), -45))
)

# --- 3. Create the Main Base ---
# Define the trapezoidal profile on the YZ plane
pts = [
    (-base_w_bottom / 2, 0),
    (base_w_bottom / 2, 0),
    (base_w_bottom / 2, wall_vertical_h),
    (base_w_top / 2, base_height),
    (-base_w_top / 2, base_height),
    (-base_w_bottom / 2, wall_vertical_h)
]

# Extrude base along X
base = cq.Workplane("YZ").polyline(pts).close().extrude(base_len / 2, both=True)

# Cut the longitudinal slot (U-channel)
# Simple rectangular cut along X
slot_cutter = (
    cq.Workplane("YZ")
    .center(0, base_height)
    .rect(slot_width, base_height * 2)
    .extrude(base_len / 2 + 5, both=True)
)
base = base.cut(slot_cutter)

# Drill the cross hole
base = (
    base.faces(">Y").workplane()
    .center(0, hole_height)
    .circle(hole_dia / 2)
    .cutThruAll()
)

# Subtract the Tool Cluster from the Base
# Position the cluster at the hole location
base_final = base.cut(cluster.translate((0, 0, hole_height)))

# --- 4. Assemble the Scene ---
# Position the floating parts to match the image
display_tool = tool_solid.translate((-40, 0, 60))
display_cluster = cluster.translate((40, 0, 60))

# Combine everything into one result
result = base_final.union(display_tool).union(display_cluster)