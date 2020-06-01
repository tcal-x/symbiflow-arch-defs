module top
(
input  wire         clk,

output wire         ser_tx,
input  wire         ser_rx,

input  wire [3:0]  sw,
output wire [3:0]  led
);

// ============================================================================

reg rst = 1;
reg rst1 = 1;
reg rst2 = 1;
reg rst3 = 1;
assign led[0] = rst;
assign led[1] = sw[1];
assign led[2] = sw[2];
assign led[3] = ser_rx;

IBUF clk_ibuf(.I(clk),      .O(clk_ibuf));
BUFG clk_bufg(.I(clk_ibuf), .O(clk_b));


always @(posedge clk_b) begin
rst3 <= 0;
rst2 <= rst3;
rst1 <= rst2;
rst <= rst1;
end

// ============================================================================
//
scalable_proc #
(
.NUM_PROCESSING_UNITS   (150),
.UART_PRESCALER         ((100000000) / (500000))
)
scalable_proc
(
.CLK        (clk_b),
.RST        (rst),

.UART_TX    (ser_tx),
.UART_RX    (ser_rx)
);

endmodule
