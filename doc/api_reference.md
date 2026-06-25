# API Reference

## CP2K Class

```python
class cp2k.CP2K(
    restart=None,
    directory='.',
    label=None,
    atoms=None,
    command=None,
    xc='PBE',
    basis_set='DZVP-MOLOPT-SR-GTH',
    basis_set_file='BASIS_MOLOPT',
    cutoff=400,
    max_scf=50,
    charge=0.0,
    multiplicity=None,
    potential='GTH-PBE',
    potential_file='POTENTIAL',
    stress_tensor=False,
    force_eval_method='Quickstep',
    poisson_solver=None,
    inp=None,
    print_level='MEDIUM',
    debug=False,
    auto_write=False,
    nworkers=1,
    **kwargs
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `restart` | str | None | Path to restart directory |
| `directory` | str | '.' | Directory for output files |
| `label` | str | None | Prefix for output files |
| `atoms` | Atoms | None | ASE Atoms object |
| `command` | str | None | CP2K command |
| `xc` | str | 'PBE' | Exchange-correlation functional |
| `basis_set` | str | 'DZVP-MOLOPT-SR-GTH' | Basis set name |
| `basis_set_file` | str | 'BASIS_MOLOPT' | Basis set file |
| `cutoff` | float | 400 | Plane-wave cutoff (Rydberg) |
| `max_scf` | int | 50 | Max SCF iterations |
| `charge` | float | 0.0 | System charge |
| `multiplicity` | int | None | Spin multiplicity |
| `potential` | str | 'GTH-PBE' | Pseudopotential |
| `potential_file` | str | 'POTENTIAL' | Potential file |
| `stress_tensor` | bool | False | Calculate stress |
| `force_eval_method` | str | 'Quickstep' | Force evaluation method |
| `poisson_solver` | str | None | Poisson solver |
| `inp` | str | None | Custom CP2K input |
| `print_level` | str | 'MEDIUM' | Output verbosity |
| `debug` | bool | False | Debug mode |
| `auto_write` | bool | False | Auto-write mode |
| `nworkers` | int | 1 | Number of workers |

### Methods

#### `calculate(atoms=None, properties=['energy'], system_changes=...)`

Perform a calculation.

#### `get_potential_energy(atoms=None)`

Return the potential energy.

#### `get_forces(atoms=None)`

Return the atomic forces.

#### `get_stress(atoms=None)`

Return the stress tensor.

#### `get_charges(atoms=None)`

Return atomic charges.

#### `set(**kwargs)`

Set calculator parameters.

#### `reset()`

Reset the calculator state.

#### `read_results()`

Read results from output files.

#### `write_input(atoms)`

Write input files.

#### `close()`

Close the CP2K shell.

### Context Manager

```python
with CP2K() as calc:
    atoms.calc = calc
    energy = atoms.get_potential_energy()
```

## Plugin Registration

### `cp2k._ase_plugin`

Contains the ASE v4 plugin registration.

```python
from cp2k import _ase_plugin

print(_ase_plugin.__ase_plugins__)
```

### CalculatorPlugin Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Plugin name ('cp2k') |
| `long_name` | str | Full descriptive name |
| `citation` | str | Citation information |
| `implementation` | str | Implementation path |
| `configurable` | bool | Uses ase.config |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ASE_CP2K_COMMAND` | CP2K command |
| `CP2K_DATA_DIR` | CP2K data directory |
| `OMP_NUM_THREADS` | Number of OpenMP threads |
