
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_reset_behavior(dut):
#     """Test that state resets correctly and spike is low after reset"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Apply reset
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 1)

#     # Check that state is reset and spike is low (uio_out should be 0)
#     assert dut.uo_out.value == 0, "State (uo_out) should be 0 after reset"
#     assert dut.uio_out.value == 0, "Spike (uio_out[7]) should be low after reset"


# @cocotb.test()
# async def test_spiking_with_adaptation(dut):
#     """Test spiking behavior with adaptation by providing low sustained input"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Initial conditions
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set a low input current to induce spiking
#     dut.ui_in.value = 10
#     spike_count = 0
#     for _ in range(50):
#         await ClockCycles(dut.clk, 1)
#         if dut.uio_out.value == 128:  # Check if spike is high
#             spike_count += 1
#         await ClockCycles(dut.clk, 5)  # Space out sampling

#     # Ensure that spiking occurred initially, indicating that input triggered the neuron
#     assert spike_count > 0, "Neuron should spike with sustained high input"


@cocotb.test()
async def test_spiking_with_adaptation(dut):
    """Test spiking behavior with adaptation by providing low sustained input"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set a high input current to induce spiking
    dut.ui_in.value = 180
    spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value == 128:  # Check if spike is high
            spike_count += 1
        await ClockCycles(dut.clk, 5)  # Space out sampling

    # Ensure that spiking occurred initially, indicating that input triggered the neuron
    assert spike_count > 0, "Neuron should spike with sustained high input"

# @cocotb.test()
# async def test_spiking_with_adaptation(dut):
#     """Test spiking behavior with adaptation by providing sustained input"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Initial conditions
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set a high input current to induce spiking
#     dut.ui_in.value = 180
#     spike_count = 0
#     for _ in range(50):
#         await ClockCycles(dut.clk, 1)
#         if dut.uio_out[7].value == 1:
#             spike_count += 1
#         await ClockCycles(dut.clk, 5)  # Space out sampling

#     # Ensure that spiking occurred initially, indicating that input triggered the neuron
#     assert spike_count > 0, "Neuron should spike with sustained high input"
#     # With adaptation, spiking frequency should eventually reduce


# @cocotb.test()
# async def test_state_decay(dut):
#     """Test that state decays gradually when there is no input"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Initial conditions
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Apply a current to increase state
#     dut.ui_in.value = 100
#     await ClockCycles(dut.clk, 20)  # Allow state to increase

#     # Check initial state
#     initial_state = dut.uo_out.value.integer
#     dut.ui_in.value = 0  # Set current to zero to observe decay
#     await ClockCycles(dut.clk, 10)

#     # Ensure state decays (but not too quickly due to 90% retention)
#     assert dut.uo_out.value < initial_state, "State should decay when current is zero"
#     assert dut.uo_out.value > (initial_state * 0.85), "State decay should be gradual (around 90% retention)"


# @cocotb.test()
# async def test_sustained_high_input_behavior(dut):
#     """Test sustained high input and observe initial spiking with adaptation reducing it over time"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Initial conditions
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set a high sustained current
#     dut.ui_in.value = 180
#     initial_spike_count = 0
#     subsequent_spike_count = 0

#     # Observe spiking over two intervals to check adaptation effect
#     for _ in range(20):
#         await ClockCycles(dut.clk, 1)
#         if dut.uio_out[7].value == 1:
#             initial_spike_count += 1
#         await ClockCycles(dut.clk, 5)  # Space out sampling

#     # With adaptation, we expect fewer spikes in the next interval
#     for _ in range(20):
#         await ClockCycles(dut.clk, 1)
#         if dut.uio_out[7].value == 1:
#             subsequent_spike_count += 1
#         await ClockCycles(dut.clk, 5)

#     assert initial_spike_count > subsequent_spike_count, (
#         "Spiking frequency should decrease over time with sustained input due to adaptation"
#     )


# # SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# # SPDX-License-Identifier: Apache-2.0

# import cocotb
# from cocotb.clock import Clock
# from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_reset_behavior(dut):
#     """Test that state, adapt_threshold, and spike_counter reset correctly"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Apply reset
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 1)

#     assert dut.state.value == 0, "State should be 0 after reset"
#     assert dut.adapt_threshold.value == 250, "Adaptive threshold should be initialized to 250"
#     assert dut.spike_counter.value == 0, "Spike counter should be 0 after reset"


# @cocotb.test()
# async def test_basic(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     dut.rst_n.value = 0  # low to reset
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1  # take out of reset

#     dut.ui_in.value = 0
#     await ClockCycles(dut.clk, 10)

#     dut.ui_in.value = 101
#     await ClockCycles(dut.clk, 300)

#     await ClockCycles(dut.clk, 20)
#     assert dut.uio_out.value == 128

#     dut._log.info("finished test wawaweewa!!")


# @cocotb.test()
# async def test_reset(dut):
#     """Test that state and spike are reset correctly"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Apply reset
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Check if state is zero and spike is low after reset
#     assert dut.uo_out.value == 0, "State is not zero after reset"
#     assert dut.uio_out.value == 0, "Spike is not low after reset"


# @cocotb.test()
# async def test_below_threshold(dut):
#     """Test that spike does not trigger when state is just below the threshold"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set input just below the threshold
#     dut.ui_in.value = 150
#     await ClockCycles(dut.clk, 20)  # Let the state accumulate

#     # Check if spike is low (state < threshold)
#     assert dut.uio_out.value == 0, "Spike should be low when state is below threshold"


# @cocotb.test()
# async def test_at_threshold(dut):
#     """Test that spike triggers when state reaches the threshold"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set input that brings state to threshold level
#     dut.ui_in.value = 200
#     await ClockCycles(dut.clk, 20)  # Let state accumulate and potentially spike

#     # Check if spike is high (state >= threshold)
#     assert dut.uio_out.value == 128, "Spike should be high when state reaches threshold"


# @cocotb.test()
# async def test_stable_below_threshold(dut):
#     """Test that state stabilizes below the threshold without spiking"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Use a small current value
#     dut.ui_in.value = 50
#     await ClockCycles(dut.clk, 200)  # Allow state to stabilize below threshold

#     # Check that spike is still low and state is stable
#     assert dut.uio_out.value == 0, "Spike should be low if state is below threshold"
#     dut._log.info("Stable below threshold test passed without spiking.")
