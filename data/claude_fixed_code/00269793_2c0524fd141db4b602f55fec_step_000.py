import cadquery as cq

# ==========================================
# Parameters
# ==========================================
# Overall Dimensions
total_length = 200.0
head_thickness = 6.0
shaft_length = total_length - head_thickness

# Head (Top Plate) Dimensions
head_width = 55.0
head_ext_top = 20.0    # Extension from shaft center to top edge (hammer side)
head_ext_bot = 35.0    # Extension from shaft center to bottom edge (hook side)
corner_radius = 5.0    # Radius of head plate corners
notch_radius = 10.0    # Radius of the rope hook cutout

# Shaft (Spike) Dimensions
shaft_width_top = 16.0
rib_thickness_top = 4.0
shaft_width_tip = 3.0
rib_thickness_tip = 1.5

# Barb (Small Cleats) Dimensions
barb_length = 18.0
barb_r_base = 3.5
barb_r_tip = 1.5
# Position barbs on the "legs" created by the notch
barb_offset_x = 16.0
barb_offset_y = -head_ext_bot + notch_radius + 2.0 

# ==========================================
# Geometry Generation
# ==========================================

# 1. Create the Head Plate
# ------------------------
# Define the main rectangular shape with rounded corners
# Center the coordinates relative to the shaft axis (0,0)
rect_height = head_ext_top + head_ext_bot
y_center = (head_ext_top - head_ext_bot) / 2.0

head = (
    cq.Workplane("XY")
    .rect(head_width, rect_height)
    .extrude(-head_thickness)
)

# Move to center position
head = head.translate((0, y_center, 0))

# Add corner fillets
head = head.edges("|Z").fillet(corner_radius)

# Cut the notch
notch = (
    cq.Workplane("XY")
    .center(0, -head_ext_bot)
    .circle(notch_radius)
    .extrude(-head_thickness)
)

head = head.cut(notch)

# Soften vertical edges
head = head.edges("|Z").fillet(1.0)


# 2. Create the Main Shaft
# ------------------------
# Create cruciform cross-section at top
shaft_top = (
    cq.Workplane("XY")
    .workplane(offset=-head_thickness)
    .rect(shaft_width_top, rib_thickness_top)
    .rect(rib_thickness_top, shaft_width_top)
    .extrude(0.001)
)

# Create cruciform cross-section at tip
shaft_tip = (
    cq.Workplane("XY")
    .workplane(offset=-head_thickness - shaft_length)
    .rect(shaft_width_tip, rib_thickness_tip)
    .rect(rib_thickness_tip, shaft_width_tip)
    .extrude(0.001)
)

# Loft between profiles
shaft = (
    cq.Workplane("XY")
    .workplane(offset=-head_thickness)
    .rect(shaft_width_top, rib_thickness_top)
    .rect(rib_thickness_top, shaft_width_top)
    .workplane(offset=-shaft_length)
    .rect(shaft_width_tip, rib_thickness_tip)
    .rect(rib_thickness_tip, shaft_width_tip)
    .loft()
)


# 3. Create the Barbs
# -------------------
def make_barb(x, y):
    return (
        cq.Workplane("XY")
        .workplane(offset=-head_thickness)
        .center(x, y)
        .circle(barb_r_base)
        .workplane(offset=-barb_length)
        .circle(barb_r_tip)
        .loft()
    )

barb_left = make_barb(-barb_offset_x, barb_offset_y)
barb_right = make_barb(barb_offset_x, barb_offset_y)


# 4. Assembly and Refinement
# --------------------------
# Combine all parts into one solid
result = head.union(shaft).union(barb_left).union(barb_right)