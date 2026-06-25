"""CP2K ASE plugin registration.

This module is loaded through the ``ase.plugins`` entry point and uses the
ASE 4 ``ase._4.plugins`` plugin system for calculator discovery.
"""

from __future__ import annotations

import warnings

try:
    from ase._4.plugins.calculator import CalculatorPlugin
except ImportError:
    warnings.warn(
        "ASE < 4 detected. cp2k requires ASE >= 4. "
        "Plugin registration skipped.",
        UserWarning,
    )

    __ase_plugins__ = set()

else:
    cp2k_plugin = CalculatorPlugin(
        name="cp2k",
        long_name="CP2K Quickstep DFT Code",
        citation=(
            "M. Iannuzzi et al., J. Phys. Chem. B, vol. 130, pp. 1237, 2026, (https://doi.org/10.1021/acs.jpcb.5c05851)\n"
            "CP2K developers (https://www.cp2k.org/)"
        ),
        implementation="cp2k_plugin.cp2k_ase_plugin.CP2K",
        configurable=True,
    )
    __ase_plugins__ = {cp2k_plugin}

