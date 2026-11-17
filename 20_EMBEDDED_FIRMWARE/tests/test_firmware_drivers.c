/**
 * @file test_firmware_drivers.c
 * @brief Unit & Integration Tests for MOSAIC-Sigma Embedded Drivers.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>

#include "../drivers/ad5940_driver.h"
#include "../drivers/sthv748_pulser.h"
#include "../drivers/adf4351_synth.h"
#include "../drivers/bayesian_engine_baremetal.h"

static int g_tests_run = 0;
static int g_tests_passed = 0;

#define TEST_ASSERT(cond, msg) do { \
    g_tests_run++; \
    if (cond) { \
        g_tests_passed++; \
    } else { \
        fprintf(stderr, "[FAIL] Line %d: %s\n", __LINE__, msg); \
        exit(1); \
    } \
} while(0)

void test_ad5940() {
    printf("[TEST] AD5940 Impedance Spectrometer Driver...\n");
    ad5940_inst_t inst;
    ad5940_config_t cfg = {
        .rcal_ohms = 10000.0f,
        .excitation_mv = 500.0f,
        .dft_num_samples = 1024,
        .four_wire_mode = true
    };

    // 1. Invalid params check (Zero-Trust)
    TEST_ASSERT(ad5940_init(NULL, &cfg, 1001) == AD5940_ERR_INVALID_PARAM, "NULL inst rejection");
    cfg.rcal_ohms = 5.0f; // Below 100 ohms
    TEST_ASSERT(ad5940_init(&inst, &cfg, 1001) == AD5940_ERR_INVALID_PARAM, "Under-range R_cal rejection");
    cfg.rcal_ohms = 10000.0f;

    // 2. Proper Init
    TEST_ASSERT(ad5940_init(&inst, &cfg, 1001) == AD5940_OK, "Valid init");

    // 3. Frequency bounds check
    ad5940_impedance_t imp;
    TEST_ASSERT(ad5940_measure_point(&inst, 0.001f, &imp) == AD5940_ERR_INVALID_PARAM, "Below min freq rejection");
    TEST_ASSERT(ad5940_measure_point(&inst, 500000.0f, &imp) == AD5940_ERR_INVALID_PARAM, "Above max freq rejection");

    // 4. Nominal measurement sweep point at 10 kHz
    TEST_ASSERT(ad5940_measure_point(&inst, 10000.0f, &imp) == AD5940_OK, "Nominal 10 kHz measurement");
    TEST_ASSERT(imp.magnitude > 0.0f, "Positive magnitude");
    TEST_ASSERT(imp.phase_deg <= 0.0f, "Capacitive phase response");

    // 5. Calibration check
    float cal_factor = 0.0f;
    TEST_ASSERT(ad5940_self_calibrate(&inst, &cal_factor) == AD5940_OK, "Self calibration");
    TEST_ASSERT(fabsf(cal_factor - 1.0f) < 0.01f, "Calibration factor near unity");
}

void test_sthv748() {
    printf("[TEST] STHV748 High-Voltage Pulser Safety Driver...\n");
    sthv748_inst_t inst;
    sthv748_config_t cfg = {
        .vpp_volts = 90.0f,
        .vnn_volts = -90.0f,
        .pulse_width_ns = 100,
        .mode = STHV748_MODE_3LEVEL,
        .enable_active_clamp = true,
        .enable_damping = true
    };

    // 1. Zero-Trust Overvoltage rejection
    cfg.vpp_volts = 150.0f; // Exceeds 105V limit
    TEST_ASSERT(sthv748_init(&inst, &cfg, 2001) == STHV748_ERR_OVERVOLTAGE, "Overvoltage rejection");
    cfg.vpp_volts = 90.0f;

    // 2. Pulse width limit rejection
    cfg.pulse_width_ns = 1000; // Exceeds 500ns limit
    TEST_ASSERT(sthv748_init(&inst, &cfg, 2001) == STHV748_ERR_INVALID_PARAM, "Pulse width limit rejection");
    cfg.pulse_width_ns = 100;

    // 3. Init
    TEST_ASSERT(sthv748_init(&inst, &cfg, 2001) == STHV748_OK, "Valid init");

    // 4. Interlock verification check
    TEST_ASSERT(sthv748_arm_and_verify(&inst, 90.0f, -90.0f) == STHV748_OK, "Interlock nominal match");
    TEST_ASSERT(sthv748_arm_and_verify(&inst, 50.0f, -90.0f) == STHV748_ERR_INTERLOCK_OPEN, "Interlock voltage mismatch");

    // 5. Duty-cycle / thermal enforcement
    TEST_ASSERT(sthv748_fire_pulse(&inst, 1000) == STHV748_OK, "First fire pulse");
    // Immediate re-fire within 10 us (< 100 us recovery) must trip
    TEST_ASSERT(sthv748_fire_pulse(&inst, 1010) == STHV748_ERR_DUTY_CYCLE_TRIP, "Duty cycle trip enforced");
    // Re-fire after 150 us must succeed
    TEST_ASSERT(sthv748_fire_pulse(&inst, 1200) == STHV748_OK, "Re-fire after proper recovery");
    TEST_ASSERT(inst.total_shots == 2, "Shot counter tracking");
}

void test_adf4351() {
    printf("[TEST] ADF4351 Microwave PLL Synthesizer Driver...\n");
    adf4351_inst_t inst;
    TEST_ASSERT(adf4351_init(&inst, 25.0f, 3001) == ADF4351_OK, "Valid 25MHz ref init");

    adf4351_registers_t regs;
    // 1. Out of range check
    TEST_ASSERT(adf4351_calculate_registers(&inst, 10.0f, &regs) == ADF4351_ERR_FREQ_OUT_OF_RANGE, "Low freq rejection");
    TEST_ASSERT(adf4351_calculate_registers(&inst, 5000.0f, &regs) == ADF4351_ERR_FREQ_OUT_OF_RANGE, "High freq rejection");

    // 2. 2.45 GHz synthesis calculation
    TEST_ASSERT(adf4351_calculate_registers(&inst, 2450.0f, &regs) == ADF4351_OK, "2450 MHz calculation");
    TEST_ASSERT((regs.r0 & 0x07) == 0x00, "R0 control bits = 0");
    TEST_ASSERT((regs.r1 & 0x07) == 0x01, "R1 control bits = 1");
    TEST_ASSERT((regs.r2 & 0x07) == 0x02, "R2 control bits = 2");
    TEST_ASSERT((regs.r4 & 0x07) == 0x04, "R4 control bits = 4");
}

void test_bayesian_engine() {
    printf("[TEST] Bayesian Experimental Design Engine...\n");
    bed_engine_t engine;
    bed_hyperparams_t hp = {
        .length_scales = {15.0f, 15.0f, 0.5f}, // X mm, Y mm, Freq GHz
        .signal_variance = 1.0f,
        .noise_variance = 0.05f,
        .exploration_weight = 2.0f
    };

    TEST_ASSERT(bed_init(&engine, &hp, 4001) == BED_OK, "Valid BED init");

    // Candidate pool: 4 points
    float candidates[4][BED_DIMENSIONS] = {
        {10.0f, 10.0f, 2.45f},
        {50.0f, 50.0f, 2.45f},
        {80.0f, 80.0f, 2.45f},
        {10.0f, 12.0f, 2.45f}
    };

    uint32_t next_idx = 99;
    // Before observations, candidates have equal or initial variance
    TEST_ASSERT(bed_select_next_experiment(&engine, candidates, 4, &next_idx) == BED_OK, "Initial selection");

    // Add observation at (10, 10, 2.45) with strong defect response
    float obs_coord[3] = {10.0f, 10.0f, 2.45f};
    TEST_ASSERT(bed_add_observation(&engine, obs_coord, 2.5f) == BED_OK, "Add observation");

    // Predict near observation
    float mean_near = 0.0f, var_near = 0.0f;
    float near_coord[3] = {10.0f, 11.0f, 2.45f};
    TEST_ASSERT(bed_predict(&engine, near_coord, &mean_near, &var_near) == BED_OK, "Predict near");
    TEST_ASSERT(mean_near > 1.0f, "High predicted value near observation");
    TEST_ASSERT(var_near < hp.signal_variance, "Reduced variance near observation");

    // Predict far observation
    float mean_far = 0.0f, var_far = 0.0f;
    float far_coord[3] = {80.0f, 80.0f, 2.45f};
    TEST_ASSERT(bed_predict(&engine, far_coord, &mean_far, &var_far) == BED_OK, "Predict far");
    TEST_ASSERT(var_far > var_near, "Higher uncertainty far from observation");
}

int main(void) {
    printf("====================================================\n");
    printf("PROJECT MOSAIC-SIGMA: FIRMWARE DRIVER TEST SUITE\n");
    printf("====================================================\n");

    test_ad5940();
    test_sthv748();
    test_adf4351();
    test_bayesian_engine();

    printf("\nSUMMARY: %d / %d tests passed successfully (100%%).\n", g_tests_passed, g_tests_run);
    return 0;
}
