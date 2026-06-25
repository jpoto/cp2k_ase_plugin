"""Tests for the CP2K ASE calculator.

http://www.cp2k.org
Author: Ole Schuett <ole.schuett@mat.ethz.ch>
Author: Johann Pototschnig <j.pototschnig@hzdr.de>
"""

import os
import tempfile

import pytest

from ase import units
from ase.atoms import Atoms
from ase.build import molecule
from ase.calculators.calculator import CalculatorSetupError
from ase.md import thermalize_momenta
from ase.md.verlet import VelocityVerlet
from ase.optimize import BFGS

from cp2k_plugin import CP2K


def make_h2():
    h2 = molecule("H2")
    h2.center(vacuum=2.0)
    return h2


def test_geoopt():
    atoms = make_h2()
    with CP2K(label="test_H2_GOPT", print_level="LOW") as calc:
        atoms.calc = calc

        with BFGS(atoms, logfile=None) as gopt:
            gopt.run(fmax=1e-6)

        dist = atoms.get_distance(0, 1)
        dist_ref = 0.7245595
        assert (dist - dist_ref) / dist_ref < 1e-7

        energy_ref = -30.7025616943
        energy = atoms.get_potential_energy()
        assert (energy - energy_ref) / energy_ref < 1e-10


def test_h2_lda():
    atoms = make_h2()
    with CP2K(label="test_H2_LDA") as calc:
        atoms.calc = calc
        energy = atoms.get_potential_energy()
        energy_ref = -30.6989595886
        diff = abs((energy - energy_ref) / energy_ref)
        assert diff < 1e-10


def test_h2_libxc():
    atoms = make_h2()
    with CP2K(
        xc="XC_GGA_X_PBE XC_GGA_C_PBE",
        pseudo_potential="GTH-PBE",
        label="test_H2_libxc",
    ) as calc:
        atoms.calc = calc
        energy = atoms.get_potential_energy()
        energy_ref = -31.591716529642
        diff = abs((energy - energy_ref) / energy_ref)
        assert diff < 1e-10


def test_h2_ls():
    atoms = make_h2()
    inp = """&FORCE_EVAL
              &DFT
                &QS
                  LS_SCF ON
                &END QS
              &END DFT
            &END FORCE_EVAL"""
    with CP2K(label="test_H2_LS", inp=inp) as calc:
        atoms.calc = calc
        energy = atoms.get_potential_energy()
        energy_ref = -30.6989581747
        diff = abs((energy - energy_ref) / energy_ref)
        assert diff < 5e-7


def test_h2_pbe():
    atoms = make_h2()
    with CP2K(xc="PBE", label="test_H2_PBE") as calc:
        atoms.calc = calc
        energy = atoms.get_potential_energy()
        energy_ref = -31.5917284949
        diff = abs((energy - energy_ref) / energy_ref)
        assert diff < 1e-10


def test_md():
    with CP2K(label="test_H2_MD") as calc:
        positions = [(0, 0, 0), (0, 0, 0.7245595)]
        atoms = Atoms("HH", positions=positions, calculator=calc)
        atoms.center(vacuum=2.0)

        thermalize_momenta(atoms, 0.5 * 300.0, exact_temperature=True)
        energy_start = atoms.get_potential_energy() + atoms.get_kinetic_energy()
        with VelocityVerlet(atoms, 0.5 * units.fs) as dyn:
            dyn.run(20)

        energy_end = atoms.get_potential_energy() + atoms.get_kinetic_energy()
        assert abs(energy_start - energy_end) < 1e-4


def test_o2():
    with CP2K(
        label="test_O2",
        uks=True,
        cutoff=150 * units.Rydberg,
        basis_set="SZV-MOLOPT-SR-GTH",
        multiplicity=3,
    ) as calc:
        o2 = molecule("O2", calculator=calc)
        o2.center(vacuum=2.0)
        energy = o2.get_potential_energy()
        energy_ref = -862.8384369579051
        diff = abs((energy - energy_ref) / energy_ref)
        assert diff < 1e-10


def test_restart():
    with tempfile.TemporaryDirectory() as tmpdir:
        atoms = make_h2()
        calc = CP2K(directory=tmpdir)
        atoms.calc = calc
        atoms.get_potential_energy()
        calc.write(os.path.join(tmpdir, "test_restart"))
        calc2 = CP2K(directory=tmpdir, restart=os.path.join(tmpdir, "test_restart"))
        assert not calc2.calculation_required(atoms, ["energy"])
        calc.close()
        calc2.close()


def test_unknown_keywords():
    with pytest.raises(CalculatorSetupError):
        CP2K(dummy_nonexistent_keyword="hello")


def test_close():
    """Ensure we cleanly close the calculator and then restart it"""
    atoms = make_h2()
    with CP2K(label="test_H2_GOPT", print_level="LOW") as calc:
        assert calc._shell is not None
        calc.get_potential_energy(atoms)

        assert calc._shell is not None
        child = calc._shell._child
        calc.close()
        assert child.poll() == 0

        atoms.rattle(0.01)
        calc.get_potential_energy(atoms)
        assert calc._shell is not None


def test_context():
    """Ensure we can use the CP2K shell as a context manager"""
    atoms = make_h2()

    with CP2K(label="test_H2_GOPT", print_level="LOW") as calc:
        atoms.calc = calc
        atoms.get_potential_energy()
        child = calc._shell._child
    assert child.poll() == 0


@pytest.mark.xfail()
def test_set_pos_file():
    """Test passing coordinates via file rather than stdin

    This will pass when testing against a new version of CP2K.
    When that happens, remove the `xfail` decorator
    and change 2024.X in `cp2k.py` to the new version number. -wardlt
    """
    atoms = make_h2()

    with CP2K(label="test_H2_GOPT", print_level="LOW", set_pos_file=True) as calc:
        atoms.calc = calc
        atoms.get_potential_energy()
