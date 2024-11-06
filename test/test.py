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

    dut.rst_n.value = 0  # low to reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1  # take out of reset

    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    dut.ui_in.value = 101
    await ClockCycles(dut.clk, 300)

    await ClockCycles(dut.clk, 20)
    assert dut.uio_out.value == 128

    dut._log.info("finished test wawaweewa!!")
