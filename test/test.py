
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_reset_behavior(dut):
    """Test that state resets correctly and spike is low after reset"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Apply reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Check that state is reset and spike is low (uio_out should be 0)
    assert dut.uo_out.value == 0, "State (uo_out) should be 0 after reset"
    assert dut.uio_out.value == 0, "Spike (uio_out[7]) should be low after reset"


@cocotb.test()
async def test_spiking_with_adaptation_low_input(dut):
    """Test spiking behavior with adaptation by providing low sustained input"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set a low input current to induce spiking
    dut.ui_in.value = 10
    spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        if (dut.uio_out.value & 0b11000000) != 0:
            spike_count += 1
        await ClockCycles(dut.clk, 5)  # Space out sampling

    # Ensure that spiking occurred initially, indicating that input triggered the neuron
    assert spike_count > 0, "Neuron should spike with sustained high input"


@cocotb.test()
async def test_spiking_with_adaptation_high_input(dut):
    """Test spiking behavior with adaptation by providing low sustained input"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set a high input current to induce spiking
    dut.ui_in.value = 180
    spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            spike_count += 1
        await ClockCycles(dut.clk, 5)  # Space out sampling

    # Ensure that spiking occurred initially, indicating that input triggered the neuron
    assert spike_count > 0, "Neuron should spike with sustained high input"


@cocotb.test()
async def test_adaptive_threshold_decay_indirect(dut):
    """Indirectly test that adapt_threshold decays over time by observing spike activity with no input"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Reset and initialize
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set no input current to prevent immediate spiking
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 64)  # Increase wait time to allow more decay

    # Apply a moderate input to observe if the neuron now spikes more easily
    dut.ui_in.value = 80  # Increase the input value to a higher moderate level
    spike_count = 0
    for _ in range(100):  # Increase observation period for spiking
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            spike_count += 1
        await ClockCycles(dut.clk, 5)

    # We expect at least one spike due to decay in adapt_threshold over time
    assert spike_count > 0, "Neuron should spike after decay of adapt_threshold with moderate input"


@cocotb.test()
async def test_saturation_behavior(dut):
    """Test that state does not exceed the 8-bit maximum (255) with high input current"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set a very high input to see if saturation is handled
    dut.ui_in.value = 255
    await ClockCycles(dut.clk, 50)  # Run for a number of cycles to observe

    # Ensure that state does not exceed 255
    assert dut.uo_out.value == "11111111", "State should not exceed 255 due to saturation"


@cocotb.test()
async def test_low_medium_high_current_levels(dut):
    """Test the neuron with low, medium, and high current levels to observe spiking and adaptation"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Initial conditions
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Test low current
    dut.ui_in.value = 10
    low_spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            low_spike_count += 1
        await ClockCycles(dut.clk, 5)

    # Test high current
    dut.ui_in.value = 180
    high_spike_count = 0
    for _ in range(50):
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            high_spike_count += 1
        await ClockCycles(dut.clk, 5)

    # Assertions to ensure expected spiking frequency based on input level
    assert low_spike_count < high_spike_count, (
        "Spiking frequency should increase with higher input current levels"
    )


@cocotb.test()
async def test_threshold_decay_via_spike_frequency(dut):
    """Test that adapt_threshold decays over time by observing an increase in spike frequency"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    # Initial reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set moderate input current to induce initial spikes without reaching saturation
    dut.ui_in.value = 10

    # Measure spike frequency in the first interval (before decay)
    initial_spike_count = 0
    for _ in range(50):  # First interval for initial spike count
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            initial_spike_count += 1
        await ClockCycles(dut.clk, 5)

    # Measure spike frequency in the second interval (after decay)
    later_spike_count = 0
    for _ in range(50):  # Second interval for spike count after threshold decay
        await ClockCycles(dut.clk, 1)
        if dut.uio_out.value.integer >= 64:  # Check if spike is high
            later_spike_count += 1
        await ClockCycles(dut.clk, 5)

    # Assert that the spiking frequency increased in the second interval
    assert later_spike_count > initial_spike_count, (
        "Spiking frequency should increase over time as adapt_threshold decays"
    )


@cocotb.test()
async def test_dual_neurons(dut):
    """Test that both neurons respond to the input and produce spikes based on noisy inputs"""
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ui_in.value = 0

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Set the input current for both neurons via ui_in
    dut.ui_in.value = 50  # A moderate input current that should allow spikes with adaptation
    spike1_count = 0
    spike2_count = 0

    for _ in range(100):  # Observe behavior over 100 cycles
        await ClockCycles(dut.clk, 10)

        # Check for spikes on both neurons
        if dut.uio_out.value & 0b10000000:  # Spike from lif1 (uio_out[7])
            spike1_count += 1

        if dut.uio_out.value & 0b01000000:  # Spike from lif2 (uio_out[6])
            spike2_count += 1

        await ClockCycles(dut.clk, 5)  # Space out sampling

    # Simple assertions to confirm both neurons are responsive
    assert spike1_count > 0, "Neuron 1 (lif1) should produce spikes with the input current"
    assert spike2_count > 0, "Neuron 2 (lif2) should produce spikes with the input current"
    assert abs(spike1_count - spike2_count) <= 10, (
        "Both neurons should have similar spike counts due to similar noisy inputs"
    )
