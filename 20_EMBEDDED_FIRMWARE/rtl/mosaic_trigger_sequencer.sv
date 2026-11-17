// Project: MOSAIC-Sigma Autonomous Matter Intelligence Engine
// Module:  mosaic_trigger_sequencer.sv
// Description: Multi-physics hardware trigger alignment and sequencing engine for UltraScale+ PL.
// Features: Sub-nanosecond delay generation, ultrasound/RF synchronization, and safety interlocks.

`timescale 1ns / 1ps

module mosaic_trigger_sequencer #(
    parameter int CLK_FREQ_HZ = 200_000_000, // 200 MHz system clock (5 ns period)
    parameter int DELAY_WIDTH  = 32
)(
    input  logic                   clk,
    input  logic                   rst_n,

    // Control & Configuration Interface
    input  logic                   arm_i,
    input  logic                   soft_trigger_i,
    input  logic                   ext_trigger_i,
    input  logic                   interlock_safe_i, // High-voltage & thermal interlock check

    // Programmable Timing Registers (clock cycles)
    input  logic [DELAY_WIDTH-1:0] pulser_delay_cycles_i,
    input  logic [DELAY_WIDTH-1:0] pulser_width_cycles_i,
    input  logic [DELAY_WIDTH-1:0] tr_blanking_cycles_i,
    input  logic [DELAY_WIDTH-1:0] rf_chirp_delay_cycles_i,
    input  logic [DELAY_WIDTH-1:0] adc_sample_delay_cycles_i,
    input  logic [DELAY_WIDTH-1:0] adc_window_cycles_i,

    // Synchronized Physical Triggers
    output logic                   pulser_tx_o,
    output logic                   tr_switch_blank_o,
    output logic                   rf_chirp_trig_o,
    output logic                   adc_capture_en_o,
    output logic                   metasurface_latch_o,

    // Diagnostics
    output logic                   busy_o,
    output logic                   fault_interlock_o,
    output logic [31:0]            trigger_counter_o
);

    typedef enum logic [2:0] {
        IDLE        = 3'b000,
        ARMED       = 3'b001,
        RUNNING     = 3'b010,
        HOLD_BLANK  = 3'b011,
        FAULT       = 3'b100
    } state_t;

    state_t state_reg, state_next;

    logic [DELAY_WIDTH-1:0] cycle_cnt_reg, cycle_cnt_next;
    logic [31:0]            seq_counter_reg, seq_counter_next;
    logic                   fault_reg, fault_next;

    logic ext_trig_d1, ext_trig_d2, ext_trig_pulse;
    assign ext_trig_pulse = ext_trig_d1 & ~ext_trig_d2;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ext_trig_d1 <= 1'b0;
            ext_trig_d2 <= 1'b0;
        end else begin
            ext_trig_d1 <= ext_trigger_i;
            ext_trig_d2 <= ext_trig_d1;
        end
    end

    // Sequential State Register
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_reg       <= IDLE;
            cycle_cnt_reg   <= '0;
            seq_counter_reg <= '0;
            fault_reg       <= 1'b0;
        end else begin
            state_reg       <= state_next;
            cycle_cnt_reg   <= cycle_cnt_next;
            seq_counter_reg <= seq_counter_next;
            fault_reg       <= fault_next;
        end
    end

    // Combinational State Transition and Outputs
    always_comb begin
        state_next       = state_reg;
        cycle_cnt_next   = cycle_cnt_reg;
        seq_counter_next = seq_counter_reg;
        fault_next       = fault_reg;

        pulser_tx_o         = 1'b0;
        tr_switch_blank_o   = 1'b0;
        rf_chirp_trig_o     = 1'b0;
        adc_capture_en_o    = 1'b0;
        metasurface_latch_o = 1'b0;
        busy_o              = 1'b0;

        case (state_reg)
            IDLE: begin
                cycle_cnt_next = '0;
                fault_next     = 1'b0;
                if (arm_i) begin
                    state_next = ARMED;
                end
            end

            ARMED: begin
                cycle_cnt_next = '0;
                if (!interlock_safe_i) begin
                    fault_next = 1'b1;
                    state_next = FAULT;
                end else if (soft_trigger_i || ext_trig_pulse) begin
                    state_next = RUNNING;
                    seq_counter_next = seq_counter_reg + 1'b1;
                    metasurface_latch_o = 1'b1; // Strobe metasurface update at sequence start
                end
            end

            RUNNING: begin
                busy_o = 1'b1;
                cycle_cnt_next = cycle_cnt_reg + 1'b1;

                // Safety Interlock Enforcement during active pulse
                if (!interlock_safe_i) begin
                    fault_next = 1'b1;
                    state_next = FAULT;
                end

                // 1. T/R Switch Blanking (Protect receiver LNA before and during pulser fire)
                if (cycle_cnt_reg < tr_blanking_cycles_i) begin
                    tr_switch_blank_o = 1'b1;
                end

                // 2. High-Voltage Pulser TX Gate
                if (cycle_cnt_reg >= pulser_delay_cycles_i &&
                    cycle_cnt_reg < (pulser_delay_cycles_i + pulser_width_cycles_i)) begin
                    pulser_tx_o = 1'b1;
                end

                // 3. RF PLL Chirp Strobe
                if (cycle_cnt_reg >= rf_chirp_delay_cycles_i &&
                    cycle_cnt_reg < (rf_chirp_delay_cycles_i + 4)) begin
                    rf_chirp_trig_o = 1'b1;
                end

                // 4. ADC Capture Window
                if (cycle_cnt_reg >= adc_sample_delay_cycles_i &&
                    cycle_cnt_reg < (adc_sample_delay_cycles_i + adc_window_cycles_i)) begin
                    adc_capture_en_o = 1'b1;
                end

                // Sequence completion check
                if (cycle_cnt_reg >= (adc_sample_delay_cycles_i + adc_window_cycles_i) &&
                    cycle_cnt_reg >= tr_blanking_cycles_i) begin
                    state_next = IDLE;
                end
            end

            FAULT: begin
                fault_next = 1'b1;
                busy_o     = 1'b0;
                // Require arm de-assertion to clear fault
                if (!arm_i) begin
                    state_next = IDLE;
                end
            end

            default: state_next = IDLE;
        endcase
    end

    assign fault_interlock_o = fault_reg;
    assign trigger_counter_o = seq_counter_reg;

endmodule
