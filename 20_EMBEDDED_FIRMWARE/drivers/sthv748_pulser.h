/**
 * @file sthv748_pulser.h
 * @brief Zero-Trust Driver for STMicroelectronics STHV748 4-Channel +/-100V Ultrasonic Pulser.
 * @project MOSAIC-Sigma Autonomous Matter Intelligence Engine
 */

#ifndef STHV748_PULSER_H
#define STHV748_PULSER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define STHV748_MAX_PULSE_WIDTH_NS   500
#define STHV748_MIN_PULSE_WIDTH_NS    20
#define STHV748_MIN_RECOVERY_US      100
#define STHV748_MAX_RAIL_VOLTS       105.0f

typedef enum {
    STHV748_OK = 0,
    STHV748_ERR_INVALID_PARAM   = -1,
    STHV748_ERR_OVERVOLTAGE     = -2,
    STHV748_ERR_DUTY_CYCLE_TRIP = -3,
    STHV748_ERR_INTERLOCK_OPEN  = -4,
    STHV748_ERR_UNINITIALIZED   = -5
} sthv748_status_t;

typedef enum {
    STHV748_MODE_3LEVEL = 0, // +VPP, 0V, -VNN
    STHV748_MODE_5LEVEL = 1  // +VPP1, +VPP2, 0V, -VNN1, -VNN2
} sthv748_mode_t;

typedef struct {
    float vpp_volts;
    float vnn_volts;
    uint32_t pulse_width_ns;
    sthv748_mode_t mode;
    bool enable_active_clamp;
    bool enable_damping;
} sthv748_config_t;

typedef struct {
    sthv748_config_t config;
    bool is_initialized;
    uint32_t last_fire_timestamp_us;
    uint32_t total_shots;
    uint32_t trace_id;
} sthv748_inst_t;

sthv748_status_t sthv748_init(sthv748_inst_t *inst, const sthv748_config_t *cfg, uint32_t trace_id);
sthv748_status_t sthv748_arm_and_verify(sthv748_inst_t *inst, float measured_vpp, float measured_vnn);
sthv748_status_t sthv748_fire_pulse(sthv748_inst_t *inst, uint32_t current_timestamp_us);

#ifdef __cplusplus
}
#endif

#endif /* STHV748_PULSER_H */
