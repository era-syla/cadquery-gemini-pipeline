import cadquery as cq

# --- Parameters ---
length = 180.0        # Total length of the remote housing
width = 52.0          # Total width
height = 24.0         # Height of the housing
wall_thickness = 2.0  # Thickness of the plastic shell
fillet_r_ends = width / 2.0 - 0.01  # Radius to create stadium shape (slightly less than half width)
fillet_r_bottom = 14.0 # Radius for the bottom curvature (belly)

# Internal feature parameters
boss_od = 9.0         # Outer diameter of screw bosses
boss_id = 3.5         # Inner diameter of screw holes
boss_spacing = 55.0   # Distance of bosses from the center point
rib_thickness = 1.5   # Thickness of structural ribs

# --- 1. Main Body Generation ---

# Create the base solid: An extruded rectangle with rounded vertical edges (stadium shape)
# We use a centered rectangle for the straight section and fillet the corners to round the ends.
base_sketch = (
    cq.Workplane("XY")
    .rect(length - width, width) 
    .extrude(height)
)

# Apply fillet to vertical edges to form the rounded ends
base_stadium = base_sketch.edges("|Z").fillet(fillet_r_ends)

# Apply fillet to the bottom edges to create the curved "belly" profile
# Selecting edges at Z=0 (bottom)
base_solid = base_stadium.edges("<Z").fillet(fillet_r_bottom)

# Shell the object to create the hollow housing
# We remove the top face (>Z) and specify negative thickness for inward offset
shell = base_solid.faces(">Z").shell(-wall_thickness)

# --- 2. Internal Structure (Bosses & Ribs) ---

# Helper function to create the raw solid for a boss
def make_boss_raw(y_pos):
    return (
        cq.Workplane("XY")
        .workplane(offset=-5) # Start below the floor to ensure full penetration
        .center(0, y_pos)
        .circle(boss_od / 2.0)
        .extrude(height + 5) # Extrude high enough
    )

# Helper function to create the raw solid for a supporting rib
def make_rib_raw(y_pos):
    return (
        cq.Workplane("XY")
        .workplane(offset=-5)
        .center(0, y_pos)
        .rect(width - wall_thickness*2, rib_thickness) # Full width rib
        .extrude(height * 0.65) # Ribs are usually lower than the rim
    )

# Create the internal solids
boss_front = make_boss_raw(boss_spacing)
boss_rear = make_boss_raw(-boss_spacing)
rib_front = make_rib_raw(boss_spacing)
rib_rear = make_rib_raw(-boss_spacing)

# Center circular detail (ring on the floor)
center_ring = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .circle(10.0)
    .circle(8.0) # Inner circle to make it a ring
    .extrude(5.0 + 5.0)
)

# Combine all raw internal parts
internals_raw = boss_front.union(boss_rear).union(rib_front).union(rib_rear).union(center_ring)

# Trim internals to match the outer contour
# Intersecting with the original solid 'base_solid' trims the parts sticking out of the bottom
# and creates a perfect fit with the curved floor.
internals_trimmed = internals_raw.intersect(base_solid)

# Create holes for the bosses
def make_boss_hole(y_pos):
    return (
        cq.Workplane("XY")
        .workplane(offset=-10)
        .center(0, y_pos)
        .circle(boss_id / 2.0)
        .extrude(height + 20)
    )

hole_front = make_boss_hole(boss_spacing)
hole_rear = make_boss_hole(-boss_spacing)

# Apply holes to the internal structure
internals_final = internals_trimmed.cut(hole_front).cut(hole_rear)

# Merge the internals into the main shell
result = shell.union(internals_final)

# --- 3. External Cutouts ---

# Front IR Window Cutout (Rectangular hole at the far tip)
ir_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=length/2.0 + 5) # Position plane in front of the object
    .center(0, height/2.0 + 3)        # Center vertically
    .rect(14, 8)
    .extrude(-20)                     # Cut backwards into the object
)

# Rear Cable Cutout (U-shaped slot at the rear rim)
rear_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=-(length/2.0) - 5) # Position plane behind the object
    .center(0, height)                   # Align with top rim
    .rect(12, 12)                        # Size of the slot
    .extrude(20)                         # Cut forwards into the object
)

# Apply the cutouts
result = result.cut(ir_cutout).cut(rear_cutout)