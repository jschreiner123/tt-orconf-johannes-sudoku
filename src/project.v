/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_sudoku (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  reg [4:0] reg_array [8:0][8:0];
  reg [4:0] current_col;
  reg [4:0] current_row;

  wire number_valid;
  wire [3:0] number;
  assign number_valid = ui_in[4];
  assign number = ui_in[3:0];

  integer i, j;
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      integer i, j;
      for (i = 0; i < 9; i = i + 1) begin
        for (j = 0; j < 9; j = j + 1) begin
          reg_array[i][j] <= 5'b0000; // Fixed value
        end
      end
      current_col <= 0;
      current_row <= 0;
    end else begin
      if(number_valid) begin
        reg_array[current_row][current_col] <= number;
        current_col <= (current_col + 1) % 9;
        current_row <= current_col == 9 ? current_row + 1 : current_row;
      end
    end
  end

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in - uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
