import cadquery as cq

# Parameters for the geometric construction
radius = 20.0
groove_width = 2.0
groove_depth = 1.0
button_outer_radius = 6.0
button_inner_radius = 4.0

# 1. Base Geometry: Main Sphere
# Centered at the origin (0,0,0)
result = cq.Workplane("XY").sphere(radius)

# 2. Tool Creation: Equatorial Groove
# We create a ring (tube) oriented along the Z-axis.
# This represents the material to be removed for the band around the middle.
# Inner radius determines the depth of the groove from the sphere surface.
groove_outer = cq.Workplane("XY").workplane(offset=-groove_width/2).circle(radius + 2).extrude(groove_width)
groove_inner = cq.Workplane("XY").workplane(offset=-groove_width/2).circle(radius - groove_depth).extrude(groove_width)
groove_tool = groove_outer.cut(groove_inner)

# 3. Tool Modification: Button Keepout Zone
# The groove should not pass through the button area on the front.
# We create a mask (cylinder) along the X-axis (front direction) to interrupt the groove tool.
button_mask = (
    cq.Workplane("YZ")
    .circle(button_outer_radius)
    .extrude(radius * 1.5)  # Extrude along +X direction
)

# Remove the mask volume from the groove tool.
# This ensures the groove stops exactly at the button's outer boundary on the front face.
trimmed_groove_tool = groove_tool.cut(button_mask)

# 4. Tool Creation: Button Ring Recess
# The black ring around the button needs to follow the curvature of the sphere.
# We create this by intersecting a spherical shell (depth definition) with a cylindrical tube (shape definition).

# A spherical shell defined by the outer surface and the groove depth
shell_outer = cq.Workplane("XY").sphere(radius)
shell_inner = cq.Workplane("XY").sphere(radius - groove_depth)
shell_tool = shell_outer.cut(shell_inner)

# A tube along the X-axis defining the ring's 2D profile
ring_outer = cq.Workplane("YZ").circle(button_outer_radius).extrude(radius * 1.5)
ring_inner = cq.Workplane("YZ").circle(button_inner_radius).extrude(radius * 1.5)
button_ring_profile = ring_outer.cut(ring_inner)

# Intersect to get a curved ring tool
button_recess_tool = shell_tool.intersect(button_ring_profile)

# 5. Final Boolean Operations
# Apply the cut for the equatorial groove and the button ring.
# The center of the button remains untouched, leaving it as the original spherical surface.
result = result.cut(trimmed_groove_tool).cut(button_recess_tool)