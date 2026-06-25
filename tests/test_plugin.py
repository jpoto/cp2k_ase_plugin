"""Unit test for cp2k import and plugin registration."""

import pytest


def test_import_calculators():
    """Test that the CP2K calculator can be imported."""
    from cp2k_plugin import CP2K

    assert CP2K is not None


def test_plugin_registration():
    """Test that the plugin is registered."""
    from cp2k_plugin import _ase_plugin

    assert len(_ase_plugin.__ase_plugins__) == 1
    plugin = list(_ase_plugin.__ase_plugins__)[0]
    assert plugin.name == "cp2k"


def test_plugin_attributes():
    """Test that the plugin has required attributes."""
    from cp2k_plugin import _ase_plugin

    plugin = list(_ase_plugin.__ase_plugins__)[0]
    assert plugin.name == "cp2k"
    assert plugin.long_name == "CP2K Quickstep DFT Code"
    assert "Iannuzzi" in plugin.citation or "CP2K" in plugin.citation
    assert plugin.configurable is True


def test_ase_plugin_discovery():
    """Test that the plugin is discoverable via ASE."""
    from ase._4.plugins import plugins

    cp2ks = [p for p in plugins.calculators if p.name == "cp2k"]
    assert len(cp2ks) >= 1


def test_implementation_class():
    """Test that the implementation is a class (not a string)."""
    from cp2k_plugin import _ase_plugin

    plugin = list(_ase_plugin.__ase_plugins__)[0]
    assert hasattr(plugin, "implementation")
    assert plugin.implementation is not None
