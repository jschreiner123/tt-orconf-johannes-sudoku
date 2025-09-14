# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    sudoku = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    for i in range(9):
        for j in range(9):
            dut.ui_in <= (1 << 4) | (sudoku[i][j] & 0xF)  # Set valid bit + 4-bit number
            dut.ui_in.value[4] = 1
            await ClockCycles(dut.clk, 1)
    
    dut.ui_in.value[4] = 0
    await ClockCycles(dut.clk, 1)
    
    dut.ui_in.value[5] = 1  # Trigger check
    await ClockCycles(dut.clk, 1)

    # Verify check is active
    assert dut.uo_out.value[0] == 1  # Check active
    dut._log.info(f"Check started - CHECK_ACTIVE: {dut.uo_out.value[0]}")

    # Wait for the check to complete (wait for sufficient cycles)
    # The check process iterates through all 81 cells, so we need enough cycles
    await ClockCycles(dut.clk, 100)  # Wait for 100 cycles to ensure completion
    
    # Check the status after waiting
    check_active = dut.uo_out.value[0]
    check_done = dut.uo_out.value[1] 
    error_detected = dut.uo_out.value[2]
    
    dut._log.info(f"After waiting - CHECK_ACTIVE: {check_active}, CHECK_DONE: {check_done}, ERROR_DETECTED: {error_detected}")
    
    # Verify the check is completed
    assert check_done == 1, f"Expected CHECK_DONE=1, got {check_done}"
    assert check_active == 0, f"Expected CHECK_ACTIVE=0 (finished), got {check_active}"
    
    # For a valid sudoku solution, we should not have errors
    assert error_detected == 0, f"Expected no errors for valid sudoku, got ERROR_DETECTED={error_detected}"
    
    dut._log.info("Test completed successfully - valid sudoku solution verified")


