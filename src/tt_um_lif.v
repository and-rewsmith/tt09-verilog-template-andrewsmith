`default_nettype none

module tt_um_lif (
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

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, 1'b0};

    // Generate noisy variations of ui_in for each neuron
    wire [11:0] noisy_input1 = {4'b0000, ui_in} + 12'h0B;
    wire [11:0] noisy_input2 = {4'b0000, ui_in} + 12'h14;
    wire [11:0] noisy_input3 = {4'b0000, ui_in} + 12'h0A;
    wire [11:0] noisy_input4 = {4'b0000, ui_in} + 12'h13;
    wire [11:0] noisy_input5 = {4'b0000, ui_in} + 12'h0D;  // New noise values
    wire [11:0] noisy_input6 = {4'b0000, ui_in} + 12'h16;
    wire [11:0] noisy_input7 = {4'b0000, ui_in} + 12'h0C;
    wire [11:0] noisy_input8 = {4'b0000, ui_in} + 12'h15;

    // Internal states and spike outputs for all neurons
    wire [7:0] state1, state2, state3, state4;
    wire [7:0] state5, state6, state7, state8;
    wire spike1, spike2, spike3, spike4;
    wire spike5, spike6, spike7, spike8;

    // Instantiate all eight LIF neurons
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
    
    lif lif4 (
        .current(noisy_input4),
        .clk(clk),
        .reset_n(rst_n),
        .state(state4),
        .spike(spike4)
    );
    
    lif lif5 (
        .current(noisy_input5),
        .clk(clk),
        .reset_n(rst_n),
        .state(state5),
        .spike(spike5)
    );
    
    lif lif6 (
        .current(noisy_input6),
        .clk(clk),
        .reset_n(rst_n),
        .state(state6),
        .spike(spike6)
    );
    
    lif lif7 (
        .current(noisy_input7),
        .clk(clk),
        .reset_n(rst_n),
        .state(state7),
        .spike(spike7)
    );
    
    lif lif8 (
        .current(noisy_input8),
        .clk(clk),
        .reset_n(rst_n),
        .state(state8),
        .spike(spike8)
    );
    
    // Route all spike outputs to uio_out
    assign uio_out = {spike1, spike2, spike3, spike4, spike5, spike6, spike7, spike8};
    
    // Route one of the neuron's states to uo_out for testing
    // You could modify this to multiplex between different neurons' states if needed
    assign uo_out = state1;


endmodule