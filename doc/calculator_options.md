# Calculator Options

## Basic Parameters

### `xc`
Exchange-correlation functional. Default is `PBE`.

```python
calc = CP2K(xc='PBE')  # Options: LDA, PBE, BLYP, HFX, etc.
```

### `cutoff`
Plane-wave cutoff energy. Default is `400 * Rydberg`.

```python
calc = CP2K(cutoff=600)  # in Rydberg
```

### `basis_set`
Basis set name. Default is `DZVP-MOLOPT-SR-GTH`.

```python
calc = CP2K(basis_set='TZV2P-MOLOPT-GTH')
```

### `potential`
Pseudopotential. Default is `GTH-PBE`.

```python
calc = CP2K(potential='GTH-PBE')
```

### `charge`
Total system charge. Default is `0`.

```python
calc = CP2K(charge=-1)  # Anion
```

### `multiplicity`
Spin multiplicity. Default is `None` (auto-detect).

```python
calc = CP2K(multiplicity=1)  # Singlet
```

## Calculation Mode

### `force_eval_method`
Method for energy and force evaluation. Default is `Quickstep`.

```python
calc = CP2K(force_eval_method='Quickstep')
```

### `max_scf`
Maximum number of SCF iterations. Default is `50`.

```python
calc = CP2K(max_scf=100)
```

### `stress_tensor`
Calculate stress tensor. Default is `False`.

```python
calc = CP2K(stress_tensor=True)
```

## Parallelization

### `command`
Command to run CP2K shell.

```python
calc = CP2K(command="mpirun -n 4 cp2k.psmp -s")
```

### `nworkers`
Number of workers for parallel calculations. Default is `1`.

```python
calc = CP2K(nworkers=4)
```

## Output Control

### `print_level`
Verbosity of output. Options: `SILENT`, `LOW`, `MEDIUM`, `HIGH`. Default is `MEDIUM`.

```python
calc = CP2K(print_level='LOW')
```

### `label`
Prefix for output files. Default is `cp2k`.

```python
calc = CP2K(label='my_calc')
```

### `directory`
Directory for calculation files. Default is current directory.

```python
calc = CP2K(directory='calc_results')
```

## Input Template

### `inp`
Custom CP2K input template.

```python
calc = CP2K(inp="""
&FORCE_EVAL
   METHOD Quickstep
   &DFT
      &XC
         &XC_FUNCTIONAL LDA
      &END
   &END
&END
""")
```

## Complete Example

```python
from ase.build import molecule
from cp2k import CP2K

atoms = molecule('CH3OH')
atoms.center(vacuum=8.0)

calc = CP2K(
    xc='PBE',
    cutoff=600,
    basis_set='DZVP-MOLOPT-SR-GTH',
    potential='GTH-PBE',
    max_scf=100,
    charge=0,
    multiplicity=None,
    command="mpirun -n 4 cp2k.psmp -s",
    print_level='MEDIUM',
    label='methanol',
    directory='methanol_calc',
)

atoms.calc = calc
energy = atoms.get_potential_energy()
```
