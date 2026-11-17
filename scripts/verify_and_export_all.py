#!/usr/bin/env python3
"""
Automated DRC, ERC, Gerber, NC Drill, and 3D Visualization Pipeline
for all 5 Project MOSAIC-Sigma boards using KiCad 9.0.2 CLI.
"""

import os
import subprocess

ROOT_DIR = "/home/justin/MOSAIC-SIGMA"
BOARDS = [
    ("05_MOSAIC_CORE", "MOSAIC_CORE"),
    ("06_MOSAIC_WAVE", "MOSAIC_WAVE"),
    ("07_MOSAIC_SENSE", "MOSAIC_SENSE"),
    ("08_MOSAIC_RADAR", "MOSAIC_RADAR"),
    ("09_MOSAIC_RESERVOIR", "MOSAIC_RESERVOIR")
]

GERBER_OUT_BASE = os.path.join(ROOT_DIR, "15_GERBER_OUTPUTS")
RENDER_OUT_BASE = os.path.join(ROOT_DIR, "16_3D_VISUALIZATION")
os.makedirs(GERBER_OUT_BASE, exist_ok=True)
os.makedirs(RENDER_OUT_BASE, exist_ok=True)

def run_cmd(cmd, desc):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAIL] {desc}: {res.stderr.strip() or res.stdout.strip()}")
        return False
    print(f"[PASS] {desc}")
    return True

def process_board(bdir_name, bname):
    print(f"\n=======================================================")
    print(f"PROCESSING: {bname} ({bdir_name})")
    print(f"=======================================================")
    bdir = os.path.join(ROOT_DIR, bdir_name)
    pcb_file = os.path.join(bdir, f"{bname}.kicad_pcb")
    sch_file = os.path.join(bdir, f"{bname}.kicad_sch")
    
    # 1. ERC
    erc_rpt = os.path.join(bdir, f"{bname}_erc.rpt")
    run_cmd(f"kicad-cli sch erc --output {erc_rpt} {sch_file}", f"ERC for {bname}")
    
    # 2. DRC
    drc_rpt = os.path.join(bdir, f"{bname}_drc.rpt")
    run_cmd(f"kicad-cli pcb drc --output {drc_rpt} {pcb_file}", f"DRC for {bname}")
    
    # 3. 3D Renders (Top View & Bottom View)
    render_top = os.path.join(RENDER_OUT_BASE, f"{bname}_3D_TOP.png")
    render_bot = os.path.join(RENDER_OUT_BASE, f"{bname}_3D_BOTTOM.png")
    run_cmd(f"kicad-cli pcb render -o {render_top} --side top {pcb_file}", f"3D Render Top: {bname}")
    run_cmd(f"kicad-cli pcb render -o {render_bot} --side bottom {pcb_file}", f"3D Render Bottom: {bname}")
    
    # 4. Gerbers Export
    gerber_dir = os.path.join(GERBER_OUT_BASE, bname)
    os.makedirs(gerber_dir, exist_ok=True)
    run_cmd(f"kicad-cli pcb export gerbers -o {gerber_dir}/ {pcb_file}", f"Gerber Export: {bname}")
    
    # 5. Drill Export
    drill_dir = os.path.join(gerber_dir, "drill")
    os.makedirs(drill_dir, exist_ok=True)
    run_cmd(f"kicad-cli pcb export drill -o {drill_dir}/ {pcb_file}", f"NC Drill Export: {bname}")

if __name__ == "__main__":
    for bdir_name, bname in BOARDS:
        process_board(bdir_name, bname)
    print("\nAll 5 boards processed through ERC, DRC, 3D Render, Gerbers, and NC Drill!")
