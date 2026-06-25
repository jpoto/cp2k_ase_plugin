"""Test DCD file reading for CP2K ASE calculator.

http://www.cp2k.org
Author: Ole Schuett <ole.schuett@mat.ethz.ch>
"""

import os
import subprocess
import tempfile

import numpy as np
import pytest

from ase import io
from ase.build import molecule
from ase.calculators.calculator import compare_atoms
from ase.config import cfg
from ase.io.cp2k import iread_cp2k_dcd

from cp2k_plugin import CP2K

inp = """\
&MOTION
  &PRINT
    &TRAJECTORY SILENT
      FORMAT DCD_ALIGNED_CELL
    &END TRAJECTORY
  &END PRINT
  &MD
    STEPS 5
  &END MD
&END MOTION
&GLOBAL
  RUN_TYPE MD
&END GLOBAL
"""


def test_dcd():
    cp2k_main = cfg.parser.get("cp2k", "cp2k_main", fallback=None)
    if cp2k_main is None:
        pytest.skip("Missing cp2k configuration. Add to ~/.config/ase/config.ini:\n\n[cp2k]\ncp2k_main = env OMP_NUM_THREADS=1 mpiexec -np 4 /path/to/cp2k.psmp")

    with tempfile.TemporaryDirectory() as tmpdir:
        calc = CP2K(directory=tmpdir, label="test_dcd", inp=inp)
        h2 = molecule("H2", calculator=calc)
        h2.center(vacuum=2.0)
        h2.set_pbc(True)
        energy = h2.get_potential_energy()
        assert energy is not None

        subprocess.check_call(
            f"cd {tmpdir} && {cp2k_main} -i test_dcd.inp -o test_dcd.out",
            shell=True,
        )

        dcd_file = os.path.join(tmpdir, "test_dcd-pos-1.dcd")
        h2_end = io.read(dcd_file)
        assert (h2_end.symbols == "X").all()

        traj = io.read(dcd_file, ref_atoms=h2, index=slice(0, None), aligned=True)
        ioITraj = io.iread(dcd_file, ref_atoms=h2, index=slice(0, None), aligned=True)

        with open(dcd_file, "rb") as fd:
            itraj = iread_cp2k_dcd(
                fd, indices=slice(0, None), ref_atoms=h2, aligned=True
            )
            for i, iMol in enumerate(itraj):
                ioIMol = next(ioITraj)
                assert compare_atoms(iMol, traj[i]) == []
                assert compare_atoms(iMol, ioIMol) == []
                assert iMol.get_pbc().all()

        traj = io.read(dcd_file, ref_atoms=h2, index=slice(0, None))
        pbc = [mol.get_pbc() for mol in traj]
        assert not np.any(pbc)