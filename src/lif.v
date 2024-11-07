module lif (
    input wire [11:0]    current,
    input wire          clk,
    input wire          reset_n,
    output reg [7:0]    state,
    output wire         spike
);
    reg [7:0]    adapt_threshold;  // Temporarily exposed for testing
    reg [7:0]    spike_counter;     // Temporarily exposed for testing
    wire [7:0] next_state;
    reg [7:0] threshold;

    always @(posedge clk) begin
        if (!reset_n) begin
            state <= 0;
            threshold <= 50;
            adapt_threshold <= 250;  // Start adapt_threshold higher to see decay
            spike_counter <= 0;
        end else begin
            state <= next_state;
            
            // Adapt threshold increase upon spiking
            if (spike) begin
                if (adapt_threshold < 170) begin
                    adapt_threshold <= adapt_threshold + (state >> 2); // Increment proportional to current
                    spike_counter <= 0;  // Reset counter on spike
                end else begin
                    spike_counter <= 0;  // Reset counter on spike
                end
            end else begin
                spike_counter <= spike_counter + 1;  // Increment counter each cycle without spike
            end

            // Decay adapt_threshold over time if it's greater than base threshold
            if (spike_counter > 5 && adapt_threshold > threshold)
                adapt_threshold <= adapt_threshold - (1 + (spike_counter >> 3)); // Decay rate increases over time
        end
    end

    wire [11:0] scaled_state;  // Intermediate 12-bit result for scaling
    assign scaled_state = (state * 14) >> 4;

    wire [11:0] sum = current + scaled_state; // 12-bit addition
    assign next_state = (sum > 12'h0FF) ? 8'hFF : sum[7:0];

    assign spike = (state >= adapt_threshold);

endmodule


// module lif (
//     input wire [7:0]    current,
//     input wire          clk,
//     input wire          reset_n,
//     output reg [7:0]    state,
//     output wire         spike
// );

//     wire [7:0] next_state;
//     reg [7:0] threshold;
//     reg [7:0] adapt_threshold;  // Adaptive threshold

//     always @(posedge clk) begin
//         if (!reset_n) begin
//             state <= 0;
//             threshold <= 200;
//             adapt_threshold <= 250;  // Start adapt_threshold higher to see decay
//         end else begin
//             state <= next_state;
//             // Decay adapt_threshold over time if it's greater than base threshold
//             if (adapt_threshold > threshold)
//                 adapt_threshold <= adapt_threshold - 1;
//         end
//     end

//     // next state logic
//     assign next_state = current + (state >> 1);

//     // spiking logic with adaptive threshold
//     assign spike = (state >= adapt_threshold);

// endmodule




// /*
//  * Copyright (c) 2024 Your Name
//  * SPDX-License-Identifier: Apache-2.0
//  */

// `default_nettype none

// module lif (
//     input wire [7:0]    current,
//     input wire          clk,
//     input wire          reset_n,
//     output reg [7:0]    state,
//     output wire         spike
// );

//     wire [7:0] next_state;
//     reg [7:0] threshold;

//     always @(posedge clk) begin
        
//         if (!reset_n) begin
//             state <= 0;
//             threshold <= 200;
//         end else begin
//             state <= next_state;
//         end
//     end

//     // next state logic
//     assign next_state = current + (state >> 1);

//     // spiking logic
//     assign spike = (state >= threshold);


// endmodule