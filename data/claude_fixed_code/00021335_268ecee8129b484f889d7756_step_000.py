import cadquery as cq

# Parameter definitions based on visual analysis of the image
# The shape is a "spherical bead": a sphere with truncated poles (flat sides) and a through-hole.
sphere_radius = 15.0
thickness = 18.0
hole_diameter = 10.0

# Generate the 3D object
result = (
    cq.Workplane("XY")
    # 1. Create the base sphere geometry
    .sphere(sphere_radius)
    # 2. Create the flat sides by intersecting the sphere with a box of defined thickness.
    #    The box is centered at the origin, effectively slicing off the top and bottom of the sphere
    #    beyond Z = +/- (thickness / 2).
    .intersect(
        cq.Workplane("XY").box(sphere_radius * 2.5, sphere_radius * 2.5, thickness)
    )
    # 3. Create the central cylindrical hole.
    #    Create a new workplane and drill through.
)

result = result.faces(">Z").workplane().circle(hole_diameter / 2).cutThruAll()