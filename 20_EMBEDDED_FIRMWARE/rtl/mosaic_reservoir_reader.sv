// Project: MOSAIC-Sigma Autonomous Matter Intelligence Engine
// Module:  mosaic_reservoir_reader.sv
// Description: Physical reservoir state feature extraction & ADC stream processor.
// Features: Real-time nonlinear feature extraction, moving variance, and ring buffer readout.

`timescale 1ns / 1ps

module mosaic_reservoir_reader #(
    parameter int DATA_WIDTH    = 16,
    parameter int NUM_FEATURES  = 8,
    parameter int BUFFER_DEPTH  = 1024
)(
    input  logic                   clk,
    input  logic                   rst_n,

    // ADC Stream Input
    input  logic                   adc_valid_i,
    input  logic signed [DATA_WIDTH-1:0] adc_data_i,
    input  logic                   sample_window_en_i,

    // Feature Readout Interface
    output logic                   features_valid_o,
    output logic signed [31:0]     features_o [NUM_FEATURES],

    // Diagnostic & Overflow Flags
    output logic                   buffer_overflow_o,
    output logic [15:0]            peak_amplitude_o
);

    logic signed [DATA_WIDTH-1:0] prev_sample_d1, prev_sample_d2;
    logic signed [31:0]           acc_energy;
    logic signed [31:0]           acc_abs;
    logic signed [31:0]           acc_diff_sq;
    logic signed [31:0]           acc_cubic;
    logic [15:0]                  max_val;
    logic [15:0]                  sample_count;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prev_sample_d1    <= '0;
            prev_sample_d2    <= '0;
            acc_energy        <= '0;
            acc_abs           <= '0;
            acc_diff_sq       <= '0;
            acc_cubic         <= '0;
            max_val           <= '0;
            sample_count      <= '0;
            features_valid_o  <= 1'b0;
            buffer_overflow_o <= 1'b0;
            peak_amplitude_o  <= '0;
            for (int i = 0; i < NUM_FEATURES; i++) begin
                features_o[i] <= '0;
            end
        end else begin
            if (sample_window_en_i) begin
                if (adc_valid_i) begin
                    prev_sample_d1 <= adc_data_i;
                    prev_sample_d2 <= prev_sample_d1;
                    sample_count   <= sample_count + 1'b1;

                    // Non-linear transformations across physical reservoir echoes
                    // F0: Mean energy (x^2)
                    acc_energy  <= acc_energy + (adc_data_i * adc_data_i);
                    // F1: L1 norm (|x|)
                    acc_abs     <= acc_abs + ((adc_data_i >= 0) ? adc_data_i : -adc_data_i);
                    // F2: 1st difference square (dx/dt)^2
                    acc_diff_sq <= acc_diff_sq + ((adc_data_i - prev_sample_d1) * (adc_data_i - prev_sample_d1));
                    // F3: Cubic echo nonlinearity (x^3 / 2^16)
                    acc_cubic   <= acc_cubic + ((adc_data_i * adc_data_i * adc_data_i) >>> 16);

                    // Peak Tracking
                    if (((adc_data_i >= 0) ? adc_data_i : -adc_data_i) > signed'(max_val)) begin
                        max_val <= (adc_data_i >= 0) ? adc_data_i[15:0] : (-adc_data_i)[15:0];
                    end
                end
                features_valid_o <= 1'b0;
            end else begin
                // Window closed: Latch features and assert valid
                if (sample_count > 0) begin
                    features_valid_o <= 1'b1;
                    features_o[0]    <= acc_energy;
                    features_o[1]    <= acc_abs;
                    features_o[2]    <= acc_diff_sq;
                    features_o[3]    <= acc_cubic;
                    features_o[4]    <= {16'b0, max_val};
                    features_o[5]    <= {16'b0, sample_count};
                    features_o[6]    <= acc_energy >>> 8; // Normalized power
                    features_o[7]    <= (acc_diff_sq >>> 4) + acc_abs;

                    peak_amplitude_o <= max_val;

                    // Reset accumulators for next sweep
                    acc_energy   <= '0;
                    acc_abs      <= '0;
                    acc_diff_sq  <= '0;
                    acc_cubic    <= '0;
                    max_val      <= '0;
                    sample_count <= '0;
                end else begin
                    features_valid_o <= 1'b0;
                end
            end
        end
    end

endmodule
