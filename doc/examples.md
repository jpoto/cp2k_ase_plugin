# Examples

## Single Point Calculation

Calculate the energy and forces for a water molecule:

```python
from ase.build import molecule
from cp2k import CP2K

atoms = molecule('H2O')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)

energy = atoms.get_potential_energy()
forces = atoms.get_forces()
stress = atoms.get_stress()

print(f"Energy: {energy:.4f} eV")
print(f"Forces:\n{forces}")
print(f"Stress:\n{stress}")
```

## Geometry Optimization

Optimize the structure of an ethanol molecule:

```python
from ase.build import molecule
from ase.optimize import BFGS
from cp2k import CP2K

atoms = molecule('CH3CH2OH')
atoms.center(vacuum=8.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)

opt = BFGS(atoms, trajectory='opt.traj')
opt.run(fmax=0.01)

print(f"Final energy: {atoms.get_potential_energy():.4f} eV")
print(f"Final positions:\n{atoms.positions}")
```

## Molecular Dynamics

Run ab initio molecular dynamics:

```python
from ase.build import molecule
from ase.md.verlet import VelocityVerlet
from ase.md import MDLogger
from cp2k import CP2K

atoms = molecule('H2')
atoms.center(vacuum=5.0)
atoms.set_temperature(300)

atoms.calc = CP2K(xc='PBE', cutoff=400)

dyn = VelocityVerlet(atoms, timestep=1.0)  # 1 fs
dyn.attach(MDLogger(dyn, atoms, 'md.log'))
dyn.run(100)
```

## NPT Molecular Dynamics

Run NPT ensemble molecular dynamics:

```python
from ase.build import bulk
from ase.md.npt import NPT
from ase.units import fs
from cp2k import CP2K

atoms = bulk('NaCl', 'rocksalt', a=5.64)
atoms.set_temperature(300)

atoms.calc = CP2K(xc='PBE', cutoff=400)

npt = NPT(atoms, timestep=1.0*fs, temperature=300, pressure=1.0)
npt.run(1000)
```

## Band Structure Calculation

Calculate the band structure:

```python
from ase.build import graphene_nanoribbon
from cp2k import CP2K
from ase.dft.band_structure import BandStructure

atoms = graphene_nanoribbon(5, 5, type='armchair')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)

bs = atoms.calc.band_structure()
```

## DOS Calculation

Calculate the density of states:

```python
from ase.build import molecule
from cp2k import CP2K

atoms = molecule('C2H4')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)

dos = atoms.calc.dos(npoints=200)
```

## Vibration Analysis

Calculate vibrational frequencies:

```python
from ase.build import molecule
from ase.vibrations import Vibrations
from cp2k import CP2K

atoms = molecule('H2O')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)

vib = Vibrations(atoms)
vib.run()
vib.summary()
```

## Using Custom Input

Pass custom CP2K input:

```python
from ase.build import molecule
from cp2k import CP2K

atoms = molecule('H2')
atoms.center(vacuum=5.0)

custom_input = """
&FORCE_EVAL
   METHOD Quickstep
   &DFT
      &XC
         &XC_FUNCTIONAL LDA
      &END XC_FUNCTIONAL
      &POISSON
         PERIODIC NONE
         PSOLVER  MT
      &END POISSON
   &END DFT
&END FORCE_EVAL
"""

atoms.calc = CP2K(inp=custom_input)
energy = atoms.get_potential_energy()
```
