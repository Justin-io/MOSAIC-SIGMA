/**
 * @file bayesian_engine_baremetal.h
 * @brief Embedded Gaussian Process & Bayesian Experimental Design (BED) Active Learning Engine.
 * @project MOSAIC-Sigma Autonomous Matter Intelligence Engine
 */

#ifndef BAYESIAN_ENGINE_BAREMETAL_H
#define BAYESIAN_ENGINE_BAREMETAL_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define BED_MAX_OBSERVATIONS   64
#define BED_DIMENSIONS         3   // (X mm, Y mm, Frequency GHz)
#define BED_MAX_CANDIDATES     128

typedef enum {
    BED_OK = 0,
    BED_ERR_INVALID_PARAM = -1,
    BED_ERR_SINGULAR_MATRIX = -2,
    BED_ERR_CAPACITY_FULL = -3,
    BED_ERR_UNINITIALIZED = -4
} bed_status_t;

typedef struct {
    float coords[BED_DIMENSIONS];
    float value;
    float variance;
} bed_point_t;

typedef struct {
    float length_scales[BED_DIMENSIONS];
    float signal_variance;
    float noise_variance;
    float exploration_weight; // Beta parameter for UCB/EIG
} bed_hyperparams_t;

typedef struct {
    bed_point_t observations[BED_MAX_OBSERVATIONS];
    uint32_t num_obs;
    bed_hyperparams_t hp;
    float K_inv[BED_MAX_OBSERVATIONS][BED_MAX_OBSERVATIONS];
    bool is_initialized;
    uint32_t trace_id;
} bed_engine_t;

bed_status_t bed_init(bed_engine_t *engine, const bed_hyperparams_t *hp, uint32_t trace_id);
bed_status_t bed_add_observation(bed_engine_t *engine, const float coords[BED_DIMENSIONS], float value);
bed_status_t bed_predict(const bed_engine_t *engine, const float candidate[BED_DIMENSIONS], float *mean_out, float *var_out);
bed_status_t bed_select_next_experiment(const bed_engine_t *engine, const float candidates[][BED_DIMENSIONS], uint32_t num_candidates, uint32_t *best_index_out);

#ifdef __cplusplus
}
#endif

#endif /* BAYESIAN_ENGINE_BAREMETAL_H */
