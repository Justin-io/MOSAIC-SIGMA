/**
 * @file adf4351_synth.c
 * @brief Implementation of ADF4351 Wideband PLL Register Calculator.
 */

#include "adf4351_synth.h"
#include <math.h>

#define VCO_MIN_MHZ 2200.0f
#define VCO_MAX_MHZ 4400.0f

adf4351_status_t adf4351_init(adf4351_inst_t *inst, float ref_freq_mhz, uint32_t trace_id) {
    if (!inst) {
        return ADF4351_ERR_INVALID_PARAM;
    }
    if (ref_freq_mhz < 10.0f || ref_freq_mhz > 250.0f) {
        return ADF4351_ERR_INVALID_PARAM;
    }

    inst->ref_freq_mhz = ref_freq_mhz;
    inst->current_freq_mhz = 0.0f;
    inst->is_initialized = true;
    inst->trace_id = trace_id;

    return ADF4351_OK;
}

adf4351_status_t adf4351_calculate_registers(adf4351_inst_t *inst, float target_freq_mhz, adf4351_registers_t *out_regs) {
    if (!inst || !out_regs) {
        return ADF4351_ERR_INVALID_PARAM;
    }
    if (!inst->is_initialized) {
        return ADF4351_ERR_UNINITIALIZED;
    }
    if (target_freq_mhz < ADF4351_MIN_FREQ_MHZ || target_freq_mhz > ADF4351_MAX_FREQ_MHZ) {
        return ADF4351_ERR_FREQ_OUT_OF_RANGE;
    }

    // Determine output divider (1, 2, 4, 8, 16, 32, 64)
    uint32_t rf_div = 1;
    uint32_t rf_div_sel = 0;
    float vco_freq = target_freq_mhz;

    while (vco_freq < VCO_MIN_MHZ && rf_div < 64) {
        rf_div <<= 1;
        rf_div_sel++;
        vco_freq = target_freq_mhz * (float)rf_div;
    }

    if (vco_freq < VCO_MIN_MHZ || vco_freq > VCO_MAX_MHZ) {
        return ADF4351_ERR_FREQ_OUT_OF_RANGE;
    }

    // PFD frequency = ref_freq (with R divider = 1)
    float pfd_freq = inst->ref_freq_mhz;
    uint32_t int_val = (uint32_t)(vco_freq / pfd_freq);
    uint32_t mod_val = 4095; // Max resolution modulus
    float remainder = (vco_freq / pfd_freq) - (float)int_val;
    uint32_t frac_val = (uint32_t)roundf(remainder * (float)mod_val);

    // Register 0: [30:15] INT, [14:3] FRAC, [2:0] Control = 0
    out_regs->r0 = ((int_val & 0xFFFF) << 15) | ((frac_val & 0xFFF) << 3) | 0x00;

    // Register 1: [27] Prescaler 8/9, [14:3] MOD = 4095, [2:0] Control = 1
    out_regs->r1 = (1 << 27) | ((mod_val & 0xFFF) << 3) | 0x01;

    // Register 2: R=1, CP current, Control = 2
    out_regs->r2 = (1 << 14) | (7 << 9) | 0x02;

    // Register 3: Band select clock divider, Control = 3
    out_regs->r3 = (150 << 3) | 0x03;

    // Register 4: RF output power (+5dBm), RF divider select, Control = 4
    out_regs->r4 = (rf_div_sel << 20) | (1 << 5) | (3 << 3) | 0x04;

    // Register 5: Digital lock detect, Control = 5
    out_regs->r5 = (1 << 22) | 0x05;

    inst->current_freq_mhz = target_freq_mhz;
    inst->regs = *out_regs;

    return ADF4351_OK;
}
