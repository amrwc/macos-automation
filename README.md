# macOS Automation

Scripts and tools for interacting with macOS and various application via
command-line and/or Quick Actions.

For usage and setup instructions for each script, refer to its docblock near
the top.

## Setup

The scripts are usable either from the repository's directory, or via symlinks.
To create symlinks to all the scripts, run `setup.py`.

```console
./setup.py
```

## Testing

It's best to set up a virtual environment first

```console
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

### Unit tests

```console
pytest

# If you encounter errors, try the following:
python3 -m pytest

# Detailed output:
python3 -m pytest -vv

# Include stdout:
python3 -m pytest -vv -s
```

### Linting

```console
flake8
```
