# Quick Start

## Basic Usage

Here's a simple example of running a DFT calculation with CP2K:

```python
from ase.build import molecule
from cp2k_plugin import CP2K

atoms = molecule('H2')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)
energy = atoms.get_potential_energy()
forces = atoms.get_forces()

print(f"Energy: {energy:.3f} eV")
print(f"Forces:\n{forces}")
```

## Geometry Optimization

```python
from ase.build import molecule
from ase.optimize import BFGS
from cp2k_plugin import CP2K

atoms = molecule('H2O')
atoms.center(vacuum=5.0)

atoms.calc = CP2K(xc='PBE', cutoff=400)
opt = BFGS(atoms)
opt.run(fmax=0.01)

print(f"Optimized positions:\n{atoms.positions}")
```

## Molecular Dynamics

```python
from ase.build import molecule
from ase.md.verlet import VelocityVerlet
from ase.md import MDLogger
from cp2k_plugin import CP2K

atoms = molecule('H2')
atoms.center(vacuum=5.0)
atoms.set_temperature(300)

atoms.calc = CP2K(xc='PBE', cutoff=400)

dyn = VelocityVerlet(atoms, timestep=1.0)
dyn.attach(MDLogger(dyn, atoms, 'md.traj'))
dyn.run(100)
```

## Using the Plugin System

You can also access the CP2K calculator through ASE's plugin system:

```python
from ase._4.plugins import plugins

calc_cls = plugins.calculators['cp2k'].implementation()
atoms.calc = calc_cls(xc='PBE')
```

## Context Manager

Use the context manager for automatic cleanup:

```python
from ase.build import molecule
from cp2k_plugin import CP2K

atoms = molecule('H2')

with CP2K(xc='PBE', cutoff=400) as calc:
    atoms.calc = calc
    energy = atoms.get_potential_energy()

print(f"Energy: {energy:.3f} eV")
```