import cadquery as cq

# Analysis of the image:
# The object appears to be a long, slender, symmetrical rod (like a tie rod, tensile specimen, or pin).
# It has a "dogbone" shape with thicker cylindrical sections at the top and bottom,
# transitioning via conical tapers to a much thinner central shaft.
# The cross-section is assumed to be circular (cylindrical) based on the elliptical profiles at the ends.

# Geometric Dimensions (Approximated based on visual aspect ratios)
total_height = 120.0      # Total length of the object
end_diameter = 4.0        # Diameter of the top and bottom heads
shaft_diameter = 1.0      # Diameter of the thin central shaft (approx 1/4 of end diameter)
end_length = 6.0          # Height of the cylindrical part of the ends
taper_length = 4.0        # Height of the conical transition zones

# Derived parameters
r_end = end_diameter / 2.0
r_shaft = shaft_diameter / 2.0

# Define the points for the revolution profile
# We sketch the right half of the cross-section on the XZ plane.
# The local X axis represents the radius, and the local Y axis (Global Z) represents the height.
points = [
    (0, 0),                                             # Center bottom
    (r_end, 0),                                         # Outer bottom edge
    (r_end, end_length),                                # Top of bottom cylinder
    (r_shaft, end_length + taper_length),               # Top of bottom taper (start of shaft)
    (r_shaft, total_height - end_length - taper_length),# Bottom of top taper (end of shaft)
    (r_end, total_height - end_length),                 # Bottom of top cylinder
    (r_end, total_height),                              # Outer top edge
    (0, total_height)                                   # Center top
]

# Create the 3D object
# We draw the profile on the XZ plane and revolve it around the vertical axis (Local Y / Global Z).
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)