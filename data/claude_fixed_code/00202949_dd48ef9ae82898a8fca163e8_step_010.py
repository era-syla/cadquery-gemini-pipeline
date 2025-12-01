import cadquery as cq

# --- Parameter Definitions ---
# Estimated based on visual proportions relative to the central hub.
# Hub
hub_width = 10.0         # Width/Length of the central block
hub_height = 12.0        # Height of the central block
hub_chamfer = 2.0        # Chamfer size for vertical edges
bore_diameter = 4.5      # Diameter of the central hole

# Blades
blade_radius = 15.0      # Radius of the circular blades
blade_thickness = 0.8    # Thickness of the blades (thin discs)
blade_dist = 22.0        # Distance from center of hub to center of blade

# Connecting Stems
stem_width = 3.5         # Width of the connector
stem_thickness = 3.0     # Thickness of the connector (thicker than blade for support)
stem_overlap = 2.0       # Overlap into the blade for solid union

# --- Geometry Construction ---

# 1. Create the Central Hub
# A box centered at the origin with chamfered vertical edges and a central bore.
hub = (
    cq.Workplane("XY")
    .box(hub_width, hub_width, hub_height)
    .edges("|Z").chamfer(hub_chamfer)
    .faces(">Z").hole(bore_diameter)
)

# 2. Create a Single Arm (Stem + Blade)
# We construct one arm along the X-axis and then rotate it to create the others.

# Calculate stem dimensions to bridge the gap between hub and blade
# Start stem inside the hub solid (but outside the bore)
stem_start_x = bore_diameter / 2.0 + 1.0 
# End stem slightly inside the blade disc
stem_end_x = blade_dist - blade_radius + stem_overlap
stem_length = stem_end_x - stem_start_x
stem_center_x = stem_start_x + stem_length / 2.0

# Create the Stem geometry
stem = (
    cq.Workplane("XY")
    .rect(stem_length, stem_width)
    .extrude(stem_thickness)
    .translate((stem_center_x, 0, -stem_thickness / 2.0))
)

# Create the Blade geometry
# A cylinder (disc) extruded and centered vertically
blade = (
    cq.Workplane("XY")
    .circle(blade_radius)
    .extrude(blade_thickness)
    .translate((blade_dist, 0, -blade_thickness / 2.0))
)

# Combine Stem and Blade into one object
arm = stem.union(blade)

# 3. Assemble the Object
# Start with the hub and unite the 4 arms rotated by 90 degrees
result = hub
for i in range(4):
    angle = i * 90
    # Rotate the arm around the Z-axis (center 0,0,0)
    rotated_arm = arm.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_arm)

# result is now ready to be displayed or exported