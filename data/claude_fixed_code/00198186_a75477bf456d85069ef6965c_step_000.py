import cadquery as cq

# 1. Define geometric parameters based on image analysis
# The object consists of a torus (ring) and a cylinder (handle).
# Estimates based on visual proportions:
ring_major_radius = 10.0   # Distance from center of the ring to the center of the tube
ring_tube_radius = 2.0     # Radius of the tube cross-section
handle_radius = 2.0        # Radius of the handle (appears same as tube)
handle_length = 45.0       # Length of the handle extending from the ring's tube center

# 2. Create the Ring (Torus)
# We draw the circular cross-section on the XZ plane, offset from the Z-axis 
# by the major radius, and revolve it around the Z-axis.
ring = (
    cq.Workplane("XZ")
    .center(ring_major_radius, 0)
    .circle(ring_tube_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# 3. Create the Handle (Cylinder)
# The handle connects to the ring. To ensure a solid connection, we start the 
# extrusion from the center of the ring's tube cross-section (the major radius).
# We create a new workplane on YZ plane and offset it to X = ring_major_radius.
handle = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(handle_radius)
    .extrude(handle_length)
    .translate((ring_major_radius, 0, 0))
)

# 4. Combine the shapes
# Union the ring and the handle to create a single solid object.
result = ring.union(handle)