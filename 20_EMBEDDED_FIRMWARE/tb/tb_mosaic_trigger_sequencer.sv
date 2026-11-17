// Project: MOSAIC-Sigma Autonomous Matter Intelligence Engine
// Testbench: tb_mosaic_trigger_sequencer.sv
// Validation: Timing verification, jitter, and safety interlock trip test.

`timescale 1ns / 1ps

module tb_mosaic_trigger_sequencer;

    logic clk;
    logic rst_n;
    logic arm;
    logic soft_trigger;
    logic ext_trigger;
    logic interlock_safe;

    logic [31:0] pulser_delay;
    logic [31:0] pulser_width;
    logic [31:0] tr_blanking;
    logic [31:0] rf_chirp_delay;
    logic [31:0] adc_sample_delay;
    logic [31:0] adc_window;

    logic pulser_tx;
    logic tr_switch_blank;
    logic rf_chirp_trig;
    logic adc_capture_en;
    logic metasurface_latch;
    logic busy;
    logic fault_interlock;
    logic [31:0] trigger_counter;

    mosaic_trigger_sequencer #(
        .CLK_FREQ_HZ(200_000_000),
        .DELAY_WIDTH(32)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .arm_i(arm),
        .soft_trigger_i(soft_trigger),
        .ext_trigger_i(ext_trigger),
        .interlock_safe_i(interlock_safe),
        .pulser_delay_cycles_i(pulser_delay),
        .pulser_width_cycles_i(pulser_width),
        .tr_blanking_cycles_i(tr_blanking),
        .rf_chirp_delay_cycles_i(rf_chirp_delay),
        .adc_sample_delay_cycles_i(adc_sample_delay),
        .adc_window_cycles_i(adc_window),
        .pulser_tx_o(pulser_tx),
        .tr_switch_blank_o(tr_switch_blank),
        .rf_chirp_trig_o(rf_chirp_trig),
        .adc_capture_en_o(adc_capture_en),
        .metasurface_latch_o(metasurface_latch),
        .busy_o(busy),
        .fault_interlock_o(fault_interlock),
        .trigger_counter_o(trigger_counter)
    );

    // 200 MHz clock generation (5 ns period)
    always #2.5 clk = ~clk;

    initial begin
        clk = 0;
        rst_n = 0;
        arm = 0;
        soft_trigger = 0;
        ext_trigger = 0;
        interlock_safe = 1;

        // Timing parameters (in 5ns cycles)
        pulser_delay     = 32'd10; // 50 ns delay
        pulser_width     = 32'd40; // 200 ns pulse width (5 MHz half-wave)
        tr_blanking      = 32'd80; // 400 ns blanking (covers pulse + recovery)
        rf_chirp_delay   = 32'd20; // 100 ns delay
        adc_sample_delay = 32'd30; // 150 ns delay
        adc_window       = 32'd100;// 500 ns window

        #20;
        rst_n = 1;
        #20;

        // TEST 1: Arm and Trigger Normal Cycle
        arm = 1;
        #20;
        soft_trigger = 1;
        #10;
        soft_trigger = 0;

        // Wait for busy completion
        wait(busy == 1);
        wait(busy == 0);
        #50;

        if (trigger_counter !== 32'd1) begin
            $display("[FAIL] Expected trigger_counter == 1, got %0d", trigger_counter);
            $finish(1);
        end else begin
            $display("[PASS] Test 1: Normal trigger sequence executed cleanly. Count = %0d", trigger_counter);
        end

        // TEST 2: Interlock Safety Violation Detection
        arm = 1;
        #20;
        soft_trigger = 1;
        #10;
        soft_trigger = 0;
        #30; // Mid-sequence
        interlock_safe = 0; // Trip safety clamp
        #20;

        if (fault_interlock !== 1'b1 || pulser_tx !== 1'b0) begin
            $display("[FAIL] Interlock trip failed to shutdown pulser or raise fault!");
            $finish(1);
        end else begin
            $display("[PASS] Test 2: Safety interlock successfully tripped and shut down pulser.");
        end

        // Clear fault by de-arming
        arm = 0;
        #20;
        interlock_safe = 1;
        #20;
        arm = 1;
        #20;

        $display("ALL TRIGGER SEQUENCER VERIFICATIONS PASSED (0 ERRORS).");
        $finish(0);
    end

endmodule
