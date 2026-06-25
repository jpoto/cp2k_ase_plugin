# CP2K Plugin for ASE

A standalone CP2K calculator plugin for the Atomic Simulation Environment (ASE).

## Features

- Full CP2K calculator implementation compatible with ASE
- ASE v4 plugin system integration
- Support for ASE configuration system (`ase.config`)

## Installation

### From source

```bash
git clone https://github.com/cp2k/cp2k_ase_plugin.git
cd cp2k_plugin
pip install -e .
```

## Requirements

- ASE >= 3.23.0 (https://docs.ase-lib.org/install.html) 
- CP2K (https://github.com/cp2k/cp2k/blob/master/INSTALL.md)

## Usage

### Via plugin system

```python
from ase._4.plugins import plugins

CP2K = plugins.calculators['cp2k'].implementation()
calc = CP2K()
```

## CP2K Executable Configuration

The CP2K executable is launched via **CP2K-shell** (the interactive socket-mode
variant used for ASE communication). The plugin uses the following priority
order to locate the command:

### 1. Command parameter (highest priority)

```python
calc = CP2K(command="mpiexec -n 4 cp2k.psmp -s")
```

### 2. Class variable

```python
CP2K.command = "mpiexec -n 4 cp2k.psmp -s"
calc = CP2K()
```

### 3. ASE configuration file

Set in `~/.config/ase/config.ini`:

```ini
[cp2k]
cp2k_shell = mpirun -n 4 cp2k.psmp -s
```

### 4. Environment variable

```bash
export ASE_CP2K_COMMAND="mpiexec -n 4 cp2k.psmp -s"
```

### 5. Default (lowest priority)

If none of the above is set, the plugin defaults to:

```
cp2k.psmp -s
```

**Note**: The command must be resolvable via `$PATH` or given as an absolute path.
The plugin does not search for the executable automatically.

### shell mode

The default command `cp2k.psmp -s` launches CP2K-shell in shell mode.
For file-I/O mode (batch-style), you may want to use e.g.:

```bash
cp2k.psmp -i PREFIX.inp -o PREFIX.out
```

However, the CP2K calculator is designed around CP2K-shell and the
`-s` flag is required for full functionality.

## Citation

If you use this plugin in your research, please cite:

- M. Iannuzzi et al., “The CP2K Program Package Made Simple,” J. Phys. Chem. B, vol. 130, pp. 1237, 2026, (https://doi.org/10.1021/acs.jpcb.5c05851)
- CP2K developers (https://www.cp2k.org/)

## License

LGPL-2.1-or-later

## Documentation

See the [doc/](doc/) directory for detailed documentation.

## Testing

```bash
pytest cp2k/tests/
```

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
