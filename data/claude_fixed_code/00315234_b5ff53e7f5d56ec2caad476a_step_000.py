import cadquery as cq

# Geometric parameters
length = 80.0   # Main body X dimension
depth = 40.0    # Main body Y dimension
height = 40.0   # Main body Z dimension

hole_diam = 5.0
hole_dist = 40.0 # Distance between hole centers

# Left tab dimensions (on the side face)
lt_prot = 5.0   # Protrusion outward
lt_width = 12.0 # Length along the side
lt_thick = 4.0  # Thickness

# Right tab dimensions (on the front face)
rt_width = 10.0
rt_prot = 3.0
rt_thick = 4.0

# 1. Create Main Body
# Aligned so Front is +Y, Right is +X, Top is +Z
result = cq.Workplane("XY").box(length, depth, height)

# 2. Add Holes on Front Face
# Selecting the face with normal in +Y direction
# Coordinates are relative to the center of the face
result = result.faces(">Y").workplane()\
    .pushPoints([(-hole_dist/2, 0), (hole_dist/2, 0)])\
    .hole(hole_diam)

# 3. Add Left Tab
# Attached to Left Face (<X), flush with Front Face (>Y)
# Vertical position: Centered (Z=0)
# Create a separate solid and union it for precise positioning
# Position: X = Left Face - half protrusion
#           Y = Front Face - half width (to align flush with front)
#           Z = 0
left_tab = cq.Workplane("XY").box(lt_prot, lt_width, lt_thick)\
    .translate((-length/2 - lt_prot/2, depth/2 - lt_width/2, 0))

result = result.union(left_tab.val())

# 4. Add Right Tab
# Attached to Front Face (>Y), near bottom-right corner
# Position: X = Near Right Edge
#           Y = Front Face + half protrusion
#           Z = Below center
right_tab = cq.Workplane("XY").box(rt_width, rt_prot, rt_thick)\
    .translate((length/2 - rt_width - 5, depth/2 + rt_prot/2, -10))

result = result.union(right_tab.val())