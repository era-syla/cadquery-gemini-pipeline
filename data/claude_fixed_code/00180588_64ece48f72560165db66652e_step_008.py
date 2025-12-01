import cadquery as cq

# The object is a stepped pin/plunger consisting of three cylindrical sections:
# 1. A long main shaft
# 2. A collar/flange
# 3. A shorter top shaft with a rounded end
# The entire assembly is rotationally symmetric. We will construct it by stacking
# extrusions along the Z-axis and applying fillets to the ends.

# --- Dimensions (Estimated from visual proportions) ---
long_shaft_diam = 10.0
long_shaft_length = 35.0

collar_diam = 14.0
collar_thickness = 2.5

short_shaft_diam = 8.0
short_shaft_length = 12.0

# --- Construction ---

# 1. Create the main long shaft on the XY plane
result = (
    cq.Workplane("XY")
    .circle(long_shaft_diam / 2.0)
    .extrude(long_shaft_length)
)

# 2. Create the collar
# We select the top face (positive Z direction) of the current solid
# and create a new workplane on it to extrude the next section.
result = (
    result.faces(">Z")
    .workplane()
    .circle(collar_diam / 2.0)
    .extrude(collar_thickness)
)

# 3. Create the short top shaft
# Again, select the top face of the collar and extrude.
result = (
    result.faces(">Z")
    .workplane()
    .circle(short_shaft_diam / 2.0)
    .extrude(short_shaft_length)
)

# --- Finishing Features ---

# 4. Fillet the bottom end (Long shaft start)
# The image shows a rounded transition at the edge of the flat bottom face.
# We select the bottom-most face ("<Z") and apply a fillet to its edges.
result = result.faces("<Z").fillet(2.0)

# 5. Round the top end (Short shaft tip)
# The image shows a hemispherical or fully domed end.
# We select the top-most face (">Z") and fillet its edge.
# Using a radius slightly smaller than the shaft radius creates the dome shape
# while avoiding geometric singularities at the tip.
tip_fillet_radius = (short_shaft_diam / 2.0) - 0.05
result = result.faces(">Z").fillet(tip_fillet_radius)