# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_basic(dut):
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


@cocotb.test()
async def test_reset(dut):
    """Test that state and spike are reset correctly"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Check if state is zero and spike is low after reset
    assert dut.uo_out.value == 0, "State is not zero after reset"
    assert dut.uio_out.value == 0, "Spike is not low after reset"


@cocotb.test()
async def test_below_threshold(dut):
    """Test that spike does not trigger when state is just below the threshold"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set input just below the threshold
    dut.ui_in.value = 150
    await ClockCycles(dut.clk, 20)  # Let the state accumulate

    # Check if spike is low (state < threshold)
    assert dut.uio_out.value == 0, "Spike should be low when state is below threshold"


@cocotb.test()
async def test_at_threshold(dut):
    """Test that spike triggers when state reaches the threshold"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set input that brings state to threshold level
    dut.ui_in.value = 200
    await ClockCycles(dut.clk, 20)  # Let state accumulate and potentially spike

    # Check if spike is high (state >= threshold)
    assert dut.uio_out.value == 128, "Spike should be high when state reaches threshold"


@cocotb.test()
async def test_stable_below_threshold(dut):
    """Test that state stabilizes below the threshold without spiking"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Use a small current value
    dut.ui_in.value = 50
    await ClockCycles(dut.clk, 200)  # Allow state to stabilize below threshold

    # Check that spike is still low and state is stable
    assert dut.uio_out.value == 0, "Spike should be low if state is below threshold"
    dut._log.info("Stable below threshold test passed without spiking.")
