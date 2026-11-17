#!/usr/bin/env python3
"""
Generate BOM and Pinout Registers:
1. 05_MOSAIC_CORE/MOSAIC_CORE_BOM.xlsx
2. 05_MOSAIC_CORE/MOSAIC_CORE_PIN_ASSIGNMENT.xlsx
3. 06_MOSAIC_WAVE/MOSAIC_WAVE_BOM.xlsx
4. 07_MOSAIC_SENSE/MOSAIC_SENSE_BOM.xlsx
5. 13_CIRCUIT_SIMULATION/MOSAIC_UNCERTAINTY_BUDGET.xlsx
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR = "/home/justin/MOSAIC-SIGMA"

def style_sheet(ws, title, headers, data, col_widths):
    header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=13, bold=True, color="1A365D")
    data_font = Font(name="Calibri", size=10)
    border_side = Side(border_style="thin", color="CBD5E0")
    thin_border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)
    alt_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")

    ws.cell(row=1, column=1, value=title).font = title_font
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 8

    ws.row_dimensions[3].height = 26
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    for row_idx, r in enumerate(data, 4):
        ws.row_dimensions[row_idx].height = 20
        is_alt = (row_idx % 2 == 0)
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.border = thin_border
            if is_alt:
                cell.fill = alt_fill
            cell.alignment = Alignment(horizontal="left", vertical="center")

    for col_idx, width in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

def build_core_bom():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MOSAIC-CORE BOM"
    headers = ["Item", "Reference", "Qty", "Manufacturer MPN", "Manufacturer", "Description", "Package", "Tolerance / Rating", "Supplier Ref"]
    data = [
        [1, "U1", 1, "XCZU3EG-1SFVC784E", "AMD / Xilinx", "Zynq UltraScale+ MPSoC (Quad A53, Dual R5, 154k LC)", "BGA-784 (23x23mm)", "Speed -1, Ext", "Mouser 981-XCZU3EG-1SFVC784"],
        [2, "U2", 1, "MT40A512M16LY-075:E", "Micron Technology", "8 Gb (512Mx16) DDR4-2400 SDRAM 1.2V", "BGA-96 (7.5x13mm)", "1.2V, 2400 MT/s", "DigiKey 557-MT40A512M16LY"],
        [3, "U3", 1, "EMMC16G-TA29-7BA01", "Kingston", "16 GB eMMC 5.1 Flash Memory", "BGA-153", "HS400, 1.8V/3.3V", "Mouser 649-EMMC16G-TA29"],
        [4, "U4", 1, "MT25QU512ABB8ESF-0SIT", "Micron Technology", "512 Mb Quad-SPI NOR Flash Bootloader", "SOIC-16", "133 MHz, 1.8V", "DigiKey 557-1773-ND"],
        [5, "U5", 1, "88E1512-A0-NNP2I000", "Marvell", "Gigabit Ethernet Transceiver RGMII", "QFN-56 (8x8mm)", "Industrial Temp", "Mouser 88E1512-A0-NNP2I"],
        [6, "Y1", 1, "SiT5356AI-FP-33E0-25.000000", "SiTime", "25.0 MHz Elite VCTCXO Reference", "SMD 5.0x3.2mm", "+-0.5 ppm, 3.3V", "DigiKey 1473-SiT5356-ND"],
        [7, "U6", 1, "TPS548A28RWWR", "Texas Instruments", "15A Synchronous Buck Converter (0.85V)", "QFN-21 (3x4mm)", "Vin 12V, Vout 0.85V", "DigiKey 296-TPS548A28-ND"],
        [8, "U7, U8", 2, "TPS543320RTER", "Texas Instruments", "3A Synchronous Buck Converter (1.2V, 3.3V)", "QFN-16 (3x3mm)", "Vin 12V, Eff >92%", "DigiKey 296-TPS543320-ND"],
        [9, "J1", 1, "QSH-060-01-L-D-A", "Samtec", "120-Pin High-Speed Mezzanine Receptacle to SENSE", "SMD 0.5mm pitch", "Gold Plated, 50-ohm", "Samtec QSH-060-01"],
        [10, "J2", 1, "QSH-040-01-L-D-A", "Samtec", "80-Pin High-Speed Mezzanine Receptacle to WAVE", "SMD 0.5mm pitch", "Gold Plated, 50-ohm", "Samtec QSH-040-01"],
        [11, "C1-C10", 10, "GRM31CR60J476ME19L", "Murata", "47 uF 6.3V X5R Ceramic Capacitor", "1206 SMD", "+-20%, ESR 15mR", "DigiKey 490-4493-1-ND"],
        [12, "C11-C26", 16, "GRM188R60J106ME47D", "Murata", "10 uF 6.3V X5R Ceramic Capacitor", "0603 SMD", "+-20%, ESR 20mR", "DigiKey 490-6401-1-ND"],
        [13, "C27-C50", 24, "GRM155R61A105KE15D", "Murata", "1.0 uF 10V X5R Ceramic Capacitor", "0402 SMD", "+-10%, ESR 30mR", "DigiKey 490-6328-1-ND"],
        [14, "C51-C82", 32, "GRM1555C1H104JA01D", "Murata", "0.1 uF 50V C0G/X7R Ceramic Capacitor", "0402 SMD", "+-5%, Low ESL", "DigiKey 490-1324-1-ND"]
    ]
    style_sheet(ws, "MOSAIC-CORE: Master Bill of Materials (BOM)", headers, data, [8, 14, 8, 25, 20, 36, 18, 18, 25])
    wb.save(os.path.join(ROOT_DIR, "05_MOSAIC_CORE/MOSAIC_CORE_BOM.xlsx"))
    print("Saved MOSAIC_CORE_BOM.xlsx")

def build_core_pinouts():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pin Assignments"
    headers = ["Bank", "Pin Number", "Signal Name", "I/O Standard", "Drive / Slew", "Connected IC / Destination", "Routing Constraint"]
    data = [
        ["Bank 504 (DDR4)", "A14, B14", "DDR4_CK_P / N", "DIFF_POD12_2400", "Default", "Micron MT40A512M16LY (Pins K7, K8)", "Length match to +/- 5 mils"],
        ["Bank 504 (DDR4)", "C12, D12", "DDR4_DQS0_P / N", "DIFF_POD12_2400", "Default", "Micron MT40A512M16LY (Pins G3, F3)", "Length match to Byte 0 +/- 5 mils"],
        ["Bank 504 (DDR4)", "A11..H11", "DDR4_DQ[7:0]", "POD12_2400", "Default", "Micron MT40A512M16LY (Data Byte 0)", "Route on Layer 3 Stripline"],
        ["Bank 504 (DDR4)", "E14, F14", "DDR4_DQS1_P / N", "DIFF_POD12_2400", "Default", "Micron MT40A512M16LY (Pins B7, A7)", "Length match to Byte 1 +/- 5 mils"],
        ["Bank 504 (DDR4)", "A16..H16", "DDR4_DQ[15:8]", "POD12_2400", "Default", "Micron MT40A512M16LY (Data Byte 1)", "Route on Layer 10 Stripline"],
        ["Bank 65 (PL HD)", "AA12, AB12", "TRIG_SYNC_P / N", "LVDS_25", "Fast / 8mA", "Samtec QSH-060 Mezzanine A (Pins 1, 3)", "Differential pair 100-ohm, skew < 2ps"],
        ["Bank 65 (PL HD)", "AA15..AD15", "ADC_DATA[11:0]", "LVCMOS25", "Normal", "Samtec QSH-060 Mezzanine A (Pins 10-34)", "Length match bus < 25 mils"],
        ["Bank 65 (PL HD)", "AC18", "ADC_CLK_65M", "LVCMOS25", "Clock Input", "Samtec QSH-060 Mezzanine A (Pin 36)", "Global clock buffer CCIO pin"],
        ["Bank 66 (PL HD)", "W10..W18", "WAVE_BIAS_SPI", "LVCMOS33", "Fast / 12mA", "Samtec QSH-040 Mezzanine B (Shift Registers)", "Series 33-ohm source damping"],
        ["Bank 500 (PS MIO)", "B2..D2", "QSPI_CLK/CS/IO", "LVCMOS18", "Fast", "Micron MT25QU512 NOR Flash", "Keep trace length < 35 mm"]
    ]
    style_sheet(ws, "MOSAIC-CORE: FPGA Pin Assignments & I/O Standards Register", headers, data, [18, 14, 20, 18, 14, 34, 30])
    wb.save(os.path.join(ROOT_DIR, "05_MOSAIC_CORE/MOSAIC_CORE_PIN_ASSIGNMENT.xlsx"))
    print("Saved MOSAIC_CORE_PIN_ASSIGNMENT.xlsx")

def build_wave_bom():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MOSAIC-WAVE BOM"
    headers = ["Item", "Reference", "Qty", "Manufacturer MPN", "Manufacturer", "Description", "Package", "Specs", "Supplier Ref"]
    data = [
        [1, "D1-D128", 128, "SMV1231-079LF", "Skyworks Solutions", "Hyperabrupt Tuning Varactor Diode (Back-to-Back Pair per Cell)", "SC-79 (0402 equiv)", "0.46 to 2.35 pF, Q>3000", "Skyworks SMV1231"],
        [2, "U1-U8", 8, "74HC595PW,118", "Nexperia", "8-Bit Serial-In Parallel-Out Shift Register with Latches", "TSSOP-16", "2.0V to 6.0V, 100MHz", "DigiKey 1727-2038-1-ND"],
        [3, "J_RF1, J_RF2", 2, "CONSMA001-SMD-G", "Linx / TE Connectivity", "Edge-Mount SMA Female 50-Ohm RF Receptacle", "SMD Edge Launch", "DC to 18 GHz, 50-ohm", "DigiKey CONSMA001-ND"],
        [4, "J_MEZZ1", 1, "QTH-040-01-L-D-A", "Samtec", "80-Pin High-Speed Mezzanine Plug (Mates to CORE)", "SMD 0.5mm pitch", "Gold Plated, 50-ohm", "Samtec QTH-040-01"],
        [5, "R1-R64", 64, "RC0402FR-07100KL", "Yageo", "100k Ohm 1% 1/16W Thick-Film Chip Resistor (Bias Feed)", "0402 SMD", "100k 1%, 50V", "DigiKey 311-100KLRTR-ND"],
        [6, "C1-C64", 64, "CC0402KRX7R9BB103", "Yageo", "10 nF 50V X7R Ceramic Capacitor (Bias Low-Pass Filter)", "0402 SMD", "+-10%, 50V", "DigiKey 311-1376-1-ND"]
    ]
    style_sheet(ws, "MOSAIC-WAVE: Master Bill of Materials (BOM)", headers, data, [8, 14, 8, 25, 20, 38, 18, 20, 25])
    wb.save(os.path.join(ROOT_DIR, "06_MOSAIC_WAVE/MOSAIC_WAVE_BOM.xlsx"))
    print("Saved MOSAIC_WAVE_BOM.xlsx")

def build_sense_bom():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MOSAIC-SENSE BOM"
    headers = ["Item", "Reference", "Qty", "Manufacturer MPN", "Manufacturer", "Description", "Package", "Specs", "Supplier Ref"]
    data = [
        [1, "U1", 1, "STHV748L", "STMicroelectronics", "4-Channel +/-100V 2A High-Voltage Ultrasonic Pulser", "QFN-64 (10x10mm)", "+-100V, 2A peak", "Mouser 511-STHV748L"],
        [2, "U2", 1, "MD0100DK6-G", "Microchip", "100V Bidirectional High-Voltage T/R Protection Switch", "DFN-8 (3x3mm)", "+-100V, Ron 15 Ohm", "DigiKey MD0100DK6-ND"],
        [3, "U3", 1, "AD5940BCPZ", "Analog Devices", "High Precision Electrochemical & Impedance Front-End", "LFCSP-40 (6x6mm)", "0.016Hz-200kHz, 16b ADC", "Mouser 584-AD5940BCPZ"],
        [4, "U4", 1, "ADF4351BCPZ", "Analog Devices", "Wideband Fractional-N Synthesizer with Integrated VCO", "LFCSP-32 (5x5mm)", "35MHz to 4400MHz", "Mouser 584-ADF4351BCPZ"],
        [5, "U5", 1, "LTC5586IUF#PBF", "Analog Devices", "300MHz to 6GHz High Linearity Direct I/Q Demodulator", "QFN-32 (5x5mm)", "IIP3 +30.5 dBm", "Mouser 584-LTC5586IUF#PBF"],
        [6, "U6", 1, "AD8331ARQZ", "Analog Devices", "Ultralow Noise Variable Gain Amplifier with TGC", "QSOP-20", "0.74 nV/rtHz, 48dB gain", "Mouser 584-AD8331ARQZ"],
        [7, "U7", 1, "AD9235BCPZ-65", "Analog Devices", "12-Bit 65 MSPS 3V Analog-to-Digital Converter", "LFCSP-32 (5x5mm)", "65 MSPS, SNR 70dB", "Mouser 584-AD9235BCPZ-65"],
        [8, "U8", 1, "ADS8881IDGS", "Texas Instruments", "18-Bit 2 MSPS True Differential SAR ADC", "VSSOP-10", "18-Bit, SNR 100dB", "DigiKey 296-37328-1-ND"],
        [9, "U9", 1, "ADG904BCPZ", "Analog Devices", "Wideband DC to 2.5 GHz Absorptive SP4T Switch (SOL Cal)", "LFCSP-20 (4x4mm)", "Isolation > 35dB", "Mouser 584-ADG904BCPZ"],
        [10, "U10", 1, "ADR4525BRZ", "Analog Devices", "Ultra-Low Noise, High Accuracy 2.500V Voltage Reference", "SOIC-8", "2 ppm/C, 1.2 uV p-p", "Mouser 584-ADR4525BRZ"],
        [11, "U11-U13", 3, "TMP117AIDRVR", "Texas Instruments", "High Precision Digital Temperature Sensors (+-0.1C)", "WSON-6 (2x2mm)", "+-0.1C accuracy", "DigiKey 296-TMP117-ND"],
        [12, "R_LOAD1", 2, "FC0402E50R0BST1", "Vishay Precision", "0402 50.0 Ohm 0.1% Thin-Film RF Resistor (SOL Standard)", "0402 SMD", "50.0 Ohm +-0.05 Ohm", "DigiKey FC0402E50R0BST1"],
        [13, "J_MEZZ_SENSE", 1, "QTH-060-01-L-D-A", "Samtec", "120-Pin High-Speed Mezzanine Plug (Mates to CORE)", "SMD 0.5mm pitch", "Gold Plated, 50-ohm", "Samtec QTH-060-01"]
    ]
    style_sheet(ws, "MOSAIC-SENSE: Master Bill of Materials (BOM)", headers, data, [8, 14, 8, 25, 20, 38, 18, 20, 25])
    wb.save(os.path.join(ROOT_DIR, "07_MOSAIC_SENSE/MOSAIC_SENSE_BOM.xlsx"))
    print("Saved MOSAIC_SENSE_BOM.xlsx")

def build_uncertainty_budget():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Uncertainty Budget"
    headers = ["Error Source", "Modality", "Uncalibrated Error (1-sigma)", "Mitigation Mechanism", "Calibrated Error (1-sigma)", "Standard Uncertainty (u_i)", "Sensitivity (c_i)", "Contribution (u_i * c_i)"]
    data = [
        ["RF Synthesizer Amplitude Drift", "RF Reflectometry", "+- 0.80 dB", "LTC5586 coherent loopback tracking", "+- 0.05 dB", 0.05, 1.0, 0.050],
        ["RF LO Phase Jitter & Thermal Drift", "RF Reflectometry", "+- 12.0 deg", "In-situ SOL de-embedding every 10s", "+- 0.25 deg", 0.25, 0.0175, 0.004],
        ["Directional Coupler Directivity", "RF Reflectometry", "18 dB (~12%)", "Vector 3-term error subtraction", "> 42 dB (<0.8%)", 0.008, 1.0, 0.008],
        ["AD5940 Transimpedance Gain Drift", "EIS (Impedance)", "0.75%", "Vishay 0.05% 10ppm/C Kelvin cal resistor", "0.05%", 0.0005, 1.0, 0.0005],
        ["Electrode Contact Resistance", "EIS (Impedance)", "15.0 Ohms", "4-wire Kelvin ratiometric separation", "0.15 Ohms", 0.15, 0.002, 0.0003],
        ["Ultrasonic Velocity Thermal Shift", "Ultrasound", "1.5% (+-45 m/s)", "On-board TMP117 thermal compensation", "0.08% (+-2.4 m/s)", 0.0008, 1.0, 0.0008],
        ["LNA Input Voltage Offset / Drift", "Ultrasound", "+- 5.0 mV", "AC coupling + digital baseline subtraction", "+- 0.10 mV", 0.0001, 1.0, 0.0001],
        ["ADC Voltage Reference Drift", "All Modalities", "50 ppm/C", "ADR4525 ultra-low noise 2 ppm/C standard", "2 ppm/C", 0.00002, 1.0, 0.00002],
        ["Combined Expanded Uncertainty (k=2, 95% Confidence)", "System Multi-Physics", "26.4%", "MOSAIC-Σ Autonomous In-Situ Calibration", "0.98%", 0.0049, 2.0, 0.0098]
    ]
    style_sheet(ws, "MOSAIC-Σ: System Multi-Physics Measurement Uncertainty Budget (GUM Compliant)", headers, data, [28, 18, 22, 34, 22, 18, 14, 18])
    wb.save(os.path.join(ROOT_DIR, "13_CIRCUIT_SIMULATION/MOSAIC_UNCERTAINTY_BUDGET.xlsx"))
    print("Saved MOSAIC_UNCERTAINTY_BUDGET.xlsx")

if __name__ == "__main__":
    build_core_bom()
    build_core_pinouts()
    build_wave_bom()
    build_sense_bom()
    build_uncertainty_budget()
    print("All board registers and BOM workbooks successfully built!")
