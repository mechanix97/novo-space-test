/* Generated by Yosys 0.9+4052 (git sha1 32a0ce9d, gcc 7.5.0-3ubuntu1~18.04 -fPIC -Os) */

(* generator = "nMigen" *)
(* top =  1  *)
(* \nmigen.hierarchy  = "top" *)
module top(dat_r, dat_w, we, clk, rst, adr);
  (* src = "generate.py:7" *)
  input [3:0] adr;
  (* src = "/home/lucas/.local/lib/python3.6/site-packages/nmigen/hdl/ir.py:526" *)
  input clk;
  (* src = "generate.py:8" *)
  output [7:0] dat_r;
  (* src = "generate.py:9" *)
  input [7:0] dat_w;
  (* src = "generate.py:15" *)
  wire [3:0] mem_r_addr;
  (* src = "generate.py:15" *)
  wire [7:0] mem_r_data;
  (* src = "generate.py:16" *)
  wire [3:0] mem_w_addr;
  (* src = "generate.py:16" *)
  wire [7:0] mem_w_data;
  (* src = "generate.py:16" *)
  wire mem_w_en;
  (* src = "/home/lucas/.local/lib/python3.6/site-packages/nmigen/hdl/ir.py:526" *)
  input rst;
  (* src = "generate.py:10" *)
  input we;
  reg [7:0] mem [15:0];
  initial begin
    mem[0] = 8'hb7;
    mem[1] = 8'h50;
    mem[2] = 8'h60;
    mem[3] = 8'h70;
    mem[4] = 8'ha2;
    mem[5] = 8'h0d;
    mem[6] = 8'hb3;
    mem[7] = 8'hd8;
    mem[8] = 8'h64;
    mem[9] = 8'h7b;
    mem[10] = 8'hb9;
    mem[11] = 8'hca;
    mem[12] = 8'h59;
    mem[13] = 8'h6c;
    mem[14] = 8'h24;
    mem[15] = 8'h5c;
  end
  reg [3:0] _0_;
  always @(posedge clk) begin
    _0_ <= mem_r_addr;
    if (mem_w_en) mem[mem_w_addr] <= mem_w_data;
  end
  assign mem_r_data = mem[_0_];
  assign mem_w_en = we;
  assign mem_w_data = dat_w;
  assign mem_w_addr = adr;
  assign dat_r = mem_r_data;
  assign mem_r_addr = adr;
endmodule
