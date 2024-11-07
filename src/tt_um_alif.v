`default_nettype none

module tt_um_alif (
    input  wire [7:0] ui_in,     // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,       // always 1 when the design is powered, so you can ignore it
    input  wire       clk,       // clock
    input  wire       rst_n      // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_oe  = 1;            // Set all IOs as outputs
  assign uio_out[4:0] = 0;       // Assign unused output pins to 0

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, 1'b0};

  // Generate noisy variations of uio_in
  wire [11:0] noisy_input1 = {4'b0000, ui_in} + 12'h0B;  // Add a small value as "noise"
  wire [11:0] noisy_input2 = {4'b0000, ui_in} + 12'h14;  // Add a different small value for second "noise"
  wire [11:0] noisy_input3 = {4'b0000, ui_in} + 12'h0A;  // Add a different small value for second "noise"

  // Instantiate two LIF neurons with noisy inputs
  wire [7:0] state1, state2, state3;     // Internal states of the neurons
  wire spike1, spike2, spike3;            // Spike outputs from the neurons

  lif lif1 (
      .current(noisy_input1),
      .clk(clk),
      .reset_n(rst_n),
      .state(state1),
      .spike(spike1)
  );

  lif lif2 (
      .current(noisy_input2),
      .clk(clk),
      .reset_n(rst_n),
      .state(state2),
      .spike(spike2)
  );

  lif lif3 (
      .current(noisy_input3),
      .clk(clk),
      .reset_n(rst_n),
      .state(state3),
      .spike(spike3)
  );

  // Route spike outputs to specific bits of uio_out
  assign uio_out[7] = spike1;
  assign uio_out[6] = spike2;
  assign uio_out[5] = spike3;

  // route internal states to `uo_out` for tests
  assign uo_out = state1; 

endmodule