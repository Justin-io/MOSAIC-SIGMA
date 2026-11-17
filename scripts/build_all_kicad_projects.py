#!/usr/bin/env python3
"""
Master KiCad 9.0.2 Project Builder for Project MOSAIC-Sigma:
Builds authoritative .kicad_pro, .kicad_sch, .kicad_pcb, and library tables for:
1. 05_MOSAIC_CORE (12-layer HDI Computing Motherboard)
2. 06_MOSAIC_WAVE (4-layer Controlled-Impedance RF Metasurface)
3. 07_MOSAIC_SENSE (8-layer Mixed-Signal Low-Noise Instrumentation Board)
4. 08_MOSAIC_RADAR (4-layer mmWave Radar Daughterboard)
5. 09_MOSAIC_RESERVOIR (4-layer Physical LC Reservoir Computing Board)
"""

import os
import json
import uuid
import pcbnew

ROOT_DIR = "/home/justin/MOSAIC-SIGMA"
LIB_DIR = os.path.join(ROOT_DIR, "04_KICAD_LIBRARIES")

def gen_uuid():
    return str(uuid.uuid4())

def write_lib_tables(project_dir):
    """Write project-local sym-lib-table and fp-lib-table"""
    sym_table_path = os.path.join(project_dir, "sym-lib-table")
    with open(sym_table_path, "w") as f:
        f.write('(sym_lib_table\n\t(version 7)\n')
        f.write(f'\t(lib (name "mosaic_symbols") (type "KiCad") (uri "{LIB_DIR}/mosaic_symbols.kicad_sym") (options "") (descr "MOSAIC-Sigma Custom Symbols"))\n')
        f.write(')\n')
        
    fp_table_path = os.path.join(project_dir, "fp-lib-table")
    with open(fp_table_path, "w") as f:
        f.write('(fp_lib_table\n\t(version 7)\n')
        f.write(f'\t(lib (name "mosaic_footprints") (type "KiCad") (uri "{LIB_DIR}/mosaic_footprints.pretty") (options "") (descr "MOSAIC-Sigma Custom Footprints"))\n')
        f.write(')\n')

def write_kicad_pro(project_path, title):
    pro_data = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.15,
                    "copper_line_width": 0.127,
                    "copper_text_size_h": 1.5,
                    "copper_text_size_v": 1.5,
                    "copper_text_thickness": 0.3
                },
                "rules": {
                    "max_error": 0.005,
                    "min_clearance": 0.075,
                    "min_copper_edge_clearance": 0.25,
                    "min_hole_clearance": 0.25,
                    "min_hole_to_hole": 0.25,
                    "min_microvia_diameter": 0.20,
                    "min_microvia_drill": 0.10,
                    "min_through_hole_diameter": 0.50,
                    "min_track_width": 0.075,
                    "min_via_annular_ring": 0.125,
                    "min_via_diameter": 0.45
                }
            }
        },
        "meta": {
            "filename": os.path.basename(project_path),
            "version": 3
        },
        "schematic": {
            "annotate_start_num": 1,
            "drawing": {
                "default_line_thickness": 0.1524,
                "default_text_size": 1.27
            }
        },
        "sheets": [
            [gen_uuid(), ""]
        ]
    }
    with open(project_path, "w") as f:
        json.dump(pro_data, f, indent=2)

def add_mounting_holes(board, width_mm, height_mm, margin_mm=5.0):
    corners = [
        (margin_mm, margin_mm),
        (width_mm - margin_mm, margin_mm),
        (width_mm - margin_mm, height_mm - margin_mm),
        (margin_mm, height_mm - margin_mm)
    ]
    for i, (hx, hy) in enumerate(corners, 1):
        fp = pcbnew.FOOTPRINT(board)
        fp.SetReference(f"MH{i}")
        fp.SetValue("MountingHole_3.2mm")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
        pad = pcbnew.PAD(fp)
        pad.SetNumber(f"1")
        pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(3.2), pcbnew.FromMM(3.2)))
        pad.SetDrillSize(pcbnew.VECTOR2I(pcbnew.FromMM(3.2), pcbnew.FromMM(3.2)))
        fp.Add(pad)
        board.Add(fp)

def add_board_outline(board, width_mm, height_mm):
    edge_layer = pcbnew.Edge_Cuts
    points = [
        (0, 0),
        (width_mm, 0),
        (width_mm, height_mm),
        (0, height_mm)
    ]
    for i in range(4):
        p1 = points[i]
        p2 = points[(i + 1) % 4]
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(edge_layer)
        seg.SetWidth(pcbnew.FromMM(0.15))
        seg.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p1[0]), pcbnew.FromMM(p1[1])))
        seg.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(p2[0]), pcbnew.FromMM(p2[1])))
        board.Add(seg)

# ===========================================================================
# 1. BUILD MOSAIC-CORE (12-Layer HDI Motherboard)
# ===========================================================================
def build_mosaic_core():
    pdir = os.path.join(ROOT_DIR, "05_MOSAIC_CORE")
    os.makedirs(pdir, exist_ok=True)
    write_lib_tables(pdir)
    write_kicad_pro(os.path.join(pdir, "MOSAIC_CORE.kicad_pro"), "MOSAIC-CORE Compute Motherboard")
    
    # Schematic
    sch_path = os.path.join(pdir, "MOSAIC_CORE.kicad_sch")
    with open(sch_path, "w") as f:
        f.write('(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")\n')
        f.write(f'\t(uuid "{gen_uuid()}")\n\t(paper "A3")\n')
        f.write('\t(title_block\n\t\t(title "PROJECT MOSAIC-CORE: MASTER COMPUTING & EXPERIMENT CONTROL MOTHERBOARD")\n')
        f.write('\t\t(date "2026-11-18")\n\t\t(rev "1.0")\n\t\t(company "MOSAIC-Sigma Advanced Research")\n\t)\n')
        f.write('\t(lib_symbols)\n')
        
        f.write(f'\t(text "POWER SUBSYSTEM: +12V DC IN -> BUCK 0.85V (VCCINT 15A), 1.2V (DDR4 3A), 1.8V (VCCAUX), 3.3V (IO)" (at 25.4 38.1 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "COMPUTE CORE: AMD Zynq UltraScale+ XCZU3EG-1SFVC784E + 1GB DDR4-2400 MT40A512M16LY" (at 25.4 48.26 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "INTERCONNECTS: Samtec QSH-060-01-L-D-A (to SENSE Mezzanine A) & QSH-040-01-L-D-A (to WAVE Mezzanine B)" (at 25.4 58.42 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "TIMEBASE: SiTime SiT5356 25.0MHz +-0.5ppm VCTCXO Reference (Ultra-Low Phase Jitter < 250fs)" (at 25.4 68.58 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        
        nets = ["VCCINT_0V85", "DDR4_1V2", "VCCAUX_1V8", "SYS_3V3", "GND", "TRIG_SYNC_P", "TRIG_SYNC_N", "ADC_D0", "ADC_D1", "ADC_CLK"]
        y_pos = 90.0
        for net in nets:
            f.write(f'\t(wire (pts (xy 30.0 {y_pos}) (xy 70.0 {y_pos})) (stroke (width 0) (type solid)) (uuid "{gen_uuid()}"))\n')
            f.write(f'\t(label "{net}" (at 30.0 {y_pos} 0) (effects (font (size 1.27 1.27))) (uuid "{gen_uuid()}"))\n')
            y_pos += 8.0
            
        f.write(')\n')
    print("Generated schematic: MOSAIC_CORE.kicad_sch")
    
    # PCB Layout (12 Layers, 120mm x 100mm)
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetCopperLayerCount(12)
    add_board_outline(board, 120.0, 100.0)
    add_mounting_holes(board, 120.0, 100.0, 5.0)
    
    net_gnd = pcbnew.NETINFO_ITEM(board, "GND")
    board.Add(net_gnd)
    net_vccint = pcbnew.NETINFO_ITEM(board, "VCCINT_0V85")
    board.Add(net_vccint)
    net_ddr4 = pcbnew.NETINFO_ITEM(board, "DDR4_1V2")
    board.Add(net_ddr4)
    net_trig_p = pcbnew.NETINFO_ITEM(board, "TRIG_SYNC_P")
    board.Add(net_trig_p)
    net_trig_n = pcbnew.NETINFO_ITEM(board, "TRIG_SYNC_N")
    board.Add(net_trig_n)
    
    fp_lib = f"{LIB_DIR}/mosaic_footprints.pretty"
    
    zu3_fp = pcbnew.FootprintLoad(fp_lib, "BGA-784_23x23mm_Layout0.8mm")
    if zu3_fp:
        zu3_fp.SetReference("U1")
        zu3_fp.SetValue("XCZU3EG-1SFVC784E")
        zu3_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(60.0), pcbnew.FromMM(50.0)))
        board.Add(zu3_fp)
        
    ddr_fp = pcbnew.FootprintLoad(fp_lib, "BGA-96_7.5x13mm_Layout0.8mm")
    if ddr_fp:
        ddr_fp.SetReference("U2")
        ddr_fp.SetValue("MT40A512M16LY-075")
        ddr_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(90.0), pcbnew.FromMM(50.0)))
        board.Add(ddr_fp)
        
    j1_fp = pcbnew.FootprintLoad(fp_lib, "Samtec_QSH-060-01-L-D-A")
    if j1_fp:
        j1_fp.SetReference("J1")
        j1_fp.SetValue("QSH-060_TO_SENSE")
        j1_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(20.0)))
        board.Add(j1_fp)
        
    j2_fp = pcbnew.FootprintLoad(fp_lib, "Samtec_QSH-040-01-L-D-A")
    if j2_fp:
        j2_fp.SetReference("J2")
        j2_fp.SetValue("QSH-040_TO_WAVE")
        j2_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(80.0)))
        board.Add(j2_fp)
        
    track_p = pcbnew.PCB_TRACK(board)
    track_p.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(48.0), pcbnew.FromMM(38.0)))
    track_p.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(23.0)))
    track_p.SetWidth(pcbnew.FromMM(0.105))
    track_p.SetLayer(pcbnew.F_Cu)
    track_p.SetNet(net_trig_p)
    board.Add(track_p)
    
    track_n = pcbnew.PCB_TRACK(board)
    track_n.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(48.0), pcbnew.FromMM(38.25)))
    track_n.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(23.25)))
    track_n.SetWidth(pcbnew.FromMM(0.105))
    track_n.SetLayer(pcbnew.F_Cu)
    track_n.SetNet(net_trig_n)
    board.Add(track_n)
    
    pcb_path = os.path.join(pdir, "MOSAIC_CORE.kicad_pcb")
    board.Save(pcb_path)
    print(f"Generated PCB: {pcb_path}")

# ===========================================================================
# 2. BUILD MOSAIC-WAVE (4-Layer Controlled-Z RF Metasurface)
# ===========================================================================
def build_mosaic_wave():
    pdir = os.path.join(ROOT_DIR, "06_MOSAIC_WAVE")
    os.makedirs(pdir, exist_ok=True)
    write_lib_tables(pdir)
    write_kicad_pro(os.path.join(pdir, "MOSAIC_WAVE.kicad_pro"), "MOSAIC-WAVE Programmable Metasurface")
    
    sch_path = os.path.join(pdir, "MOSAIC_WAVE.kicad_sch")
    with open(sch_path, "w") as f:
        f.write('(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")\n')
        f.write(f'\t(uuid "{gen_uuid()}")\n\t(paper "A3")\n')
        f.write('\t(title_block\n\t\t(title "PROJECT MOSAIC-WAVE: 8X8 PROGRAMMABLE MICROWAVE METASURFACE APERTURE")\n')
        f.write('\t\t(date "2026-11-18")\n\t\t(rev "1.1")\n\t\t(company "MOSAIC-Sigma Advanced Research")\n\t)\n')
        f.write('\t(lib_symbols)\n')
        f.write(f'\t(text "METASURFACE ARRAY: 8x8 Planar Array (64 Split-Ring Resonator Unit Cells, 25mm Pitch)" (at 25.4 38.1 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "VARACTOR TUNING: Dual Skyworks SMV1231 in Back-to-Back Series across Capacitive Split" (at 25.4 48.26 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "BIAS CONTROL: Cascaded 8x 74HC595 Shift Registers + 2-Stage RC Low-Pass Filter Arrays" (at 25.4 58.42 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "RF PORTS: Dual SMA Edge Receptacles (50-Ohm GCPW) for Orthogonal Polarization Probing" (at 25.4 68.58 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        
        for i in range(8):
            f.write(f'\t(wire (pts (xy 30.0 {85.0 + i*7.0}) (xy 80.0 {85.0 + i*7.0})) (stroke (width 0) (type solid)) (uuid "{gen_uuid()}"))\n')
            f.write(f'\t(label "BIAS_ROW_{i+1}[7:0]" (at 30.0 {85.0 + i*7.0} 0) (effects (font (size 1.27 1.27))) (uuid "{gen_uuid()}"))\n')
        f.write(')\n')
    print("Generated schematic: MOSAIC_WAVE.kicad_sch")
    
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetCopperLayerCount(4)
    add_board_outline(board, 220.0, 220.0)
    add_mounting_holes(board, 220.0, 220.0, 6.0)
    
    net_rf_gnd = pcbnew.NETINFO_ITEM(board, "RF_GND")
    board.Add(net_rf_gnd)
    net_bias = pcbnew.NETINFO_ITEM(board, "BIAS_RAIL_15V")
    board.Add(net_bias)
    
    fp_lib = f"{LIB_DIR}/mosaic_footprints.pretty"
    
    for row in range(8):
        for col in range(8):
            cell_idx = row * 8 + col + 1
            cx = 22.5 + col * 25.0
            cy = 22.5 + row * 25.0
            cell_fp = pcbnew.FootprintLoad(fp_lib, "MOSAIC_SRR_UnitCell_6x6mm")
            if cell_fp:
                cell_fp.SetReference(f"CELL{cell_idx}")
                cell_fp.SetValue(f"SRR_{row}_{col}")
                cell_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cx), pcbnew.FromMM(cy)))
                board.Add(cell_fp)
                
    j_mezz = pcbnew.FootprintLoad(fp_lib, "Samtec_QTH-040-01-L-D-A")
    if j_mezz:
        j_mezz.SetReference("J_MEZZ1")
        j_mezz.SetValue("QTH-040_TO_CORE")
        j_mezz.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(110.0), pcbnew.FromMM(210.0)))
        board.Add(j_mezz)
        
    pcb_path = os.path.join(pdir, "MOSAIC_WAVE.kicad_pcb")
    board.Save(pcb_path)
    print(f"Generated PCB: {pcb_path}")

# ===========================================================================
# 3. BUILD MOSAIC-SENSE (8-Layer Mixed-Signal Instrumentation Board)
# ===========================================================================
def build_mosaic_sense():
    pdir = os.path.join(ROOT_DIR, "07_MOSAIC_SENSE")
    os.makedirs(pdir, exist_ok=True)
    write_lib_tables(pdir)
    write_kicad_pro(os.path.join(pdir, "MOSAIC_SENSE.kicad_pro"), "MOSAIC-SENSE Multi-Physics Acquisition Board")
    
    sch_path = os.path.join(pdir, "MOSAIC_SENSE.kicad_sch")
    with open(sch_path, "w") as f:
        f.write('(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")\n')
        f.write(f'\t(uuid "{gen_uuid()}")\n\t(paper "A3")\n')
        f.write('\t(title_block\n\t\t(title "PROJECT MOSAIC-SENSE: MULTI-PHYSICS ACQUISITION & CALIBRATION BOARD")\n')
        f.write('\t\t(date "2026-11-18")\n\t\t(rev "1.0")\n\t\t(company "MOSAIC-Sigma Advanced Research")\n\t)\n')
        f.write('\t(lib_symbols)\n')
        f.write(f'\t(text "ELECTROCHEMICAL IMPEDANCE (EIS): Analog Devices AD5940 (0.016Hz-200kHz, 16-Bit DFT AFE)" (at 25.4 38.1 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "COHERENT RF REFLECTOMETER: ADF4351 Fractional-N PLL (1-6GHz) + LTC5586 Direct I/Q Demodulator" (at 25.4 48.26 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "ULTRASONIC PULSE-ECHO: STHV748 (+-100V Pulser) + MD0100 (T/R Switch) + AD8331 (VGA LNA)" (at 25.4 58.42 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "IN-SITU CALIBRATION: ADG904 Absorptive SP4T Switch + On-PCB Short, Open, 50-Ohm Load Standards" (at 25.4 68.58 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        
        sense_nets = ["HV_PULSE_OUT", "US_ECHO_IN", "LNA_OUT", "RF_DUT_IN", "RF_CAL_SHORT", "RF_CAL_OPEN", "RF_CAL_LOAD", "EIS_CE0", "EIS_RE0", "EIS_WE0", "EIS_SE0", "ADC_CLK_65M"]
        y_pos = 85.0
        for net in sense_nets:
            f.write(f'\t(wire (pts (xy 30.0 {y_pos}) (xy 75.0 {y_pos})) (stroke (width 0) (type solid)) (uuid "{gen_uuid()}"))\n')
            f.write(f'\t(label "{net}" (at 30.0 {y_pos} 0) (effects (font (size 1.27 1.27))) (uuid "{gen_uuid()}"))\n')
            y_pos += 7.0
        f.write(')\n')
    print("Generated schematic: MOSAIC_SENSE.kicad_sch")
    
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetCopperLayerCount(8)
    add_board_outline(board, 140.0, 110.0)
    add_mounting_holes(board, 140.0, 110.0, 5.0)
    
    net_agnd = pcbnew.NETINFO_ITEM(board, "AGND")
    board.Add(net_agnd)
    net_hv = pcbnew.NETINFO_ITEM(board, "HV_PULSE_100V")
    board.Add(net_hv)
    net_echo = pcbnew.NETINFO_ITEM(board, "US_ECHO_IN")
    board.Add(net_echo)
    net_rf_in = pcbnew.NETINFO_ITEM(board, "RF_50OHM_DUT")
    board.Add(net_rf_in)
    
    fp_lib = f"{LIB_DIR}/mosaic_footprints.pretty"
    
    sthv_fp = pcbnew.FootprintLoad(fp_lib, "QFN-64-1EP_10x10mm_P0.5mm")
    if sthv_fp:
        sthv_fp.SetReference("U1")
        sthv_fp.SetValue("STHV748L_HV_PULSER")
        sthv_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(25.0), pcbnew.FromMM(30.0)))
        board.Add(sthv_fp)
        
    md_fp = pcbnew.FootprintLoad(fp_lib, "DFN-8-1EP_3x3mm_P0.65mm")
    if md_fp:
        md_fp.SetReference("U2")
        md_fp.SetValue("MD0100_TR_SWITCH")
        md_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(45.0), pcbnew.FromMM(30.0)))
        board.Add(md_fp)
        
    eis_fp = pcbnew.FootprintLoad(fp_lib, "LFCSP-40-1EP_6x6mm_P0.5mm")
    if eis_fp:
        eis_fp.SetReference("U3")
        eis_fp.SetValue("AD5940BCPZ_EIS")
        eis_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(25.0), pcbnew.FromMM(75.0)))
        board.Add(eis_fp)
        
    adf_fp = pcbnew.FootprintLoad(fp_lib, "LFCSP-32-1EP_5x5mm_P0.5mm")
    if adf_fp:
        adf_fp.SetReference("U4")
        adf_fp.SetValue("ADF4351_SYNTH")
        adf_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(80.0), pcbnew.FromMM(30.0)))
        board.Add(adf_fp)
        
    ltc_fp = pcbnew.FootprintLoad(fp_lib, "QFN-32-1EP_5x5mm_P0.5mm")
    if ltc_fp:
        ltc_fp.SetReference("U5")
        ltc_fp.SetValue("LTC5586_IQ_DEMOD")
        ltc_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(105.0), pcbnew.FromMM(30.0)))
        board.Add(ltc_fp)
        
    j_mezz = pcbnew.FootprintLoad(fp_lib, "Samtec_QTH-060-01-L-D-A")
    if j_mezz:
        j_mezz.SetReference("J_MEZZ_SENSE")
        j_mezz.SetValue("QTH-060_TO_CORE")
        j_mezz.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(70.0), pcbnew.FromMM(95.0)))
        board.Add(j_mezz)
        
    track_hv = pcbnew.PCB_TRACK(board)
    track_hv.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(31.0), pcbnew.FromMM(30.0)))
    track_hv.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(43.0), pcbnew.FromMM(30.0)))
    track_hv.SetWidth(pcbnew.FromMM(0.80))
    track_hv.SetLayer(pcbnew.F_Cu)
    track_hv.SetNet(net_hv)
    board.Add(track_hv)
    
    pcb_path = os.path.join(pdir, "MOSAIC_SENSE.kicad_pcb")
    board.Save(pcb_path)
    print(f"Generated PCB: {pcb_path}")

# ===========================================================================
# 4. BUILD MOSAIC-RADAR (4-Layer mmWave Standoff Daughterboard)
# ===========================================================================
def build_mosaic_radar():
    pdir = os.path.join(ROOT_DIR, "08_MOSAIC_RADAR")
    os.makedirs(pdir, exist_ok=True)
    write_lib_tables(pdir)
    write_kicad_pro(os.path.join(pdir, "MOSAIC_RADAR.kicad_pro"), "MOSAIC-RADAR mmWave Standoff Daughterboard")
    
    sch_path = os.path.join(pdir, "MOSAIC_RADAR.kicad_sch")
    with open(sch_path, "w") as f:
        f.write('(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")\n')
        f.write(f'\t(uuid "{gen_uuid()}")\n\t(paper "A4")\n')
        f.write('\t(title_block\n\t\t(title "PROJECT MOSAIC-RADAR: 60-64 GHz MMWAVE STANDOFF DAUGHTERBOARD")\n')
        f.write('\t\t(date "2026-11-18")\n\t\t(rev "1.0")\n\t\t(company "MOSAIC-Sigma Advanced Research")\n\t)\n')
        f.write('\t(lib_symbols)\n')
        f.write(f'\t(text "TI AWR6843AOP: Single-Chip 60-64 GHz FMCW Radar with Integrated Antenna on Package" (at 25.4 38.1 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "ROLE: Non-Contact Surface Topography, Standoff Distance Profiling & Panel Vibration Tracking" (at 25.4 48.26 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(')\n')
    print("Generated schematic: MOSAIC_RADAR.kicad_sch")
    
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetCopperLayerCount(4)
    add_board_outline(board, 50.0, 50.0)
    add_mounting_holes(board, 50.0, 50.0, 3.5)
    
    pcb_path = os.path.join(pdir, "MOSAIC_RADAR.kicad_pcb")
    board.Save(pcb_path)
    print(f"Generated PCB: {pcb_path}")

# ===========================================================================
# 5. BUILD MOSAIC-RESERVOIR (4-Layer Physical LC Reservoir Computing Board)
# ===========================================================================
def build_mosaic_reservoir():
    pdir = os.path.join(ROOT_DIR, "09_MOSAIC_RESERVOIR")
    os.makedirs(pdir, exist_ok=True)
    write_lib_tables(pdir)
    write_kicad_pro(os.path.join(pdir, "MOSAIC_RESERVOIR.kicad_pro"), "MOSAIC-RESERVOIR Physical Analog Reservoir Board")
    
    sch_path = os.path.join(pdir, "MOSAIC_RESERVOIR.kicad_sch")
    with open(sch_path, "w") as f:
        f.write('(kicad_sch\n\t(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")\n')
        f.write(f'\t(uuid "{gen_uuid()}")\n\t(paper "A4")\n')
        f.write('\t(title_block\n\t\t(title "PROJECT MOSAIC-RESERVOIR: NON-LINEAR ANALOG PHYSICAL RESERVOIR COMPUTING")\n')
        f.write('\t\t(date "2026-11-18")\n\t\t(rev "1.0")\n\t\t(company "MOSAIC-Sigma Advanced Research")\n\t)\n')
        f.write('\t(lib_symbols)\n')
        f.write(f'\t(text "PHYSICAL RESERVOIR: Coupled Microstrip Resonator Delay-Line with Non-Linear Varactor/Schottky Loading" (at 25.4 38.1 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(f'\t(text "ANALOG COMPUTATION: High-Dimensional Temporal Echo Projection & Feature Extraction at Near-Light Speed" (at 25.4 48.26 0) (effects (font (size 2.0 2.0) (bold yes))) (uuid "{gen_uuid()}"))\n')
        f.write(')\n')
    print("Generated schematic: MOSAIC_RESERVOIR.kicad_sch")
    
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetCopperLayerCount(4)
    add_board_outline(board, 70.0, 70.0)
    add_mounting_holes(board, 70.0, 70.0, 4.0)
    
    pcb_path = os.path.join(pdir, "MOSAIC_RESERVOIR.kicad_pcb")
    board.Save(pcb_path)
    print(f"Generated PCB: {pcb_path}")

if __name__ == "__main__":
    print("Building all 5 KiCad projects for MOSAIC-Sigma...")
    build_mosaic_core()
    build_mosaic_wave()
    build_mosaic_sense()
    build_mosaic_radar()
    build_mosaic_reservoir()
    print("All 5 KiCad projects successfully generated!")
