import cadquery as cq

# ------------------------------------------------------------------------------
# Object Analysis & Parameters
# ------------------------------------------------------------------------------
# The object consists of a central flat disk and a long bar running through it.
# The bar has a distinctive cross-section with longitudinal ridges/grooves on top.
# The bar ends are rounded (slot shape in plan view).
# The connection between bar and disk is filleted.

# Dimensions (estimated from visual proportions)
bar_length = 140.0
bar_width = 12.0
bar_base_height = 6.0   # Height of the rectangular base of the bar
ridge_radius = 0.8      # Radius of the semicircular ridges
disk_diameter = 42.0
disk_thickness = 3.0
fillet_neck = 2.0       # Fillet at bar-disk junction
fillet_rim = 1.0        # Fillet at disk outer edge

# ------------------------------------------------------------------------------
# Geometry Construction
# ------------------------------------------------------------------------------

def create_wavy_profile_wire(width, height, r_ridge):
    """
    Creates a closed wire for the bar's cross-section (YZ plane).
    The top surface consists of multiple semi-circular ridges.
    """
    # Calculate number of ridges to fit the width
    n_ridges = int(width / (2 * r_ridge))
    # Adjust radius slightly to fit the width perfectly without gaps
    r_adj = width / (2 * n_ridges)
    
    wp = cq.Workplane("YZ")
    
    # Start drawing the profile
    # 1. Bottom edge (left to right)
    # 2. Right vertical edge (up)
    path = wp.moveTo(-width/2, 0).lineTo(width/2, 0).lineTo(width/2, height)
    
    # 3. Top wavy edge (right to left)
    current_y = width / 2
    for _ in range(n_ridges):
        mid_y = current_y - r_adj
        end_y = current_y - 2 * r_adj
        # Create a semi-circle bulging upwards (+Z direction relative to the line)
        # using threePointArc: start (implicit), mid, end
        path = path.threePointArc((mid_y, height + r_adj), (end_y, height))
        current_y = end_y
        
    # 4. Left vertical edge (down) and close
    path = path.close()
    
    return path

# 1. Create the Bar
# Step A: Generate the raw bar extrusion with the wavy top
# We center the extrusion along the X-axis.
profile_wire = create_wavy_profile_wire(bar_width, bar_base_height, ridge_radius)
# Offset workplane to start extrusion from negative X, extrude to positive X
raw_bar = profile_wire.workplane(offset=-bar_length/2 - 10).extrude(bar_length + 20)

# Step B: Create a cutter to define the rounded plan-view shape (Slot)
# A slot shape centered at origin in XY plane, extruded vertically
slot_shape = cq.Workplane("XY").slot2D(bar_length, bar_width).extrude(bar_base_height + ridge_radius + 5)

# Step C: Intersect raw bar with slot shape to get the final bar geometry
# This creates the rounded ends while preserving the wavy top profile
bar = raw_bar.intersect(slot_shape)

# 2. Create the Central Disk
disk = cq.Workplane("XY").circle(disk_diameter/2).extrude(disk_thickness)

# 3. Combine Components
# Union the disk and the bar
result = disk.union(bar)

# ------------------------------------------------------------------------------
# Refinement (Fillets)
# ------------------------------------------------------------------------------

# 1. Fillet the "neck" where the bar rises out of the disk.
# We select edges on the top surface of the disk.
# Strategy: Select edges at Z = disk_thickness.
# Filter: The neck edges are straight lines (geomType 'LINE') formed by the intersection.
# (The outer rim is a 'CIRCLE' and should be excluded from this fillet)
neck_edges = []
for edge in result.edges().vals():
    bb = edge.BoundingBox()
    if abs(bb.zmin - disk_thickness) < 0.01 and abs(bb.zmax - disk_thickness) < 0.01:
        if edge.geomType() == 'LINE':
            neck_edges.append(edge)

if neck_edges:
    result = result.edges(cq.selectors.BoxSelector(neck_edges)).fillet(fillet_neck)

# 2. Fillet the top outer rim of the disk.
# Filter: Select the circular edge at Z = disk_thickness.
top_rim_edges = []
for edge in result.edges().vals():
    bb = edge.BoundingBox()
    if abs(bb.zmin - disk_thickness) < 0.01 and abs(bb.zmax - disk_thickness) < 0.01:
        if edge.geomType() == 'CIRCLE':
            top_rim_edges.append(edge)

if top_rim_edges:
    result = result.edges(cq.selectors.BoxSelector(top_rim_edges)).fillet(fillet_rim)

# 3. Fillet the bottom outer rim of the disk.
bottom_rim_edges = []
for edge in result.edges().vals():
    bb = edge.BoundingBox()
    if abs(bb.zmin) < 0.01 and abs(bb.zmax) < 0.01:
        if edge.geomType() == 'CIRCLE':
            bottom_rim_edges.append(edge)

if bottom_rim_edges:
    result = result.edges(cq.selectors.BoxSelector(bottom_rim_edges)).fillet(fillet_rim)