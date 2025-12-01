import cadquery as cq

# --- Parameters ---
cyl_diam = 20.0       # Diameter of the main gas spring body
cyl_length = 120.0    # Length of the main body
rod_diam = 8.0        # Diameter of the piston rod
rod_length = 110.0    # Extended length of the rod
eyelet_od = 16.0      # Outer diameter of the mounting eyelets
eyelet_id = 6.0       # Hole diameter
eyelet_width = 8.0    # Thickness of the eyelet ring
neck_height = 8.0     # Height of the transition neck
bracket_width = 30.0  # Width of the top bracket plate (X)
bracket_depth = 22.0  # Depth of the top bracket plate (Y)
plate_thick = 2.0     # Thickness of sheet metal parts
pin_diam = 6.0        # Diameter of the pivot pin

# --- 1. Main Cylinder Body ---
# Create the main cylinder aligned with the Z axis
body = cq.Workplane("XY").circle(cyl_diam / 2).extrude(cyl_length)

# Add a slight chamfer to the bottom edge of the body
body = body.faces("<Z").chamfer(1.0)

# --- 2. Piston Rod ---
# Extrude the rod from the top face of the body
rod = cq.Workplane("XY", origin=(0, 0, cyl_length)).circle(rod_diam / 2).extrude(rod_length)

# --- 3. Bottom Mount (Eyelet) ---
# Create a neck transition at the bottom
bottom_neck = (
    cq.Workplane("XY", origin=(0, 0, -neck_height))
    .circle(cyl_diam / 2 * 0.6)
    .extrude(neck_height)
)

# Calculate center Z for the bottom eyelet
# It sits below the neck
bottom_eyelet_z = -neck_height - (eyelet_od / 2)

# Create the eyelet ring
# Oriented so the hole axis is along Y (Sketch on XZ plane)
bottom_eyelet = (
    cq.Workplane("XZ", origin=(0, 0, bottom_eyelet_z))
    .circle(eyelet_od / 2)
    .extrude(eyelet_width, both=True)
)

# Cut the mounting hole
bottom_eyelet = bottom_eyelet.faces(">Y").workplane().circle(eyelet_id / 2).cutThruAll()

# --- 4. Top Mount (Rod End Eyelet) ---
# Top of rod Z coordinate
top_z = cyl_length + rod_length

# Neck transition for the rod end
top_neck = (
    cq.Workplane("XY", origin=(0, 0, top_z))
    .circle(rod_diam)
    .extrude(neck_height)
)

# Pivot point Z coordinate for the top assembly
pivot_z = top_z + neck_height + (eyelet_od / 2)

# Create the top eyelet ring (same orientation as bottom)
top_eyelet = (
    cq.Workplane("XZ", origin=(0, 0, pivot_z))
    .circle(eyelet_od / 2)
    .extrude(eyelet_width, both=True)
)
top_eyelet = top_eyelet.faces(">Y").workplane().circle(eyelet_id / 2).cutThruAll()

# --- 5. Top Mounting Bracket ---
# The bracket sits above the top eyelet and holds it with a pin
clearance = 1.0
plate_z = pivot_z + (eyelet_od / 2) + 2.0  # Z height of the top plate underside

# Create the top mounting plate
bracket_plate = (
    cq.Workplane("XY", origin=(0, 0, plate_z))
    .box(bracket_width, bracket_depth, plate_thick, centered=(True, True, False))
)

# Define the shape of the side flanges (trapezoidal/triangular gussets)
# Points are relative to the pivot center in the XZ plane
flange_pts = [
    (-bracket_width / 2, plate_z - pivot_z),   # Top Left (at plate interface)
    (bracket_width / 2, plate_z - pivot_z),    # Top Right
    (pin_diam, -pin_diam),                     # Bottom Right (near pin)
    (-pin_diam, -pin_diam)                     # Bottom Left
]

# Calculate offset for flanges to sandwich the eyelet
# Gap = eyelet width + clearance on both sides
flange_offset = (eyelet_width / 2) + clearance

# Create Right Flange (Extrude outward in +Y)
right_flange = (
    cq.Workplane("XZ", origin=(0, flange_offset, pivot_z))
    .polyline(flange_pts)
    .close()
    .extrude(plate_thick)
)

# Create Left Flange (Extrude outward in -Y)
left_flange = (
    cq.Workplane("XZ", origin=(0, -flange_offset, pivot_z))
    .polyline(flange_pts)
    .close()
    .extrude(-plate_thick)
)

# --- 6. Pivot Pin ---
# A pin running through the bracket ears and the top eyelet
pin = (
    cq.Workplane("XZ", origin=(0, 0, pivot_z))
    .circle(pin_diam / 2)
    .extrude(bracket_depth + 2.0, both=True)  # Slightly wider than the bracket
)

# --- Combine All Parts ---
result = (
    body
    .union(rod)
    .union(bottom_neck)
    .union(bottom_eyelet)
    .union(top_neck)
    .union(top_eyelet)
    .union(bracket_plate)
    .union(right_flange)
    .union(left_flange)
    .union(pin)
)