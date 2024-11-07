
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


@cocotb.test()
async def test_spiking_with_adaptation_low_input(dut):
    """Test spiking behavior with adaptation by providing low sustained input"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set a low input current to induce spiking
    dut.ui_in.value = 10
    spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        print(dut.uio_out.value)
        if (dut.uio_out.value & 0b11000000) != 0:
            spike_count += 1
        await ClockCycles(dut.clk, 5)  # Space out sampling

    # Ensure that spiking occurred initially, indicating that input triggered the neuron
    assert spike_count > 0, "Neuron should spike with sustained high input"


# @cocotb.test()
# async def test_spiking_with_adaptation_high_input(dut):
#     """Test spiking behavior with adaptation by providing low sustained input"""
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
#         if dut.uio_out.value.integer >= 64:  # Check if spike is high
#             spike_count += 1
#         await ClockCycles(dut.clk, 5)  # Space out sampling

#     # Ensure that spiking occurred initially, indicating that input triggered the neuron
#     assert spike_count > 0, "Neuron should spike with sustained high input"


# @cocotb.test()
# async def test_adaptive_threshold_decay_indirect(dut):
#     """Indirectly test that adapt_threshold decays over time by observing spike activity with no input"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Reset and initialize
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set no input current to prevent immediate spiking
#     dut.ui_in.value = 0
#     await ClockCycles(dut.clk, 64)  # Increase wait time to allow more decay

#     # Apply a moderate input to observe if the neuron now spikes more easily
#     dut.ui_in.value = 80  # Increase the input value to a higher moderate level
#     spike_count = 0
#     for _ in range(100):  # Increase observation period for spiking
#         await ClockCycles(dut.clk, 1)
#         if dut.uio_out.value.integer >= 64:  # Check if spike is high
#             spike_count += 1
#         await ClockCycles(dut.clk, 5)

#     # We expect at least one spike due to decay in adapt_threshold over time
#     assert spike_count > 0, "Neuron should spike after decay of adapt_threshold with moderate input"


# @cocotb.test()
# async def test_saturation_behavior(dut):
#     """Test that state does not exceed the 8-bit maximum (255) with high input current"""
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Initial conditions
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     # Set a very high input to see if saturation is handled
#     dut.ui_in.value = 255
#     await ClockCycles(dut.clk, 50)  # Run for a number of cycles to observe

#     # Ensure that state does not exceed 255
#     assert dut.uo_out.value == "11111111", "State should not exceed 255 due to saturation"


# # @cocotb.test()
# # async def test_low_medium_high_current_levels(dut):
# #     """Test the neuron with low, medium, and high current levels to observe spiking and adaptation"""
# #     clock = Clock(dut.clk, 10, units="us")
# #     cocotb.start_soon(clock.start())

# #     # Initial conditions
# #     dut.rst_n.value = 0
# #     await ClockCycles(dut.clk, 10)
# #     dut.rst_n.value = 1

# #     # Test low current
# #     dut.ui_in.value = 20
# #     low_spike_count = 0
# #     for _ in range(50):
# #         await ClockCycles(dut.clk, 1)
# #         if dut.uio_out.value.integer >= 64:  # Check if spike is high
# #             low_spike_count += 1
# #         await ClockCycles(dut.clk, 5)

# #     # Test medium current
# #     dut.ui_in.value = 100
# #     medium_spike_count = 0
# #     for _ in range(50):
# #         await ClockCycles(dut.clk, 1)
# #         if dut.uio_out.value.integer >= 64:  # Check if spike is high
# #             medium_spike_count += 1
# #         await ClockCycles(dut.clk, 5)

# #     # Test high current
# #     dut.ui_in.value = 180
# #     high_spike_count = 0
# #     for _ in range(50):
# #         await ClockCycles(dut.clk, 1)
# #         if dut.uio_out.value.integer >= 64:  # Check if spike is high
# #             high_spike_count += 1
# #         await ClockCycles(dut.clk, 5)

# #     # Assertions to ensure expected spiking frequency based on input level
# #     assert low_spike_count < medium_spike_count < high_spike_count, (
# #         "Spiking frequency should increase with higher input current levels"
# #     )


# # @cocotb.test()
# # async def test_threshold_decay_via_spike_frequency(dut):
# #     """Test that adapt_threshold decays over time by observing an increase in spike frequency"""
# #     clock = Clock(dut.clk, 10, units="us")
# #     cocotb.start_soon(clock.start())

# #     # Initial reset
# #     dut.rst_n.value = 0
# #     await ClockCycles(dut.clk, 10)
# #     dut.rst_n.value = 1

# #     # Set moderate input current to induce initial spikes without reaching saturation
# #     dut.ui_in.value = 10

# #     # Measure spike frequency in the first interval (before decay)
# #     initial_spike_count = 0
# #     for _ in range(50):  # First interval for initial spike count
# #         await ClockCycles(dut.clk, 1)
# #         if dut.uio_out.value.integer >= 64:  # Check if spike is high
# #             initial_spike_count += 1
# #         await ClockCycles(dut.clk, 5)

# #     # Measure spike frequency in the second interval (after decay)
# #     later_spike_count = 0
# #     for _ in range(50):  # Second interval for spike count after threshold decay
# #         await ClockCycles(dut.clk, 1)
# #         if dut.uio_out.value.integer >= 64:  # Check if spike is high
# #             later_spike_count += 1
# #         await ClockCycles(dut.clk, 5)

# #     # Assert that the spiking frequency increased in the second interval
# #     assert later_spike_count > initial_spike_count, (
# #         "Spiking frequency should increase over time as adapt_threshold decays"
# #     )
