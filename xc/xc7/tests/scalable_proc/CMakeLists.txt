
add_file_target(FILE top_arty100t.v SCANNER_TYPE verilog)
add_file_target(FILE processing_unit.v SCANNER_TYPE verilog)
add_file_target(FILE scalable_proc.v SCANNER_TYPE verilog)
add_file_target(FILE simpleuart.v SCANNER_TYPE verilog)
add_file_target(FILE rom_bram36.v SCANNER_TYPE verilog)

add_fpga_target(
  NAME scalable_proc_arty100t
  BOARD arty100t-full
  SOURCES 
    top_arty100t.v
    processing_unit.v
    scalable_proc.v
    simpleuart.v
    rom_bram36.v
  INPUT_IO_FILE ${COMMON}/arty.pcf
  EXPLICIT_ADD_FILE_TARGET
)

add_vivado_target(
  NAME scalable_proc_arty100t_vivado
  PARENT_NAME scalable_proc_arty100t
)
