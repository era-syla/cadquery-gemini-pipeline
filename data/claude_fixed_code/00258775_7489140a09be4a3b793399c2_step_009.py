import cadquery as cq

# Parameters for the geometry
rod_length = 150.0
rod_radius = 5.0
pin_radius = 0.6
pin_height = 4.0
group_spacing = 30.0
groups_count = 3
pins_per_group = 4

# Helper derived parameters
pin_embed_depth = 1.0  # Depth to embed pin into rod to ensure solid union
pin_total_len = pin_height + pin_embed_depth

# 1. Create the main cylindrical rod
# We align the rod along the X-axis by extruding a circle on the YZ plane.
result = cq.Workplane("YZ").circle(rod_radius).extrude(rod_length, both=True)

# 2. Define the positions for the pin groups along the X-axis
# We center the groups around X=0
x_positions = [
    (i - (groups_count - 1) / 2) * group_spacing 
    for i in range(groups_count)
]

# 3. Create and union the pins
for x in x_positions:
    for i in range(pins_per_group):
        angle = i * (360.0 / pins_per_group)
        
        # Create a single pin
        # Start on XY plane (normal Z), create cylinder, move to surface radius
        pin = (
            cq.Workplane("XY")
            .circle(pin_radius)
            .extrude(pin_total_len)
            .translate((0, 0, rod_radius - pin_embed_depth))
            .rotate((0, 0, 0), (1, 0, 0), angle)
            .translate((x, 0, 0))
        )
        
        # Combine the pin with the main body
        result = result.union(pin)