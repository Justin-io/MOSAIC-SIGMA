/**
 * @file adf4351_synth.h
 * @brief Zero-Trust Driver for Analog Devices ADF4351 Wideband RF Synthesizer.
 * @project MOSAIC-Sigma Autonomous Matter Intelligence Engine
 */

#ifndef ADF4351_SYNTH_H
#define ADF4351_SYNTH_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define ADF4351_MIN_FREQ_MHZ    35.0f
#define ADF4351_MAX_FREQ_MHZ    4400.0f
#define ADF4351_REF_FREQ_MHZ    25.0f // SiTime VCTCXO reference

typedef enum {
    ADF4351_OK = 0,
    ADF4351_ERR_INVALID_PARAM = -1,
    ADF4351_ERR_FREQ_OUT_OF_RANGE = -2,
    ADF4351_ERR_UNLOCKED = -3,
    ADF4351_ERR_UNINITIALIZED = -4
} adf4351_status_t;

typedef struct {
    uint32_t r0;
    uint32_t r1;
    uint32_t r2;
    uint32_t r3;
    uint32_t r4;
    uint32_t r5;
} adf4351_registers_t;

typedef struct {
    float ref_freq_mhz;
    float current_freq_mhz;
    adf4351_registers_t regs;
    bool is_initialized;
    uint32_t trace_id;
} adf4351_inst_t;

adf4351_status_t adf4351_init(adf4351_inst_t *inst, float ref_freq_mhz, uint32_t trace_id);
adf4351_status_t adf4351_calculate_registers(adf4351_inst_t *inst, float target_freq_mhz, adf4351_registers_t *out_regs);

#ifdef __cplusplus
}
#endif

#endif /* ADF4351_SYNTH_H */
