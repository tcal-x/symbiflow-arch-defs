add_file_target(FILE counter.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_zybo
  BOARD zybo
  SOURCES counter.v
  INPUT_IO_FILE ${COMMON}/zybo.pcf
  EXPLICIT_ADD_FILE_TARGET
  )

add_vivado_target(
    NAME counter_zybo_vivado
    PARENT_NAME counter_zybo
    CLOCK_PINS clk
    CLOCK_PERIODS 10.0
    # TODO: https://github.com/SymbiFlow/symbiflow-arch-defs/issues/1183
    DISABLE_DIFF_TEST
    )

add_file_target(FILE counter_basys3.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_basys3
  BOARD basys3-full
  SOURCES counter_basys3.v
  INPUT_IO_FILE ${COMMON}/basys3.pcf
  EXPLICIT_ADD_FILE_TARGET
  )

add_vivado_target(
    NAME counter_basys3_vivado
    PARENT_NAME counter_basys3
    CLOCK_PINS clk
    CLOCK_PERIODS 10.0
    # TODO: https://github.com/SymbiFlow/symbiflow-arch-defs/issues/1018
    #DISABLE_DIFF_TEST
    )

add_file_target(FILE counter_arty.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_arty
  BOARD arty-swbut
  SOURCES counter_arty.v
  INPUT_IO_FILE ${COMMON}/arty_swbut.pcf
  EXPLICIT_ADD_FILE_TARGET
)

add_file_target(FILE counter_arty_bufg.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_arty100t
  BOARD arty100t-full
  SOURCES counter_arty_bufg.v
  INPUT_IO_FILE ${COMMON}/arty_swbut.pcf
  EXPLICIT_ADD_FILE_TARGET
)

add_vivado_target(
  NAME counter_arty100t_vivado
  PARENT_NAME counter_arty100t
)


add_file_target(FILE counter_nexys_video.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_nexys_video
  BOARD nexys_video
  SOURCES counter_nexys_video.v
  INPUT_IO_FILE ${COMMON}/nexys_video.pcf
  INPUT_XDC_FILE ${COMMON}/nexys_video.xdc
  EXPLICIT_ADD_FILE_TARGET
)

add_vivado_target(
    NAME counter_nexys_video_vivado
    PARENT_NAME counter_nexys_video
    CLOCK_PINS clk
    CLOCK_PERIODS 10.0
)

#add_file_target(FILE counter_zedboard.v SCANNER_TYPE verilog)
#add_fpga_target(
#  NAME counter_zedboard
#  BOARD zedboard-full
#  SOURCES counter_zedboard.v
#  INPUT_IO_FILE ../common/zedboard.pcf
#  EXPLICIT_ADD_FILE_TARGET
#)

#add_vivado_target(
#  NAME counter_zedboard_vivado
#  PARENT_NAME counter_zedboard
#)

#add_file_target(FILE counter_microzed.v SCANNER_TYPE verilog)

#add_fpga_target(
#  NAME counter_microzed
#  BOARD microzed-full
#  SOURCES counter_microzed.v
#  EXPLICIT_ADD_FILE_TARGET
#)

#add_vivado_target(
#  NAME counter_microzed_vivado
#  PARENT_NAME counter_microzed
#)

add_file_target(FILE counter_pynqz1.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_pynqz1
  BOARD pynqz1-full
  SOURCES counter_pynqz1.v
  INPUT_IO_FILE ../common/pynqz1.pcf
  EXPLICIT_ADD_FILE_TARGET
)

add_file_target(FILE counter_zybo_z7.v SCANNER_TYPE verilog)
add_fpga_target(
  NAME counter_zybo_z7
  BOARD zybo-z7-20
  SOURCES counter_zybo_z7.v
  INPUT_IO_FILE ../common/zybo_z7.pcf
  EXPLICIT_ADD_FILE_TARGET
)

add_vivado_target(
  NAME counter_pynqz1_vivado
  PARENT_NAME counter_pynqz1
)
