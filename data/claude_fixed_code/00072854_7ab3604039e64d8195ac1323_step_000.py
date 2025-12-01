import cadquery as cq

# --- Dimensions & Parameters ---
width = 70.0           # Width of all plates
thickness = 4.0        # Material thickness
riser_height = 85.0    # Height of the vertical riser plates
riser_spacing = 150.0  # Distance between the two risers
base_tail_len = 300.0  # Length of the base extension to the left
base_front_len = 50.0  # Length of the base extension to the right
gusset_size = 30.0     # Size of the triangular support

# Coordinate System: Origin (0,0,0) is centered between the risers on the top surface of the base plate.

# --- Base Plate ---
# Calculate total length and center position
total_base_len = base_tail_len + riser_spacing + base_front_len
# Center X of the base plate rectangle relative to Origin
base_center_x = (-base_tail_len + base_front_len) / 2.0

# Create base plate geometry (positioned just below Z=0)
base = (cq.Workplane("XY")
        .workplane(offset=-thickness/2)
        .center(base_center_x, 0)
        .rect(total_base_len, width)
        .extrude(thickness))

# Base Plate Features
tail_end_x = -riser_spacing/2 - base_tail_len
front_end_x = riser_spacing/2 + base_front_len
slot_inset = 20.0

base = (base.faces(">Z").workplane()
        # Slots at the far right end
        .pushPoints([(front_end_x - slot_inset, 20), (front_end_x - slot_inset, -20)])
        .slot2D(20, 6, 0)
        # Slots at the far left end
        .pushPoints([(tail_end_x + slot_inset, 20), (tail_end_x + slot_inset, -20)])
        .slot2D(20, 6, 0)
        # Large rectangular cutouts on the tail section
        .pushPoints([(-riser_spacing/2 - 100, 0), (-riser_spacing/2 - 200, 0)])
        .rect(40, 30)
        # Small mounting holes flanking the rectangular cutouts
        .pushPoints([
            (-riser_spacing/2 - 100 - 35, 0), (-riser_spacing/2 - 100 + 35, 0),
            (-riser_spacing/2 - 200 - 35, 0), (-riser_spacing/2 - 200 + 35, 0)
        ])
        .circle(2.5)
        .cutThruAll())

# --- Risers ---
# Left Riser (Tail side)
l_riser_pos = -riser_spacing/2
l_riser = (cq.Workplane("YZ")
           .workplane(offset=l_riser_pos)
           .rect(width, riser_height)
           .extrude(thickness)
           .translate((0, 0, riser_height/2)))

# Left Riser Cuts
l_riser = (l_riser.faces(">X").workplane()
           .pushPoints([(0, 25), (0, -25)])
           .slot2D(12, 4, 90) # Vertical slots
           .pushPoints([(25, 0), (-25, 0)])
           .circle(2.5)       # Side holes
           .cutThruAll())

# Right Riser (Front side)
r_riser_pos = riser_spacing/2
r_riser = (cq.Workplane("YZ")
           .workplane(offset=r_riser_pos)
           .rect(width, riser_height)
           .extrude(thickness)
           .translate((0, 0, riser_height/2)))

# Right Riser Cuts (Complex Pattern)
r_riser = (r_riser.faces(">X").workplane()
           .circle(10) # Center large hole
           .rect(30, 30, forConstruction=True).vertices().circle(2.5) # 4 holes in square pattern
           .pushPoints([(0, 32), (0, -32)]).slot2D(12, 4, 90) # Top/Bottom vertical slots
           .pushPoints([(32, 0), (-32, 0)]).slot2D(12, 4, 0)  # Left/Right horizontal slots
           .cutThruAll())

# --- Top Plate ---
top_len = riser_spacing + 30.0 # Slight overhang
top_plate = (cq.Workplane("XY")
             .workplane(offset=riser_height + thickness/2)
             .rect(top_len, width)
             .extrude(thickness))

# Top Plate Cuts
top_plate = (top_plate.faces(">Z").workplane()
             .circle(14) # Large center hole
             .polarArray(24, 0, 360, 4).circle(2.5) # Circular hole pattern
             # Slots for attachment to risers
             .pushPoints([
                 (-riser_spacing/2, 20), (-riser_spacing/2, -20),
                 (riser_spacing/2, 20), (riser_spacing/2, -20)
             ])
             .slot2D(12, 4, 0)
             .cutThruAll())

# --- Gusset ---
# Triangular support for the left riser
# Defined in XZ plane, extruded along Y
pts = [
    (l_riser_pos - thickness/2, 0),                # Bottom-Right (at riser base)
    (l_riser_pos - thickness/2 - gusset_size, 0),  # Bottom-Left
    (l_riser_pos - thickness/2, gusset_size)       # Top-Right
]
gusset = (cq.Workplane("XZ")
          .polyline(pts).close()
          .extrude(10)
          .translate((0, -5, 0)))

# --- Assembly ---
result = base.union(l_riser).union(r_riser).union(top_plate).union(gusset)