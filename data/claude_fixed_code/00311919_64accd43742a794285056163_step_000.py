import cadquery as cq

# --- Parameters ---
base_diameter = 20.0
base_length = 40.0
pin_diameter = 8.0
pin_length = 100.0
center_distance = 15.0  # Distance between the center of the base and the center of the pin

# Derived dimensions
base_radius = base_diameter / 2.0
pin_radius = pin_diameter / 2.0

# --- Geometry Construction ---

# 1. Create the base cylinder
# We construct this on the XZ plane and extrude along the Y axis
base = cq.Workplane("XZ").circle(base_radius).extrude(base_length)

# 2. Create the connecting bracket/body
# This part connects the base cylinder to the pin. 
# It has a profile that is rectangular at the bottom (intersecting the base)
# and rounded at the top (matching the pin).
bracket = (
    cq.Workplane("XZ")
    .moveTo(-pin_radius, 0)  # Start inside the base cylinder (at y=0 in sketch coordinates)
    .lineTo(-pin_radius, center_distance)  # Draw vertical side up to pin center height
    .threePointArc((0, center_distance + pin_radius), (pin_radius, center_distance))  # Draw semi-circle top
    .lineTo(pin_radius, 0)  # Draw vertical side down
    .close()  # Close the profile
    .extrude(base_length)
)

# 3. Create the long pin
# This is a cylinder concentric with the top of the bracket but longer
pin = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .moveTo(0, center_distance)
    .circle(pin_radius)
    .extrude(pin_length)
)

# --- Final Assembly ---
# Union all parts together to create a single solid object
result = base.union(bracket).union(pin)