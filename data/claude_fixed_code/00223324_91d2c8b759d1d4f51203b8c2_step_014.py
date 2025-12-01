import cadquery as cq

# --- Parameters ---
nema_size = 42.3          # Standard NEMA 17 face width
length = 40.0             # Motor body length
corner_chamfer = 4.0      # Corner cut size
boss_dia = 22.0           # Raised boss diameter
boss_height = 2.0         # Boss height
shaft_dia = 5.0           # Output shaft diameter
shaft_len = 24.0          # Shaft length from face
hole_spacing = 31.0       # Mounting hole spacing
hole_dia = 3.0            # Mounting hole diameter (M3)
conn_w = 12.0             # Connector width
conn_h = 17.0             # Connector height
conn_depth = 9.0          # Connector protrusion depth

# --- 1. Main Body Construction ---
# Create the main square prism with chamfered corners
# Extruding along negative Z axis
result = (
    cq.Workplane("XY")
    .rect(nema_size, nema_size)
    .extrude(-length)
    .edges("|Z")
    .chamfer(corner_chamfer)
)

# --- 2. Front Face Features ---
# Add the circular boss
boss = (
    cq.Workplane("XY")
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
)

# Add the shaft
shaft = (
    cq.Workplane("XY")
    .workplane(offset=boss_height)
    .circle(shaft_dia / 2.0)
    .extrude(shaft_len - boss_height)
)
shaft = shaft.faces(">Z").chamfer(0.5)

# Cut mounting holes
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_dia, depth=10.0)
)

# Combine body parts
result = result.union(boss).union(shaft)

# --- 3. Rear Connector ---
# Model the JST-style connector on the side face
# Located on the -X face (Left side), near the rear

# Create the connector housing block
conn_housing = (
    cq.Workplane("YZ")
    .workplane(offset=-nema_size / 2.0)
    .center(0, -length + 9.0)
    .rect(conn_w, conn_h)
    .extrude(-conn_depth)
)

# Create the hollow cavity inside the connector
conn_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-nema_size / 2.0 - conn_depth)
    .center(0, -length + 9.0)
    .rect(conn_w - 2.5, conn_h - 2.5)
    .extrude(conn_depth - 1.5)
)

# Create the pins inside the connector
pins = (
    cq.Workplane("YZ")
    .workplane(offset=-nema_size / 2.0 - conn_depth + 1.5)
    .center(0, -length + 9.0)
    .rarray(1, 2.0, 1, 6)
    .rect(0.64, 0.64)
    .extrude(conn_depth - 2.0)
)

# Combine connector assembly and attach to main body
connector_assembly = conn_housing.cut(conn_cut).union(pins)
result = result.union(connector_assembly)