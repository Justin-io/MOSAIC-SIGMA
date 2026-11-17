/**
 * @file ad5940_driver.h
 * @brief Zero-Trust Bare-Metal / RTOS Driver for Analog Devices AD5940 Impedance AFE.
 * @project MOSAIC-Sigma Autonomous Matter Intelligence Engine
 */

#ifndef AD5940_DRIVER_H
#define AD5940_DRIVER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define AD5940_MIN_FREQ_HZ         0.016f
#define AD5940_MAX_FREQ_HZ         200000.0f
#define AD5940_MAX_EXCIT_MV        1200.0f
#define AD5940_MIN_RCAL_OHMS       100.0f
#define AD5940_MAX_RCAL_OHMS       1000000.0f

typedef enum {
    AD5940_OK = 0,
    AD5940_ERR_INVALID_PARAM  = -1,
    AD5940_ERR_COMM_TIMEOUT   = -2,
    AD5940_ERR_CALIBRATION    = -3,
    AD5940_ERR_OVERFLOW       = -4,
    AD5940_ERR_UNINITIALIZED  = -5
} ad5940_status_t;

typedef struct {
    float rcal_ohms;          /* Precision internal/external calibration resistor */
    float excitation_mv;      /* AC peak excitation voltage in mV (<= 1200 mV) */
    uint16_t dft_num_samples; /* DFT sample count (4, 8, 16, ..., 16384) */
    bool four_wire_mode;      /* true: 4-wire (CE0, RE0, WE0, SE0); false: 2-wire */
} ad5940_config_t;

typedef struct {
    float real;
    float imag;
    float magnitude;
    float phase_deg;
    float frequency_hz;
} ad5940_impedance_t;

typedef struct {
    ad5940_config_t config;
    bool is_initialized;
    uint32_t trace_id;
    int (*spi_transmit_receive)(const uint8_t *tx, uint8_t *rx, uint16_t len);
    void (*delay_us)(uint32_t us);
} ad5940_inst_t;

ad5940_status_t ad5940_init(ad5940_inst_t *inst, const ad5940_config_t *cfg, uint32_t trace_id);
ad5940_status_t ad5940_measure_point(ad5940_inst_t *inst, float freq_hz, ad5940_impedance_t *out_result);
ad5940_status_t ad5940_self_calibrate(ad5940_inst_t *inst, float *gain_factor_out);

#ifdef __cplusplus
}
#endif

#endif /* AD5940_DRIVER_H */
