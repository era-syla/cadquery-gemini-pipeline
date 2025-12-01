import cadquery as cq

# --- Dimensions & Parameters ---
# D-Sub DE-9 Right Angle Connector

# Shell (Metal Shield) Dimensions
shell_top_w = 17.0
shell_bot_w = 14.0
shell_height = 10.0
shell_depth = 6.0
shell_fillet = 2.0
shell_thickness = 0.5

# Flange Dimensions
flange_w = 31.0
flange_h = 12.6
flange_thk = 2.0

# Housing / Body Dimensions
housing_w = 16.0
housing_len = 14.5  # Depth behind flange
pcb_offset = 8.5    # Distance from center axis to PCB surface
housing_top_y = flange_h / 2.0
housing_bot_y = -pcb_offset

# Standoffs (Hex Nuts)
standoff_pitch = 25.0
hex_flat = 5.0
hex_len = 4.5
hole_dia = 3.0

# Pins
pin_dia = 1.0
pin_row_spacing = 2.84
pin_pitch = 2.77

# --- Helper Function for D-Profile ---
def d_profile(workplane, w_top, w_bot, h, fillet_r):
    pts = [
        (-w_top/2, h/2),
        (w_top/2, h/2),
        (w_bot/2, -h/2),
        (-w_bot/2, -h/2)
    ]
    return workplane.polyline(pts).close().fillet(fillet_r)

# --- 1. Metal D-Shell ---
# Outer shell shape
shell_wp = cq.Workplane("XY")
shell_outer = d_profile(shell_wp, shell_top_w, shell_bot_w, shell_height, shell_fillet)
shell_solid = shell_outer.extrude(shell_depth)

# Inner cut to make it hollow
inner_w_top = shell_top_w - 2 * shell_thickness
inner_w_bot = shell_bot_w - 2 * shell_thickness
inner_h = shell_height - 2 * shell_thickness
inner_r = shell_fillet - shell_thickness
shell_inner_wp = cq.Workplane("XY")
shell_inner = d_profile(shell_inner_wp, inner_w_top, inner_w_bot, inner_h, inner_r)
shell = shell_solid.cut(shell_inner.extrude(shell_depth))

# Add grounding indents on top
indent_cut = (cq.Workplane("XZ")
              .workplane(offset=shell_height/2)
              .pushPoints([(3, shell_depth/2), (-3, shell_depth/2)])
              .rect(2.5, 2.0)
              .extrude(-0.6)
             )
shell = shell.cut(indent_cut)

# --- 2. Plastic Flange ---
flange = (cq.Workplane("XY")
          .rect(flange_w, flange_h)
          .extrude(-flange_thk)
          .edges("|Z").fillet(0.5)
          )

# --- 3. Rear Housing Body ---
# A block extending from the flange down to the PCB level
h_housing = housing_top_y - housing_bot_y
y_center_housing = housing_bot_y + h_housing / 2.0

housing = (cq.Workplane("XY")
           .workplane(offset=-flange_thk)
           .center(0, y_center_housing)
           .rect(housing_w, h_housing)
           .extrude(-housing_len)
           )
# Add some chamfer to the back for aesthetics
housing = housing.edges("|Y").chamfer(1.0)

# --- 4. Hex Standoffs ---
# Calculate circumscribed diameter for hexagon from flat-to-flat size
circum_dia = (hex_flat / 1.73205) * 2
standoffs_base = (cq.Workplane("XY")
                  .pushPoints([(standoff_pitch/2, 0), (-standoff_pitch/2, 0)])
                  .polygon(6, circum_dia)
                  .extrude(hex_len)
                  )
standoff_holes = (cq.Workplane("XY")
                  .pushPoints([(standoff_pitch/2, 0), (-standoff_pitch/2, 0)])
                  .circle(hole_dia/2)
                  .extrude(hex_len)
                  )
standoffs = standoffs_base.cut(standoff_holes)

# --- 5. Pins ---
pin_locs = []
# Top Row (5 pins)
y1 = pin_row_spacing / 2.0
for i in range(5):
    pin_locs.append(((i - 2) * pin_pitch, y1))
# Bottom Row (4 pins)
y2 = -pin_row_spacing / 2.0
for i in range(4):
    pin_locs.append(((i - 1.5) * pin_pitch, y2))

pins = (cq.Workplane("XY")
        .pushPoints(pin_locs)
        .circle(pin_dia/2)
        .extrude(shell_depth - 1.0)
        .translate((0, 0, -1.0))
        )

# --- 6. Board Locks (Mounting Clips) ---
# Create a single clip object and place it twice
clip_w = 2.0
clip_d = 3.5 # Length front-to-back
clip_h = 4.0 # Extension below housing

clip_geo = (cq.Workplane("XY")
            .rect(clip_w, clip_d)
            .extrude(-clip_h)
            )
# Add a barb/hook at the bottom
clip_barb = (cq.Workplane("XY")
             .workplane(offset=-clip_h + 1.0)
             .rect(clip_w + 0.8, clip_d)
             .extrude(-1.0)
             .faces("<Z").chamfer(0.5)
             )
clip_unit = clip_geo.union(clip_barb)

# Placement coordinates
clip_z = -flange_thk - (housing_len * 0.6)
clip_x = housing_w / 2.0 - 2.5

clip_L = clip_unit.translate((clip_x, housing_bot_y, clip_z))
clip_R = clip_unit.translate((-clip_x, housing_bot_y, clip_z))

# --- Assembly ---
result = (shell
          .union(flange)
          .union(housing)
          .union(standoffs)
          .union(pins)
          .union(clip_L)
          .union(clip_R)
          )