#!/usr/bin/env python3
"""
Generate comprehensive COMPONENT_MASTER_REGISTER.xlsx for Project MOSAIC-Sigma
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = "/home/justin/MOSAIC-SIGMA"

def build_component_register():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Master Component Register"
    
    headers = [
        "Component ID", "Target Board", "Manufacturer", "Manufacturer MPN",
        "Functional Description", "Package / Footprint", "Pin Count / Pitch",
        "Primary Supply Rails", "Power Dissipation", "Operating Temp Range",
        "Lifecycle Status", "Critical Design Rule / Constraint"
    ]
    
    components = [
        # MOSAIC-CORE
        ["CMP-COR-001", "MOSAIC-CORE", "AMD / Xilinx", "XCZU3EG-1SFVC784E", 
         "Zynq UltraScale+ MPSoC (Quad A53, Dual R5, 154k LC)", "BGA-784 (SFVC784)", "784 pins / 0.8 mm", 
         "0.85V (VCCINT), 1.2V, 1.8V, 3.3V", "5.2 W typ.", "-40C to +100C", 
         "Active", "Requires 12-layer HDI with dog-bone via fanout, microvias"],
        ["CMP-COR-002", "MOSAIC-CORE", "Micron Technology", "MT40A512M16LY-075:E",
         "8 Gb (512Mx16) DDR4-2400 SDRAM", "BGA-96 (FBGA)", "96 pins / 0.8 mm",
         "1.2V VDD/VDDQ, 2.5V VPP", "650 mW", "-40C to +95C",
         "Active", "Length matching +/- 5 mils within byte lanes, 40-ohm SE / 80-ohm Diff"],
        ["CMP-COR-003", "MOSAIC-CORE", "Kingston", "EMMC16G-TA29-7BA01",
         "16 GB eMMC 5.1 Non-Volatile Flash", "BGA-153", "153 pins / 0.5 mm",
         "1.8V VDD, 3.3V VCCQ", "180 mW", "-40C to +85C",
         "Active", "HS400 interface, 50-ohm trace impedance matched to +/- 20 mils"],
        ["CMP-COR-004", "MOSAIC-CORE", "Micron Technology", "MT25QU512ABB8ESF-0SIT",
         "512 Mb Quad-SPI NOR Flash (Bootloader)", "SOIC-16", "16 pins / 1.27 mm",
         "1.8V VCC", "45 mW", "-40C to +85C",
         "Active", "Keep clock trace short (<30mm), series 22-ohm damping resistor"],
        ["CMP-COR-005", "MOSAIC-CORE", "Marvell", "88E1512-A0-NNP2I000",
         "Integrated 10/100/1000 Mbps Ethernet Transceiver", "QFN-56 (8x8mm)", "56 pins / 0.5 mm",
         "1.0V, 1.8V, 3.3V", "450 mW", "-40C to +85C",
         "Active", "100-ohm diff MDI pairs with center-tapped magnetics RJ45"],
        ["CMP-COR-006", "MOSAIC-CORE", "SiTime", "SiT5356AI-FP-33E0-25.000000",
         "Precision 25.0 MHz +-0.5 ppm Elite VCTCXO Reference", "SMD 5.0x3.2mm", "4 pads / SMD",
         "3.3V VDD", "95 mW", "-40C to +85C",
         "Active", "Place adjacent to FPGA MGT/CLK pins with solid ground plane underneath"],
        ["CMP-COR-007", "MOSAIC-CORE", "Texas Instruments", "TPS548A28RWWR",
         "15A Synchronous Step-Down Converter (VCCINT 0.85V)", "QFN-21 (3x4mm)", "21 pins / 0.5 mm",
         "12V Vin, 0.85V Vout", "1.2 W (at 10A)", "-40C to +125C",
         "Active", "High-frequency ceramic input cap loop < 1mm; output ripple < 10mV"],
        ["CMP-COR-008", "MOSAIC-CORE", "Texas Instruments", "TPS543320RTER",
         "3A Synchronous Step-Down Converter (1.2V & 3.3V)", "QFN-16 (3x3mm)", "16 pins / 0.5 mm",
         "12V Vin, 1.2V / 3.3V Vout", "450 mW", "-40C to +125C",
         "Active", "Separate analog ground and power switch node, shielded inductor"],
        ["CMP-COR-009", "MOSAIC-CORE", "Samtec", "QSH-060-01-L-D-A",
         "120-Pin High-Speed Ground Plane Mezzanine Receptacle", "SMD Mezzanine", "120 pins / 0.5 mm",
         "Passes 3.3V, 5V, Trigger, 65MSPS ADC Bus", "N/A", "-55C to +125C",
         "Active", "50-ohm single-ended / 100-ohm diff matched pinouts, integral ground blade"],
        ["CMP-COR-010", "MOSAIC-CORE", "Samtec", "QSH-040-01-L-D-A",
         "80-Pin High-Speed Mezzanine Receptacle to WAVE", "SMD Mezzanine", "80 pins / 0.5 mm",
         "Passes 3.3V, 15V Bias, SPI, Control", "N/A", "-55C to +125C",
         "Active", "Integrates dedicated 15V varactor supply pins separated by ground pins"],

        # MOSAIC-WAVE
        ["CMP-WAV-001", "MOSAIC-WAVE", "Skyworks Solutions", "SMV1231-079LF",
         "Hyperabrupt Junction Tuning Varactor (0.46 to 2.35 pF)", "SC-79 / SOD-523", "2 pads / SMD",
         "0 to 15V Reverse Bias", "< 1 mW (leakage < 20nA)", "-55C to +125C",
         "Active", "Mount directly across microstrip split-ring gap; series R_bias = 100k"],
        ["CMP-WAV-002", "MOSAIC-WAVE", "Nexperia", "74HC595PW,118",
         "8-Bit Serial-In Parallel-Out Shift Register with Latches", "TSSOP-16", "16 pins / 0.65 mm",
         "5.0V VCC", "20 mW", "-40C to +125C",
         "Active", "Cascaded 8-IC chain driving 64 varactor channels; RC filter at outputs"],
        ["CMP-WAV-003", "MOSAIC-WAVE", "Samtec", "QTH-040-01-L-D-A",
         "80-Pin High-Speed Mezzanine Plug (Mates to CORE)", "SMD Mezzanine", "80 pins / 0.5 mm",
         "Mating connector to QSH-040", "N/A", "-55C to +125C",
         "Active", "Keepout around high-voltage 15V bias lines"],
        ["CMP-WAV-004", "MOSAIC-WAVE", "Linx / TE Connectivity", "CONSMA001-SMD-G",
         "Edge-Mount SMA Female RF Receptacle (50 Ohm)", "Edge Mount SMD", "5 pads / Edge",
         "Up to 18 GHz RF", "N/A", "-65C to +165C",
         "Active", "Coplanar waveguide with ground transition; tapered landing pad for 50-ohm"],

        # MOSAIC-SENSE
        ["CMP-SEN-001", "MOSAIC-SENSE", "Analog Devices", "AD5940BCPZ",
         "High Precision Electrochemical & Impedance Front-End", "LFCSP-40 (6x6mm)", "40 pins / 0.5 mm",
         "2.8V to 3.6V VDD", "15 mW typ.", "-40C to +85C",
         "Active", "Guard ring around CE0, RE0, SE0, WE0 pins; low-leakage PCB wash"],
        ["CMP-SEN-002", "MOSAIC-SENSE", "Analog Devices", "ADF4351BCPZ",
         "Wideband Fractional-N Synthesizer with Integrated VCO (35-4400MHz)", "LFCSP-32 (5x5mm)", "32 pins / 0.5 mm",
         "3.0V to 3.6V VDD, 5.0V Vp", "350 mW", "-40C to +85C",
         "Active", "Differential RF outputs matched to 50-ohm; separate analog PLL ground"],
        ["CMP-SEN-003", "MOSAIC-SENSE", "Analog Devices", "LTC5586IUF#PBF",
         "300MHz to 6GHz High Linearity Direct Conversion I/Q Demodulator", "QFN-32 (5x5mm)", "32 pins / 0.5 mm",
         "5.0V VCC", "1.2 W", "-40C to +105C",
         "Active", "Solid thermal slug soldered to L2 GND; 50-ohm RF and LO ports matched"],
        ["CMP-SEN-004", "MOSAIC-SENSE", "STMicroelectronics", "STHV748L",
         "4-Channel Monolithic +/-100V 2A High-Voltage Ultrasonic Pulser", "QFN-64 (10x10mm)", "64 pins / 0.5 mm",
         "+/-100V HV, 3.3V Logic", "1.8 W (at 10kHz PRF)", "-40C to +125C",
         "Active", "Creepage rule > 1.5mm on HV traces; dedicated HV GND star return"],
        ["CMP-SEN-005", "MOSAIC-SENSE", "Microchip", "MD0100DK6-G",
         "100V Bidirectional High-Voltage T/R Protection Switch", "DFN-8 (3x3mm)", "8 pins / 0.65 mm",
         "Passive (+/-100V clamping)", "< 1 mW", "-40C to +85C",
         "Active", "Protects AD8331 input from 100V pulse; turn-on time < 20 ns"],
        ["CMP-SEN-006", "MOSAIC-SENSE", "Analog Devices", "AD8331ARQZ",
         "Ultralow Noise Variable Gain Amplifier with TGC (0.74 nV/rtHz)", "QSOP-20", "20 pins / 0.635 mm",
         "5.0V VPOS", "125 mW", "-40C to +85C",
         "Active", "Analog gain ramp voltage (VGAIN) filtered with low-noise RC; shielded traces"],
        ["CMP-SEN-007", "MOSAIC-SENSE", "Analog Devices", "AD9235BCPZ-65",
         "12-Bit 65 MSPS 3V A/D Converter (Ultrasonic Echoes)", "LFCSP-32 (5x5mm)", "32 pins / 0.5 mm",
         "3.0V AVDD, 1.8V to 3.3V DRVDD", "300 mW", "-40C to +85C",
         "Active", "Differential analog input traces length-matched to +/- 10 mils; low-jitter clock"],
        ["CMP-SEN-008", "MOSAIC-SENSE", "Texas Instruments", "ADS8881IDGS",
         "18-Bit 2 MSPS True Differential SAR ADC (RF I/Q Baseband)", "VSSOP-10", "10 pins / 0.5 mm",
         "2.7V to 3.6V AVDD, 1.65V to 3.6V DVDD", "55 mW", "-40C to +85C",
         "Active", "Driven by low-noise fully-differential op-amp (THS4551); ADR4525 reference"],
        ["CMP-SEN-009", "MOSAIC-SENSE", "Analog Devices", "ADG904BCPZ",
         "Wideband DC to 2.5 GHz Absorptive SP4T Switch (SOL Calibration)", "LFCSP-20 (4x4mm)", "20 pins / 0.5 mm",
         "1.65V to 2.75V VDD", "1 uW", "-40C to +85C",
         "Active", "50-ohm RF transmission line routing on all 4 switched ports; isolation > 35dB"],
        ["CMP-SEN-010", "MOSAIC-SENSE", "Analog Devices", "ADR4525BRZ",
         "Ultra-Low Noise, High Accuracy 2.500V Reference (2 ppm/C)", "SOIC-8", "8 pins / 1.27 mm",
         "3.0V to 15V Vin, 2.500V Vout", "2.5 mW", "-40C to +125C",
         "Active", "Output decoupled with 10uF ceramic + 0.1uF C0G; Kelvin connection to ADC VREF"],
        ["CMP-SEN-011", "MOSAIC-SENSE", "Texas Instruments", "TMP117AIDRVR",
         "High-Precision Digital Temperature Sensor (+-0.1C Accuracy)", "WSON-6 (2x2mm)", "6 pins / 0.65 mm",
         "1.8V to 5.5V VDD", "15 uW", "-55C to +150C",
         "Active", "Place directly on RF ground copper adjacent to ADF4351, LTC5586, and SOL cal"],
        ["CMP-SEN-012", "MOSAIC-SENSE", "Vishay Precision", "FC0402E50R0BST1",
         "High-Frequency 0402 50.0 Ohm 0.1% Thin-Film RF Resistor (SOL Load)", "0402 SMD", "2 pads / 0402",
         "Up to 20 GHz, 50mW", "N/A", "-55C to +155C",
         "Active", "Solder directly to 50-ohm microstrip landing pad with minimal solder volume"],
        ["CMP-SEN-013", "MOSAIC-SENSE", "Samtec", "QTH-060-01-L-D-A",
         "120-Pin High-Speed Mezzanine Plug (Mates to CORE)", "SMD Mezzanine", "120 pins / 0.5 mm",
         "Mating connector to QSH-060", "N/A", "-55C to +125C",
         "Active", "High-speed ADC bus pins length-matched within group to < 50 mils"],

        # MOSAIC-RADAR
        ["CMP-RAD-001", "MOSAIC-RADAR", "Texas Instruments", "AWR6843AOP",
         "Single-Chip 60-64 GHz mmWave Sensor with Antenna on Package", "FCBGA-161", "161 pins / 0.5 mm",
         "1.2V, 1.8V, 3.3V", "2.1 W typ.", "-40C to +105C",
         "Active", "Strict keepout zone: zero copper or routing on any layer beneath AoP antenna array"],
        ["CMP-RAD-002", "MOSAIC-RADAR", "Texas Instruments", "LP87524BRNFRQ1",
         "4-Channel 10A Buck PMIC for AWR6843 Radar", "QFN-26 (4x4mm)", "26 pins / 0.5 mm",
         "3.3V to 5.5V Vin, 1.2V/1.8V Vout", "350 mW", "-40C to +125C",
         "Active", "Fast transient response for radar chirps; ripple < 5mV RMS"],

        # MOSAIC-RESERVOIR
        ["CMP-RES-001", "MOSAIC-RESERVOIR", "Skyworks Solutions", "SMS7621-079LF",
         "Surface Mount 0402 Schottky Barrier Diode (Non-Linear Clamping)", "SC-79 / 0402", "2 pads / SMD",
         "Forward V_f = 260 mV at 0.1mA", "< 5 mW", "-65C to +150C",
         "Active", "Anti-parallel pair creates symmetric cubic non-linearity for physical reservoir"],
        ["CMP-RES-002", "MOSAIC-RESERVOIR", "Analog Devices", "AD5683RBCPZ-RL7",
         "16-Bit Single SPI DAC with 2 ppm/C Reference (Reservoir Bias)", "LFCSP-8 (2x2mm)", "8 pins / 0.5 mm",
         "2.7V to 5.5V VDD", "5 mW", "-40C to +105C",
         "Active", "Ultra-stable static DC tuning for reservoir operating point"]
    ]
    
    col_widths = [14, 16, 20, 25, 38, 22, 18, 22, 16, 18, 14, 38]
    
    # Palette
    header_fill = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="1A365D")
    data_font = Font(name="Calibri", size=10)
    border_side = Side(border_style="thin", color="CBD5E0")
    thin_border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)
    alt_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")

    ws.cell(row=1, column=1, value="MOSAIC-Σ: Master Component Specification Register").font = title_font
    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 10

    header_row = 3
    ws.row_dimensions[header_row].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    for row_idx, r in enumerate(components, header_row + 1):
        ws.row_dimensions[row_idx].height = 22
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

    wb.save(os.path.join(BASE_DIR, "03_COMPONENT_RESEARCH/COMPONENT_MASTER_REGISTER.xlsx"))
    print("Built COMPONENT_MASTER_REGISTER.xlsx successfully!")

if __name__ == "__main__":
    build_component_register()
