# Installation

## Requirements

- Python >= 3.10
- ASE >= 3.23.0
- CP2K (installed separately)

## Installing CP2K

Please follow the [CP2K installation instructions](https://github.com/cp2k/cp2k/blob/master/INSTALL.md) to install CP2K on your system.

## Installing cp2k-plugin

### From PyPI

```bash
pip install cp2k-plugin
```

### From source

```bash
git clone https://github.com/cp2k/cp2k_plugin.git
cd cp2k
pip install -e .
```

## Environment Setup

### Setting the CP2K command

You can configure the CP2K command in several ways:

1. **Environment variable:**
   ```bash
   export ASE_CP2K_COMMAND="mpirun -n 4 cp2k.psmp -s"
   ```

2. **ASE configuration file** (`~/.config/ase/config.ini`):
   ```ini
   [cp2k]
   command = mpirun -n 4 cp2k.psmp -s
   ```

3. **Python code:**
   ```python
   from cp2k import CP2K
   calc = CP2K(command="mpirun -n 4 cp2k.psmp -s")
   ```

### CP2K data directory

Set the `CP2K_DATA_DIR` environment variable to point to the directory containing CP2K basis sets and pseudopotentials:

```bash
export CP2K_DATA_DIR=/path/to/cp2k/data
```

## Verification

To verify the installation:

```python
from cp2k import CP2K
print(CP2K)
```
