import cadquery as cq

# --- Parameter Definitions ---
width = 50.0             # Width of the block (X-axis)
depth = 50.0             # Depth of the block (Y-axis)
half_height_center = 14.0 # Z-height of one half at the center
half_height_edge = 11.0   # Z-height of one half at the edge
gap = 2.0                # Total gap between the two halves
pipe_dia = 12.0          # Diameter of the pipe channels
pipe_spacing = 24.0      # Center-to-center spacing of the pipes
center_hole_dia = 10.0   # Diameter of the central hole
cbore_dia = 15.0         # Counterbore diameter for central hole
cbore_depth = 4.0        # Counterbore depth
small_hole_dia = 4.0     # Diameter of the 4 mounting holes
small_hole_spacing = 28.0 # Spacing of the 4 mounting holes

# Derived offset
z_start = gap / 2.0

# --- Geometry Construction ---

# 1. Create the Top Half Blank
# Sketch the profile on the Front (XZ) plane: a shape with a curved top and flat bottom
top_blank = (
    cq.Workplane("XZ")
    .moveTo(-width / 2.0, z_start)
    .lineTo(-width / 2.0, z_start + half_height_edge)
    .threePointArc(
        (0, z_start + half_height_center), 
        (width / 2.0, z_start + half_height_edge)
    )
    .lineTo(width / 2.0, z_start)
    .close()
    .extrude(depth / 2.0, both=True) # Extrude symmetrically along Y
)

# 2. Create Pipe Cutters
# Define cylinders along the Y-axis centered at Z=0
# These will cut semi-circles into the bottom of the top half
pipe_cutters = (
    cq.Workplane("XZ")
    .center(-pipe_spacing / 2.0, 0)
    .circle(pipe_dia / 2.0)
    .workplane()
    .center(pipe_spacing / 2.0, 0)
    .circle(pipe_dia / 2.0)
    .extrude(depth / 2.0, both=True)
)

# Apply the cut
top_half = top_blank.cut(pipe_cutters)

# 3. Create Hole Cutters
# Define a workplane slightly above the highest point of the part to ensure clean cuts
wp_holes = cq.Workplane("XY", origin=(0, 0, z_start + half_height_center + 1.0))

# Central Through Hole
center_hole_cutter = wp_holes.circle(center_hole_dia / 2.0).extrude(-half_height_center * 3)

# Central Counterbore
# Depth includes the 1.0mm offset plus the actual counterbore depth
center_cbore_cutter = cq.Workplane("XY", origin=(0, 0, z_start + half_height_center + 1.0)).circle(cbore_dia / 2.0).extrude(-(cbore_depth + 1.0))

# 4 Mounting Holes
small_holes_cutter = (
    cq.Workplane("XY", origin=(0, 0, z_start + half_height_center + 1.0))
    .pushPoints([
        (-small_hole_spacing / 2.0, -small_hole_spacing / 2.0),
        (-small_hole_spacing / 2.0, small_hole_spacing / 2.0),
        (small_hole_spacing / 2.0, -small_hole_spacing / 2.0),
        (small_hole_spacing / 2.0, small_hole_spacing / 2.0)
    ])
    .circle(small_hole_dia / 2.0)
    .extrude(-half_height_center * 3)
)

# Apply the hole cuts
top_half = top_half.cut(center_hole_cutter).cut(center_cbore_cutter).cut(small_holes_cutter)

# 4. Create Bottom Half
# Mirror the top half across the XY plane (Z=0)
bottom_half = top_half.mirror("XY")

# 5. Combine into Final Result
result = top_half.union(bottom_half)