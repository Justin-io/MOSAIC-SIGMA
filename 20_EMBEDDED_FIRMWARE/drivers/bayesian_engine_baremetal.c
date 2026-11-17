/**
 * @file bayesian_engine_baremetal.c
 * @brief Implementation of Embedded Bayesian Active Learning with Expected Information Gain.
 */

#include "bayesian_engine_baremetal.h"
#include <math.h>
#include <string.h>

static float compute_rbf_kernel(const float x1[BED_DIMENSIONS], const float x2[BED_DIMENSIONS], const bed_hyperparams_t *hp) {
    float dist_sq = 0.0f;
    for (int d = 0; d < BED_DIMENSIONS; d++) {
        float diff = (x1[d] - x2[d]) / hp->length_scales[d];
        dist_sq += diff * diff;
    }
    return hp->signal_variance * expf(-0.5f * dist_sq);
}

bed_status_t bed_init(bed_engine_t *engine, const bed_hyperparams_t *hp, uint32_t trace_id) {
    if (!engine || !hp) {
        return BED_ERR_INVALID_PARAM;
    }

    for (int d = 0; d < BED_DIMENSIONS; d++) {
        if (hp->length_scales[d] <= 0.0f) return BED_ERR_INVALID_PARAM;
    }
    if (hp->signal_variance <= 0.0f || hp->noise_variance <= 0.0f) {
        return BED_ERR_INVALID_PARAM;
    }

    memset(engine, 0, sizeof(*engine));
    engine->hp = *hp;
    engine->is_initialized = true;
    engine->trace_id = trace_id;

    return BED_OK;
}

bed_status_t bed_add_observation(bed_engine_t *engine, const float coords[BED_DIMENSIONS], float value) {
    if (!engine || !coords) {
        return BED_ERR_INVALID_PARAM;
    }
    if (!engine->is_initialized) {
        return BED_ERR_UNINITIALIZED;
    }
    if (engine->num_obs >= BED_MAX_OBSERVATIONS) {
        return BED_ERR_CAPACITY_FULL;
    }

    uint32_t idx = engine->num_obs;
    for (int d = 0; d < BED_DIMENSIONS; d++) {
        engine->observations[idx].coords[d] = coords[d];
    }
    engine->observations[idx].value = value;
    engine->observations[idx].variance = engine->hp.noise_variance;
    engine->num_obs++;

    return BED_OK;
}

bed_status_t bed_predict(const bed_engine_t *engine, const float candidate[BED_DIMENSIONS], float *mean_out, float *var_out) {
    if (!engine || !candidate || !mean_out || !var_out) {
        return BED_ERR_INVALID_PARAM;
    }
    if (!engine->is_initialized) {
        return BED_ERR_UNINITIALIZED;
    }

    if (engine->num_obs == 0) {
        *mean_out = 0.0f;
        *var_out = engine->hp.signal_variance + engine->hp.noise_variance;
        return BED_OK;
    }

    // Weight distance from existing points using kernel
    float k_star[BED_MAX_OBSERVATIONS];
    float max_corr = 0.0f;
    float weighted_val_sum = 0.0f;
    float weight_sum = 0.0f;

    for (uint32_t i = 0; i < engine->num_obs; i++) {
        k_star[i] = compute_rbf_kernel(candidate, engine->observations[i].coords, &engine->hp);
        if (k_star[i] > max_corr) max_corr = k_star[i];
        weighted_val_sum += k_star[i] * engine->observations[i].value;
        weight_sum += k_star[i];
    }

    if (weight_sum > 1e-6f) {
        *mean_out = weighted_val_sum / weight_sum;
    } else {
        *mean_out = 0.0f;
    }

    // Posterior variance drops when near previous observations
    float var_reduction = (max_corr * max_corr) / (engine->hp.signal_variance + engine->hp.noise_variance);
    *var_out = (engine->hp.signal_variance - var_reduction) + engine->hp.noise_variance;
    if (*var_out < engine->hp.noise_variance) {
        *var_out = engine->hp.noise_variance;
    }

    return BED_OK;
}

bed_status_t bed_select_next_experiment(const bed_engine_t *engine, const float candidates[][BED_DIMENSIONS], uint32_t num_candidates, uint32_t *best_index_out) {
    if (!engine || !candidates || !best_index_out || num_candidates == 0) {
        return BED_ERR_INVALID_PARAM;
    }
    if (!engine->is_initialized) {
        return BED_ERR_UNINITIALIZED;
    }

    float max_acquisition = -1e9f;
    uint32_t best_idx = 0;

    for (uint32_t c = 0; c < num_candidates; c++) {
        float mean = 0.0f;
        float var = 0.0f;
        bed_predict(engine, candidates[c], &mean, &var);

        // Expected Information Gain (EIG) proxy: Upper Confidence Bound / Uncertainty Entropy
        // alpha(x) = sqrt(var(x)) + exploration_weight * |mean(x)|
        float acquisition = sqrtf(var) + engine->hp.exploration_weight * fabsf(mean);
        if (acquisition > max_acquisition) {
            max_acquisition = acquisition;
            best_idx = c;
        }
    }

    *best_index_out = best_idx;
    return BED_OK;
}
