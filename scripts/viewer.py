#!/usr/bin/env python3
"""
Display tutorial results next to a reference with polyscope.

Examples:
    python scripts/viewer.py cloud data/Buddah.ply output_APSS.ply output_ASO.ply
    python scripts/viewer.py mesh  data/Buddah.ply mesh_APSS.ply
"""
import argparse
from pathlib import Path

import numpy as np
import polyscope as ps
from plyfile import PlyData


def loadPly(path):
    """
        Return (positions, normals, faces) from a ply file.
        normals and faces are None when absent from the file.
    """
    ply = PlyData.read(path)
    vertices = ply["vertex"]

    positions = np.column_stack([vertices["x"], vertices["y"], vertices["z"]])
    normals = None
    faces   = None
        
    if {"nx", "ny", "nz"} <= set(vertices.data.dtype.names):
        normals = np.column_stack([vertices["nx"], vertices["ny"], vertices["nz"]])

    if "face" in ply and len(ply["face"].data) > 0:
        faces = np.vstack(ply["face"].data["vertex_indices"])

    return positions, normals, faces


def registerCloud(name, path):
    """
        Register a ply file as a pointcloud within the viewer
    """
    positions, normals, _ = loadPly(path)
    cloud = ps.register_point_cloud(name, positions)
    if normals is not None:
        cloud.add_vector_quantity("normals", normals, enabled=False)

    return cloud


def registerMesh(name, path):
    """
        Register a ply file as a mesh within the viewer
    """
    positions, normals, faces = loadPly(path)
    if faces is None:
        print(f"warning: {path} has no faces, displaying it as a point cloud")
        return registerCloud(name, path)

    mesh = ps.register_surface_mesh(name, positions, faces)
    if normals is not None:
        mesh.add_vector_quantity("normals", normals, enabled=False)
    return mesh


REGISTER = {
    # Command name: (function, help string)
    "cloud": (registerCloud, "Display inputs as point clouds"),
    "mesh":  (registerMesh, "Display inputs as meshes")
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display tutorial results next to a reference with polyscope")
    commands = parser.add_subparsers(dest="command", required=True)

    for command, (_, help) in REGISTER.items():
        sub = commands.add_parser(command, help=help)
        sub.add_argument("ref", type=Path, help="Reference input (ply)")
        sub.add_argument("inputs", type=Path, nargs="*", help="Results to compare with the reference (ply)")

    args     = parser.parse_args()
    register = REGISTER[args.command][0]

    # Disable some warnings and ini file creating 
    ps.set_verbosity(1)
    ps.set_use_prefs_file(False) 
    ps.init()

    # The reference may be the input cloud of a mesh tutorial: no warning when it has no faces
    register(args.ref.stem, args.ref)
    for path in args.inputs:
        register(path.stem, path)
    
    ps.show()
