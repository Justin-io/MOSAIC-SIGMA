#!/usr/bin/env python3
"""
Generate official KiCad 9.0.2 symbol and footprint libraries for MOSAIC-Sigma
Includes embedded 3D VRML model linkages for high-fidelity mechanical CAD export.
"""

import os
import uuid

BASE_DIR = "/home/justin/MOSAIC-SIGMA/04_KICAD_LIBRARIES"
FP_DIR = os.path.join(BASE_DIR, "mosaic_footprints.pretty")
os.makedirs(FP_DIR, exist_ok=True)

def gen_uuid():
    return str(uuid.uuid4())

def write_bga_footprint(filename, name, rows, cols, pitch, pad_dia, body_x, body_y, depop=None, model_name=None):
    if depop is None:
        depop = set()
    filepath = os.path.join(FP_DIR, f"{filename}.kicad_mod")
    with open(filepath, "w") as f:
        f.write(f'(footprint "{name}"\n')
        f.write('\t(version 20241229)\n\t(generator "pcbnew")\n\t(generator_version "9.0")\n\t(layer "F.Cu")\n')
        f.write(f'\t(descr "{name} BGA package, pitch {pitch}mm, body {body_x}x{body_y}mm")\n')
        f.write('\t(tags "BGA")\n')
        f.write(f'\t(property "Reference" "REF**" (at 0 {-body_y/2 - 1.5} 0) (layer "F.SilkS") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        f.write(f'\t(property "Value" "{name}" (at 0 {body_y/2 + 1.5} 0) (layer "F.Fab") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        
        f.write(f'\t(fp_rect (start {-body_x/2} {-body_y/2}) (end {body_x/2} {body_y/2}) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_rect (start {-body_x/2 - 0.5} {-body_y/2 - 0.5}) (end {body_x/2 + 0.5} {body_y/2 + 0.5}) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_circle (center {-body_x/2 + 0.8} {-body_y/2 - 0.8}) (end {-body_x/2 + 1.1} {-body_y/2 - 0.8}) (stroke (width 0.15) (type solid)) (fill solid) (layer "F.SilkS") (uuid "{gen_uuid()}"))\n')
        
        row_letters = "ABCDEFGHJKLMNPRTUVWYAAABACADAEAFAGAH"
        start_x = -((cols - 1) * pitch) / 2.0
        start_y = -((rows - 1) * pitch) / 2.0
        
        for r in range(rows):
            r_label = row_letters[r] if r < len(row_letters) else f"R{r+1}"
            for c in range(cols):
                pad_num = f"{r_label}{c+1}"
                if (r, c) in depop:
                    continue
                px = start_x + c * pitch
                py = start_y + r * pitch
                f.write(f'\t(pad "{pad_num}" smd circle (at {px:.4f} {py:.4f}) (size {pad_dia:.3f} {pad_dia:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
                
        if model_name:
            f.write(f'\t(model "${{KIPRJMOD}}/../04_KICAD_LIBRARIES/models_3d/{model_name}"\n')
            f.write('\t\t(offset (xyz 0 0 0))\n\t\t(scale (xyz 1 1 1))\n\t\t(rotate (xyz 0 0 0))\n\t)\n')
        f.write(')\n')

def write_qfn_footprint(filename, name, pins, pitch, body_x, body_y, pad_w, pad_l, ep_x, ep_y, model_name=None):
    filepath = os.path.join(FP_DIR, f"{filename}.kicad_mod")
    with open(filepath, "w") as f:
        f.write(f'(footprint "{name}"\n')
        f.write('\t(version 20241229)\n\t(generator "pcbnew")\n\t(generator_version "9.0")\n\t(layer "F.Cu")\n')
        f.write(f'\t(descr "{name} QFN package, {pins} pins, pitch {pitch}mm, body {body_x}x{body_y}mm")\n')
        f.write(f'\t(property "Reference" "REF**" (at 0 {-body_y/2 - 1.2} 0) (layer "F.SilkS") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        f.write(f'\t(property "Value" "{name}" (at 0 {body_y/2 + 1.2} 0) (layer "F.Fab") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        
        f.write(f'\t(fp_rect (start {-body_x/2} {-body_y/2}) (end {body_x/2} {body_y/2}) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_rect (start {-body_x/2 - 0.5} {-body_y/2 - 0.5}) (end {body_x/2 + 0.5} {body_y/2 + 0.5}) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_circle (center {-body_x/2 + 0.6} {-body_y/2 - 0.6}) (end {-body_x/2 + 0.8} {-body_y/2 - 0.6}) (stroke (width 0.15) (type solid)) (fill solid) (layer "F.SilkS") (uuid "{gen_uuid()}"))\n')
        
        if ep_x > 0 and ep_y > 0:
            f.write(f'\t(pad "{pins+1}" smd rect (at 0 0) (size {ep_x:.3f} {ep_y:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        pins_per_side = pins // 4
        start_y = -((pins_per_side - 1) * pitch) / 2.0
        for i in range(pins_per_side):
            pnum = str(i + 1)
            py = start_y + i * pitch
            px = -body_x / 2.0
            f.write(f'\t(pad "{pnum}" smd rect (at {px:.4f} {py:.4f}) (size {pad_l:.3f} {pad_w:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        start_x = -((pins_per_side - 1) * pitch) / 2.0
        for i in range(pins_per_side):
            pnum = str(pins_per_side + i + 1)
            px = start_x + i * pitch
            py = body_y / 2.0
            f.write(f'\t(pad "{pnum}" smd rect (at {px:.4f} {py:.4f}) (size {pad_w:.3f} {pad_l:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        start_y = ((pins_per_side - 1) * pitch) / 2.0
        for i in range(pins_per_side):
            pnum = str(2 * pins_per_side + i + 1)
            py = start_y - i * pitch
            px = body_x / 2.0
            f.write(f'\t(pad "{pnum}" smd rect (at {px:.4f} {py:.4f}) (size {pad_l:.3f} {pad_w:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        start_x = ((pins_per_side - 1) * pitch) / 2.0
        for i in range(pins_per_side):
            pnum = str(3 * pins_per_side + i + 1)
            px = start_x - i * pitch
            py = -body_y / 2.0
            f.write(f'\t(pad "{pnum}" smd rect (at {px:.4f} {py:.4f}) (size {pad_w:.3f} {pad_l:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        if model_name:
            f.write(f'\t(model "${{KIPRJMOD}}/../04_KICAD_LIBRARIES/models_3d/{model_name}"\n')
            f.write('\t\t(offset (xyz 0 0 0))\n\t\t(scale (xyz 1 1 1))\n\t\t(rotate (xyz 0 0 0))\n\t)\n')
        f.write(')\n')

def write_mezzanine_footprint(filename, name, pins, pitch, row_spacing, model_name=None):
    filepath = os.path.join(FP_DIR, f"{filename}.kicad_mod")
    with open(filepath, "w") as f:
        f.write(f'(footprint "{name}"\n')
        f.write('\t(version 20241229)\n\t(generator "pcbnew")\n\t(generator_version "9.0")\n\t(layer "F.Cu")\n')
        f.write(f'\t(descr "{name} Mezzanine Connector, {pins} pins, pitch {pitch}mm")\n')
        f.write(f'\t(property "Reference" "REF**" (at 0 {-5} 0) (layer "F.SilkS") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        f.write(f'\t(property "Value" "{name}" (at 0 {5} 0) (layer "F.Fab") (uuid "{gen_uuid()}") (effects (font (size 1 1) (thickness 0.15))))\n')
        
        pins_per_row = pins // 2
        start_x = -((pins_per_row - 1) * pitch) / 2.0
        body_len = (pins_per_row * pitch) + 4.0
        
        f.write(f'\t(fp_rect (start {-body_len/2} {-2.5}) (end {body_len/2} {2.5}) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G1" smd rect (at {-body_len/4} 0) (size 8.0 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G2" smd rect (at {body_len/4} 0) (size 8.0 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
        
        for i in range(pins_per_row):
            px = start_x + i * pitch
            f.write(f'\t(pad "{2*i+1}" smd rect (at {px:.4f} {-row_spacing/2:.4f}) (size 0.30 1.20) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            f.write(f'\t(pad "{2*i+2}" smd rect (at {px:.4f} {row_spacing/2:.4f}) (size 0.30 1.20) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
            
        if model_name:
            f.write(f'\t(model "${{KIPRJMOD}}/../04_KICAD_LIBRARIES/models_3d/{model_name}"\n')
            f.write('\t\t(offset (xyz 0 0 0))\n\t\t(scale (xyz 1 1 1))\n\t\t(rotate (xyz 0 0 0))\n\t)\n')
        f.write(')\n')

def write_unit_cell_footprint():
    filepath = os.path.join(FP_DIR, "MOSAIC_SRR_UnitCell_6x6mm.kicad_mod")
    with open(filepath, "w") as f:
        f.write('(footprint "MOSAIC_SRR_UnitCell_6x6mm"\n')
        f.write('\t(version 20241229)\n\t(generator "pcbnew")\n\t(generator_version "9.0")\n\t(layer "F.Cu")\n')
        f.write('\t(descr "MOSAIC-WAVE Split-Ring Resonator Unit Cell (6x6mm)")\n')
        f.write(f'\t(property "Reference" "REF**" (at 0 -4.5 0) (layer "F.SilkS") (uuid "{gen_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))\n')
        f.write(f'\t(property "Value" "SRR_CELL" (at 0 4.5 0) (layer "F.Fab") (uuid "{gen_uuid()}") (effects (font (size 0.8 0.8) (thickness 0.12))))\n')
        
        f.write(f'\t(fp_line (start -3.0 -3.0) (end 3.0 -3.0) (stroke (width 1.0) (type solid)) (layer "F.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_line (start 3.0 -3.0) (end 3.0 3.0) (stroke (width 1.0) (type solid)) (layer "F.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_line (start 3.0 3.0) (end -3.0 3.0) (stroke (width 1.0) (type solid)) (layer "F.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_line (start -3.0 3.0) (end -3.0 0.8) (stroke (width 1.0) (type solid)) (layer "F.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(fp_line (start -3.0 -3.0) (end -3.0 -0.8) (stroke (width 1.0) (type solid)) (layer "F.Cu") (uuid "{gen_uuid()}"))\n')
        
        f.write(f'\t(pad "A1" smd rect (at -3.0 -1.0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "K_MID" smd rect (at -3.0 0.0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "A2" smd rect (at -3.0 1.0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "BIAS" thru_hole circle (at -1.8 0.0) (size 0.6 0.6) (drill 0.3) (layers "*.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G1" thru_hole circle (at -4.5 -4.5) (size 0.6 0.6) (drill 0.3) (layers "*.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G2" thru_hole circle (at 4.5 -4.5) (size 0.6 0.6) (drill 0.3) (layers "*.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G3" thru_hole circle (at 4.5 4.5) (size 0.6 0.6) (drill 0.3) (layers "*.Cu") (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(pad "G4" thru_hole circle (at -4.5 4.5) (size 0.6 0.6) (drill 0.3) (layers "*.Cu") (uuid "{gen_uuid()}"))\n')
        
        f.write('\t(model "${KIPRJMOD}/../04_KICAD_LIBRARIES/models_3d/MOSAIC_SRR_6x6mm.wrl"\n')
        f.write('\t\t(offset (xyz 0 0 0))\n\t\t(scale (xyz 1 1 1))\n\t\t(rotate (xyz 0 0 0))\n\t)\n')
        f.write(')\n')

def generate_all_footprints():
    depop_zu3 = set()
    for r in range(9, 19):
        for c in range(9, 19):
            depop_zu3.add((r, c))
    write_bga_footprint("BGA-784_23x23mm_Layout0.8mm", "BGA-784_23x23mm_Layout0.8mm", 28, 28, 0.8, 0.40, 23.0, 23.0, depop_zu3, "BGA-784_23x23mm.wrl")
    
    depop_ddr = set()
    for r in range(16):
        for c in [3, 4, 5]:
            depop_ddr.add((r, c))
    write_bga_footprint("BGA-96_7.5x13mm_Layout0.8mm", "BGA-96_7.5x13mm_Layout0.8mm", 16, 9, 0.8, 0.42, 7.5, 13.0, depop_ddr, "BGA-96_7.5x13mm.wrl")
    
    write_qfn_footprint("QFN-64-1EP_10x10mm_P0.5mm", "QFN-64-1EP_10x10mm_P0.5mm", 64, 0.5, 10.0, 10.0, 0.28, 0.85, 7.5, 7.5, "QFN-64_10x10mm.wrl")
    write_qfn_footprint("LFCSP-40-1EP_6x6mm_P0.5mm", "LFCSP-40-1EP_6x6mm_P0.5mm", 40, 0.5, 6.0, 6.0, 0.28, 0.80, 4.3, 4.3, "LFCSP-40_6x6mm.wrl")
    write_qfn_footprint("LFCSP-32-1EP_5x5mm_P0.5mm", "LFCSP-32-1EP_5x5mm_P0.5mm", 32, 0.5, 5.0, 5.0, 0.28, 0.75, 3.2, 3.2, "LFCSP-32_5x5mm.wrl")
    write_qfn_footprint("QFN-32-1EP_5x5mm_P0.5mm", "QFN-32-1EP_5x5mm_P0.5mm", 32, 0.5, 5.0, 5.0, 0.28, 0.75, 3.4, 3.4, "QFN-32_5x5mm.wrl")
    write_qfn_footprint("DFN-8-1EP_3x3mm_P0.65mm", "DFN-8-1EP_3x3mm_P0.65mm", 8, 0.65, 3.0, 3.0, 0.35, 0.70, 2.4, 1.7, "DFN-8_3x3mm.wrl")
    
    write_mezzanine_footprint("Samtec_QSH-060-01-L-D-A", "Samtec_QSH-060-01-L-D-A", 120, 0.5, 3.8, "Samtec_QSH-060.wrl")
    write_mezzanine_footprint("Samtec_QTH-060-01-L-D-A", "Samtec_QTH-060-01-L-D-A", 120, 0.5, 3.8, "Samtec_QTH-060.wrl")
    write_mezzanine_footprint("Samtec_QSH-040-01-L-D-A", "Samtec_QSH-040-01-L-D-A", 80, 0.5, 3.8, "Samtec_QSH-040.wrl")
    write_mezzanine_footprint("Samtec_QTH-040-01-L-D-A", "Samtec_QTH-040-01-L-D-A", 80, 0.5, 3.8, "Samtec_QTH-040.wrl")
    
    write_unit_cell_footprint()

def write_symbol_library():
    sym_file = os.path.join(BASE_DIR, "mosaic_symbols.kicad_sym")
    with open(sym_file, "w") as f:
        f.write('(kicad_symbol_lib\n\t(version 20241209)\n\t(generator "kicad_symbol_editor")\n\t(generator_version "9.0")\n')
        
        # 1. XCZU3EG-1SFVC784E
        f.write('\t(symbol "XCZU3EG-1SFVC784E"\n\t\t(pin_names (offset 1.016))\n\t\t(in_bom yes)\n\t\t(on_board yes)\n')
        f.write('\t\t(property "Reference" "U" (at 0 25.4 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Value" "XCZU3EG-1SFVC784E" (at 0 -25.4 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Footprint" "mosaic_footprints:BGA-784_23x23mm_Layout0.8mm" (at 0 -27.94 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Datasheet" "https://docs.amd.com/v/u/en-US/ds891-zynq-ultrascale-plus-overview" (at 0 -30.48 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Description" "AMD Zynq UltraScale+ MPSoC (Quad A53, Dual R5, 154k LC)" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(symbol "XCZU3EG-1SFVC784E_1_1"\n')
        f.write('\t\t\t(rectangle (start -20.32 22.86) (end 20.32 -22.86) (stroke (width 0.254) (type solid)) (fill (type background)))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 17.78 0) (length 5.08) (name "VCCINT" (effects (font (size 1.0 1.0)))) (number "VCCINT" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 12.70 0) (length 5.08) (name "VCC_PSINTFP" (effects (font (size 1.0 1.0)))) (number "VCC_FP" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 7.62 0) (length 5.08) (name "VCC_PSINTLP" (effects (font (size 1.0 1.0)))) (number "VCC_LP" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 2.54 0) (length 5.08) (name "VCCAUX" (effects (font (size 1.0 1.0)))) (number "VCCAUX" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 -2.54 0) (length 5.08) (name "VCCO_PSDDR" (effects (font (size 1.0 1.0)))) (number "VCCO_DDR" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -25.4 -7.62 0) (length 5.08) (name "GND" (effects (font (size 1.0 1.0)))) (number "GND" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at -25.4 -15.24 0) (length 5.08) (name "PS_CLK" (effects (font (size 1.0 1.0)))) (number "PS_CLK" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin bidirectional line (at 25.4 17.78 180) (length 5.08) (name "DDR4_BUS" (effects (font (size 1.0 1.0)))) (number "DDR4" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin output line (at 25.4 10.16 180) (length 5.08) (name "TRIG_OUT" (effects (font (size 1.0 1.0)))) (number "TRIG" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at 25.4 2.54 180) (length 5.08) (name "ADC_DATA[11:0]" (effects (font (size 1.0 1.0)))) (number "ADC_D" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin bidirectional line (at 25.4 -5.08 180) (length 5.08) (name "SPI_CTRL" (effects (font (size 1.0 1.0)))) (number "SPI" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin bidirectional line (at 25.4 -12.70 180) (length 5.08) (name "ETH_RGMII" (effects (font (size 1.0 1.0)))) (number "ETH" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t)\n\t)\n')
        
        # 2. AD5940BCPZ
        f.write('\t(symbol "AD5940BCPZ"\n\t\t(pin_names (offset 1.016))\n\t\t(in_bom yes)\n\t\t(on_board yes)\n')
        f.write('\t\t(property "Reference" "U" (at 0 20.32 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Value" "AD5940BCPZ" (at 0 -20.32 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Footprint" "mosaic_footprints:LFCSP-40-1EP_6x6mm_P0.5mm" (at 0 -22.86 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Datasheet" "https://www.analog.com/media/en/technical-documentation/data-sheets/ad5940-5941.pdf" (at 0 -25.4 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Description" "High Precision Impedance & Electrochemical Front End" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(symbol "AD5940BCPZ_1_1"\n')
        f.write('\t\t\t(rectangle (start -15.24 17.78) (end 15.24 -17.78) (stroke (width 0.254) (type solid)) (fill (type background)))\n')
        f.write('\t\t\t(pin power_in line (at -20.32 12.7 0) (length 5.08) (name "AVDD" (effects (font (size 1.0 1.0)))) (number "1" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -20.32 7.62 0) (length 5.08) (name "DVDD" (effects (font (size 1.0 1.0)))) (number "2" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -20.32 -12.7 0) (length 5.08) (name "AGND" (effects (font (size 1.0 1.0)))) (number "3" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin output line (at -20.32 0 0) (length 5.08) (name "CE0" (effects (font (size 1.0 1.0)))) (number "20" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at -20.32 -5.08 0) (length 5.08) (name "RE0" (effects (font (size 1.0 1.0)))) (number "21" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at 20.32 -5.08 180) (length 5.08) (name "SE0" (effects (font (size 1.0 1.0)))) (number "22" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at 20.32 0 180) (length 5.08) (name "WE0" (effects (font (size 1.0 1.0)))) (number "23" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin bidirectional line (at 20.32 12.7 180) (length 5.08) (name "SPI_CS_N" (effects (font (size 1.0 1.0)))) (number "35" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin bidirectional line (at 20.32 7.62 180) (length 5.08) (name "SPI_SCLK" (effects (font (size 1.0 1.0)))) (number "36" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t)\n\t)\n')
        
        # 3. STHV748L
        f.write('\t(symbol "STHV748L"\n\t\t(pin_names (offset 1.016))\n\t\t(in_bom yes)\n\t\t(on_board yes)\n')
        f.write('\t\t(property "Reference" "U" (at 0 22.86 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Value" "STHV748L" (at 0 -22.86 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Footprint" "mosaic_footprints:QFN-64-1EP_10x10mm_P0.5mm" (at 0 -25.4 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Datasheet" "https://www.st.com/resource/en/datasheet/sthv748.pdf" (at 0 -27.94 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Description" "4-Channel +/-100V 2A High-Voltage Ultrasonic Pulser" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(symbol "STHV748L_1_1"\n')
        f.write('\t\t\t(rectangle (start -17.78 20.32) (end 17.78 -20.32) (stroke (width 0.254) (type solid)) (fill (type background)))\n')
        f.write('\t\t\t(pin power_in line (at -22.86 15.24 0) (length 5.08) (name "VPP (+100V)" (effects (font (size 1.0 1.0)))) (number "1" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -22.86 -15.24 0) (length 5.08) (name "VNN (-100V)" (effects (font (size 1.0 1.0)))) (number "2" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin power_in line (at -22.86 5.08 0) (length 5.08) (name "VDD (3.3V)" (effects (font (size 1.0 1.0)))) (number "3" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at -22.86 -5.08 0) (length 5.08) (name "IN_POS" (effects (font (size 1.0 1.0)))) (number "10" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin input line (at -22.86 -8.89 0) (length 5.08) (name "IN_NEG" (effects (font (size 1.0 1.0)))) (number "11" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin output line (at 22.86 0 180) (length 5.08) (name "OUT1 (HV_PULSE)" (effects (font (size 1.0 1.0)))) (number "30" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t)\n\t)\n')
        
        # 4. MOSAIC_SRR_UNIT_CELL
        f.write('\t(symbol "MOSAIC_SRR_UNIT_CELL"\n\t\t(pin_names (offset 1.016))\n\t\t(in_bom yes)\n\t\t(on_board yes)\n')
        f.write('\t\t(property "Reference" "CELL" (at 0 10.16 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Value" "SRR_UNIT_CELL" (at 0 -10.16 0) (effects (font (size 1.27 1.27))))\n')
        f.write('\t\t(property "Footprint" "mosaic_footprints:MOSAIC_SRR_UnitCell_6x6mm" (at 0 -12.7 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(property "Description" "Split-Ring Resonator Unit Cell (6x6mm) with Dual Varactor Landing" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n')
        f.write('\t\t(symbol "MOSAIC_SRR_UNIT_CELL_1_1"\n')
        f.write('\t\t\t(circle (center 0 0) (radius 6.35) (stroke (width 0.254) (type solid)) (fill (type background)))\n')
        f.write('\t\t\t(pin input line (at 0 -10.16 90) (length 3.81) (name "BIAS_IN" (effects (font (size 1.0 1.0)))) (number "1" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t\t(pin passive line (at 0 10.16 270) (length 3.81) (name "GND" (effects (font (size 1.0 1.0)))) (number "2" (effects (font (size 1.0 1.0)))))\n')
        f.write('\t\t)\n\t)\n')
        
        f.write(')\n')
    print(f"Generated symbol library: {sym_file}")

if __name__ == "__main__":
    generate_all_footprints()
    write_symbol_library()
    print("All KiCad 9.0 symbol and footprint libraries successfully generated!")
