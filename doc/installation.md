# Installation

## Requirements

- Python >= 3.10
- ASE >= 3.23.0
- CP2K (installed separately)

## Installing CP2K

Please follow the [CP2K installation instructions](https://github.com/cp2k/cp2k/blob/master/INSTALL.md) to install CP2K on your system.

## Installing cp2k-plugin

### From source

```bash
git clone https://github.com/cp2k/cp2k_ase_plugin.git
cd cp2k_plugin
pip install -e .
```

## Environment Setup

### Setting the CP2K command

You can configure the CP2K command in several ways:

1. **Environment variable:**
   ```bash
   export ASE_CP2K_COMMAND="env OMP_NUM_THREADS=1 mpirun -n 4 cp2k.psmp -s"
   ```

2. **ASE configuration file** (`~/.config/ase/config.ini`):
   ```ini
   [cp2k]
   cp2k_shell = env OMP_NUM_THREADS=1 mpirun -n 4 cp2k.psmp -s
   cp2k_main = env OMP_NUM_THREADS=1 mpirun -n 4 cp2k.psmp
   ```

3. **Python code:**
   ```python
   from cp2k_plugin import CP2K
   calc = CP2K(command="env OMP_NUM_THREADS=1 mpirun -n 4 cp2k.psmp -s")
   ```

**Note**: Any number of MPI processes should work, but large numbers can slow down the tests. Use `OMP_NUM_THREADS=1` to avoid thread exhaustion.

## Working Directory

**Important**: Always specify a working directory via `directory=...` to keep output files.
If `directory=None` (the default), a temporary directory is created and auto-cleaned on `close()`.

```python
from cp2k_plugin import CP2K

calc = CP2K(directory="/path/to/output")
```

To use a temporary directory (files are deleted when the calculator is closed):

```python
from cp2k_plugin import CP2K
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    calc = CP2K(directory=tmpdir)
    # ... use calculator ...
# Files in tmpdir are cleaned up here
```

### CP2K data directory

Set the `CP2K_DATA_DIR` environment variable to point to the directory containing CP2K basis sets and pseudopotentials:

```bash
export CP2K_DATA_DIR=/path/to/cp2k/data
```

## Verification

To verify the installation:

```python
from cp2k_plugin import CP2K
print(CP2K)
```
