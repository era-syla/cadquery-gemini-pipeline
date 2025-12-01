import cadquery as cq

# --- Parametric Dimensions ---
# Main Plate
plate_width = 60.0
plate_height = 60.0
plate_thickness = 5.0

# Front Disc (Flywheel)
disc_diameter = 55.0
disc_thickness = 15.0
disc_offset = 35.0  # Gap between plate and disc

# Front Shaft
shaft_size = 10.0
shaft_length = 20.0

# Connecting Rods
rod_diameter = 4.0
rod_spacing = 20.0

# Internal Mechanism (Hub/Motor)
hub_diameter = 10.0
motor_size = 15.0
motor_cyl_diam = 10.0

# Rear Arm
arm_width = 12.0
arm_thickness = 12.0
arm_depth = 30.0    # Length extending back
arm_reach = 35.0    # Length extending sideways
bend_radius = 20.0
flange_width = 20.0
flange_height = 20.0
flange_thick = 3.0

# --- Geometry Construction ---

# 1. Main Square Plate (Centered at origin)
plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Front Disc
# Positioned in front (+Z) of the plate
front_face_z = plate_thickness / 2.0
disc_z_start = front_face_z + disc_offset

disc = (cq.Workplane("XY")
        .workplane(offset=disc_z_start)
        .circle(disc_diameter / 2.0)
        .extrude(disc_thickness)
       )

# 3. Front Square Shaft
# Extrudes from the front face of the disc
front_shaft = (cq.Workplane("XY")
               .workplane(offset=disc_z_start + disc_thickness)
               .rect(shaft_size, shaft_size)
               .extrude(shaft_length)
              )

# 4. Connecting Rods
# Cylinders connecting plate to disc
rod_positions = [
    (rod_spacing, rod_spacing),
    (rod_spacing, -rod_spacing),
    (-rod_spacing, rod_spacing),
    (-rod_spacing, -rod_spacing)
]

rods = (cq.Workplane("XY")
        .workplane(offset=front_face_z)
        .pushPoints(rod_positions)
        .circle(rod_diameter / 2.0)
        .extrude(disc_offset)
       )

# 5. Internal Mechanism (Hub and Motor)
# Central shaft between plate and disc
hub = (cq.Workplane("XY")
       .workplane(offset=front_face_z)
       .circle(hub_diameter / 2.0)
       .extrude(disc_offset)
      )

# Motor block attached to plate
motor_base = (cq.Workplane("XY")
              .workplane(offset=front_face_z)
              .center(0, 10)  # Offset from center
              .rect(motor_size, motor_size)
              .extrude(20)
             )

# Cylinder on motor block
motor_detail = (cq.Workplane("XY")
                .workplane(offset=front_face_z + 20)
                .center(0, 10 + motor_size/2.0)
                .circle(motor_cyl_diam / 2.0)
                .extrude(8)
               )

# 6. Rear Arm
# Sweeps a profile along a curved path behind the plate (-Z)
back_face_z = -plate_thickness / 2.0

# Define the path: Straight back, then bend 90 degrees to the right (+X)
# Path constructed in XZ plane
path = (cq.Workplane("XZ")
        .moveTo(0, back_face_z)
        .lineTo(0, back_face_z - arm_depth)
        .radiusArc((arm_reach, back_face_z - arm_depth), -bend_radius)
       )

# Define the profile on the back of the plate
arm_profile = cq.Workplane("XY").workplane(offset=back_face_z).rect(arm_width, arm_thickness)

# Sweep
arm = arm_profile.sweep(path)

# 7. Rear Flange
# Located at the end of the arm sweep
# Determine coordinates of the arm end
arm_end_x = arm_reach
arm_end_z = back_face_z - arm_depth

# Flange perpendicular to the end of the arm (YZ plane, normal is X)
flange = (cq.Workplane("YZ")
          .workplane(offset=arm_end_x)
          .center(0, arm_end_z)
          .rect(flange_width, flange_height)
          .extrude(flange_thick)
         )

# --- Final Assembly ---
result = (plate
          .union(disc)
          .union(front_shaft)
          .union(rods)
          .union(hub)
          .union(motor_base)
          .union(motor_detail)
          .union(arm)
          .union(flange)
         )