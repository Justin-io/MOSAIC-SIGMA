/**
 * @file sthv748_pulser.c
 * @brief Implementation of STHV748 High-Voltage Pulser Safety Driver.
 */

#include "sthv748_pulser.h"
#include <string.h>
#include <math.h>

sthv748_status_t sthv748_init(sthv748_inst_t *inst, const sthv748_config_t *cfg, uint32_t trace_id) {
    if (!inst || !cfg) {
        return STHV748_ERR_INVALID_PARAM;
    }

    if (cfg->pulse_width_ns < STHV748_MIN_PULSE_WIDTH_NS ||
        cfg->pulse_width_ns > STHV748_MAX_PULSE_WIDTH_NS) {
        return STHV748_ERR_INVALID_PARAM;
    }
    if (fabsf(cfg->vpp_volts) > STHV748_MAX_RAIL_VOLTS ||
        fabsf(cfg->vnn_volts) > STHV748_MAX_RAIL_VOLTS) {
        return STHV748_ERR_OVERVOLTAGE;
    }

    inst->config = *cfg;
    inst->is_initialized = true;
    inst->last_fire_timestamp_us = 0;
    inst->total_shots = 0;
    inst->trace_id = trace_id;

    return STHV748_OK;
}

sthv748_status_t sthv748_arm_and_verify(sthv748_inst_t *inst, float measured_vpp, float measured_vnn) {
    if (!inst) {
        return STHV748_ERR_INVALID_PARAM;
    }
    if (!inst->is_initialized) {
        return STHV748_ERR_UNINITIALIZED;
    }

    /* Rail telemetry cross-check within 10% of configured */
    if (fabsf(measured_vpp - inst->config.vpp_volts) > (0.10f * inst->config.vpp_volts) ||
        fabsf(measured_vnn - inst->config.vnn_volts) > (0.10f * fabsf(inst->config.vnn_volts))) {
        return STHV748_ERR_INTERLOCK_OPEN;
    }

    return STHV748_OK;
}

sthv748_status_t sthv748_fire_pulse(sthv748_inst_t *inst, uint32_t current_timestamp_us) {
    if (!inst) {
        return STHV748_ERR_INVALID_PARAM;
    }
    if (!inst->is_initialized) {
        return STHV748_ERR_UNINITIALIZED;
    }

    /* Enforce duty-cycle recovery interval */
    if (inst->last_fire_timestamp_us != 0 &&
        (current_timestamp_us - inst->last_fire_timestamp_us) < STHV748_MIN_RECOVERY_US) {
        return STHV748_ERR_DUTY_CYCLE_TRIP;
    }

    inst->last_fire_timestamp_us = current_timestamp_us;
    inst->total_shots++;

    return STHV748_OK;
}
