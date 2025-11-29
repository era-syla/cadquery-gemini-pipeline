"""
PartToImage - Render CAD files to PNG images using OCC viewer
Supports .py (CadQuery), .step, and .obj files
"""
import os
import tempfile
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.Graphic3d import Graphic3d_NOM_SILVER
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.DataExchange import read_stl_file
from PIL import Image
import trimesh


def read_python_file(filepath):
    """Read Python file contents"""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def load_step_file(filename: str) -> TopoDS_Shape:
    """Load a STEP file and return the shape"""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status != IFSelect_RetDone:
        raise Exception("Error: Cannot read STEP file.")
    step_reader.TransferRoots()
    shape = step_reader.OneShape()
    return shape


def load_obj_file(filename: str) -> TopoDS_Shape:
    """Load an OBJ file and return a shape"""
    mesh = trimesh.load(filename)
    mesh.export('output.stl')
    shape = read_stl_file('output.stl')
    if shape is None:
        raise Exception(f"Error: Cannot read OBJ file {filename}.")
    return shape


def load_py_file(filename: str) -> TopoDS_Shape:
    """Load a Python file, execute it, and return the shape"""
    code = read_python_file(filename)
    code += "\nimport cadquery as cq\ncq.exporters.export(result, 'output.step')\n"

    # Execute the code
    exec(code)

    return load_step_file('output.step')


def remove_bg(image_path):
    """Remove white background from image"""
    image = Image.open(image_path)
    image = image.convert("RGBA")

    datas = image.getdata()
    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    image.save(image_path, "PNG")


def convert_part_to_image(
    file_name,
    view_type,
    save_path,
    b_rep_name,
    resolution_height=448,
    resolution_width=448,
    rotation_angle=None,
    scale=None,
    remove_bg_flag=False
):
    """
    Convert a CAD file to an image

    Args:
        file_name: Path to .py, .step, or .obj file
        view_type: View angle (iso, front, rear, left, right, top, bottom)
        save_path: Output image path
        b_rep_name: B-rep name (unused, for compatibility)
        resolution_height: Image height
        resolution_width: Image width
        rotation_angle: Optional rotation (unused currently)
        scale: Optional scale (unused currently)
        remove_bg_flag: Whether to remove white background
    """
    # Determine file type and load shape
    file_type = None

    if ".obj" in file_name:
        shape = load_obj_file(file_name)
        file_type = "obj"
    elif ".step" in file_name:
        shape = load_step_file(file_name)
        file_type = "step"
    elif ".py" in file_name:
        shape = load_py_file(file_name)
        file_type = "py"
    else:
        raise ValueError("Unrecognized file type")

    # Initialize the offscreen renderer
    offscreen_renderer = Viewer3d()

    # Set view type
    if view_type == "iso":
        offscreen_renderer.View_Iso()
    elif view_type == "front":
        offscreen_renderer.View_Front()
    elif view_type == "rear":
        offscreen_renderer.View_Rear()
    elif view_type == "left":
        offscreen_renderer.View_Left()
    elif view_type == "right":
        offscreen_renderer.View_Right()
    elif view_type == "top":
        offscreen_renderer.View_Top()
    elif view_type == "bottom":
        offscreen_renderer.View_Bottom()
    else:
        raise Exception("please choose: top, bottom, front, rear, left, right, iso")

    # Create offscreen renderer
    if file_type == "obj":
        offscreen_renderer.Create(draw_face_boundaries=False)
    else:
        offscreen_renderer.Create()

    offscreen_renderer.SetModeShaded()

    # Display the shape with silver material
    offscreen_renderer.DisplayShape(
        shape,
        update=True,
        material=Graphic3d_NOM_SILVER,
        transparency=0.0
    )

    # Set white background
    offscreen_renderer.View.SetBackgroundColor(0, 1, 1, 1)

    # Fit the entire shape in the view
    offscreen_renderer.View.FitAll(0.5)

    # Set resolution
    offscreen_renderer.SetSize(resolution_width, resolution_height)

    # Render and save the image
    offscreen_renderer.View.Dump(save_path)

    # Remove background if requested
    if remove_bg_flag:
        remove_bg(save_path)
