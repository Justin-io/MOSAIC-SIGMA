#!/usr/bin/env python3
"""
Generate VRML 2.0 (.wrl) 3D Models for MOSAIC-Sigma custom footprints.
Enables high-fidelity 3D visualization and mechanical CAD export in KiCad 9.
"""

import os

LIB_DIR = "/home/justin/MOSAIC-SIGMA/04_KICAD_LIBRARIES"
MODELS_DIR = os.path.join(LIB_DIR, "models_3d")
FP_DIR = os.path.join(LIB_DIR, "mosaic_footprints.pretty")
os.makedirs(MODELS_DIR, exist_ok=True)

def write_vrml_chip(filepath, size_x, size_y, height_z, body_color, lid_size=None, lid_color=None):
    with open(filepath, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write("# Project MOSAIC-Sigma 3D Component Model\n")
        f.write("Group {\n  children [\n")
        
        # Substrate/Body
        f.write("    Transform {\n")
        f.write(f"      translation 0.0 0.0 {height_z/2.0:.4f}\n")
        f.write("      children [\n")
        f.write("        Shape {\n")
        f.write("          appearance Appearance {\n")
        f.write(f"            material Material {{ diffuseColor {body_color[0]} {body_color[1]} {body_color[2]} specularColor 0.5 0.5 0.5 shininess 0.3 }}\n")
        f.write("          }\n")
        f.write(f"          geometry Box {{ size {size_x:.4f} {size_y:.4f} {height_z:.4f} }}\n")
        f.write("        }\n")
        f.write("      ]\n    }\n")
        
        # Metallic Lid / Cap if specified
        if lid_size and lid_color:
            lid_h = 0.2
            f.write("    Transform {\n")
            f.write(f"      translation 0.0 0.0 {height_z + lid_h/2.0:.4f}\n")
            f.write("      children [\n")
            f.write("        Shape {\n")
            f.write("          appearance Appearance {\n")
            f.write(f"            material Material {{ diffuseColor {lid_color[0]} {lid_color[1]} {lid_color[2]} specularColor 0.9 0.9 0.9 shininess 0.8 }}\n")
            f.write("          }\n")
            f.write(f"          geometry Box {{ size {lid_size[0]:.4f} {lid_size[1]:.4f} {lid_h:.4f} }}\n")
            f.write("        }\n")
            f.write("      ]\n    }\n")
            
        # Pin 1 Marker (small gold/white sphere)
        f.write("    Transform {\n")
        f.write(f"      translation {-size_x/2.0 + 1.0:.4f} {-size_y/2.0 + 1.0:.4f} {height_z + 0.1:.4f}\n")
        f.write("      children [\n")
        f.write("        Shape {\n")
        f.write("          appearance Appearance {\n")
        f.write("            material Material { diffuseColor 0.9 0.9 0.9 specularColor 1.0 1.0 1.0 shininess 0.9 }\n")
        f.write("          }\n")
        f.write("          geometry Sphere { radius 0.4 }\n")
        f.write("        }\n")
        f.write("      ]\n    }\n")
        
        f.write("  ]\n}\n")

def generate_all_3d_models():
    models = {
        "BGA-784_23x23mm.wrl": (23.0, 23.0, 2.4, (0.1, 0.1, 0.1), (20.0, 20.0), (0.75, 0.75, 0.78)), # XCZU3EG Metal Lid
        "BGA-96_7.5x13mm.wrl": (7.5, 13.0, 1.2, (0.15, 0.15, 0.15), None, None),                    # DDR4 Molded Epoxy
        "QFN-64_10x10mm.wrl": (10.0, 10.0, 0.9, (0.12, 0.12, 0.12), (6.0, 6.0), (0.4, 0.4, 0.4)),   # STHV748
        "LFCSP-40_6x6mm.wrl": (6.0, 6.0, 0.85, (0.15, 0.15, 0.15), None, None),                      # AD5940
        "LFCSP-32_5x5mm.wrl": (5.0, 5.0, 0.85, (0.15, 0.15, 0.15), None, None),                      # ADF4351
        "QFN-32_5x5mm.wrl": (5.0, 5.0, 0.85, (0.15, 0.15, 0.15), None, None),                        # LTC5586
        "DFN-8_3x3mm.wrl": (3.0, 3.0, 0.75, (0.15, 0.15, 0.15), None, None),                         # MD0100
        "Samtec_QSH-060.wrl": (30.0, 7.0, 5.0, (0.05, 0.05, 0.05), (28.0, 2.0), (0.85, 0.75, 0.2)), # High speed connector with gold blade
        "Samtec_QTH-060.wrl": (30.0, 7.0, 4.5, (0.05, 0.05, 0.05), (28.0, 2.0), (0.85, 0.75, 0.2)),
        "Samtec_QSH-040.wrl": (22.0, 7.0, 5.0, (0.05, 0.05, 0.05), (20.0, 2.0), (0.85, 0.75, 0.2)),
        "Samtec_QTH-040.wrl": (22.0, 7.0, 4.5, (0.05, 0.05, 0.05), (20.0, 2.0), (0.85, 0.75, 0.2)),
        "MOSAIC_SRR_6x6mm.wrl": (6.0, 6.0, 0.35, (0.85, 0.72, 0.25), (1.5, 0.8), (0.2, 0.2, 0.2))   # Copper SRR with SMD varactor
    }
    
    for filename, (sx, sy, sz, b_col, l_sz, l_col) in models.items():
        path = os.path.join(MODELS_DIR, filename)
        write_vrml_chip(path, sx, sy, sz, b_col, l_sz, l_col)
        print(f"Generated 3D Model: {filename}")

if __name__ == "__main__":
    generate_all_3d_models()
