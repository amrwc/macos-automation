# macOS Automation

Scripts and tools for interacting with macOS and various application via
command-line and/or Quick Actions.

## Wi-Fi

A utility to turn Wi-Fi on or off.

### Setup

Create a symlink.

```console
ln -s "$(pwd)/wifi.py" /usr/local/bin/wifi
```

### Usage

```console
./wifi.py <on/off>
wifi <on/off>
```

## Bluetooth

A utility to turn Bluetooth on or off.

### Setup

1. Install `blueutil`.

   ```console
   brew install blueutil
   ```

1. Create a symlink. Remember that there's a built-in `sleep` utility in the
   system that takes precedence. That's why it's necessary to choose a
   different name.

   ```console
   ln -s "$(pwd)/bluetooth.py" /usr/local/bin/bluetooth
   ```

### Usage

```console
./bluetooth.py <on/off>
bluetooth <on/off>
```

## Sleep

A utility for putting the machine to sleep from command-line.

### Setup

Create a symlink.

```console
ln -s "$(pwd)/sleep.py" /usr/local/bin/night
```

### Usage

```console
./sleep.py
night
```

## Good Night

A utility for performing some of the common shutting down operations from
command-line in combination.

### Setup

Create a symlink to the script.

```console
ln -s "$(pwd)/goodnight.py" /usr/local/bin/goodnight
```

### Usage

```console
./goodnight.py
goodnight
```

## Tunnelblick

A utility for sending simple instructions to Tunnelblick from command line.

Supported commands:

- connect -- opens Tunnelblick if it was closed and establishes a connection
  using the configuration specified in the config file.
- quit -- quits Tunnelblick.

### Setup

1. Rename `tunnelblick.config.example.json` to `tunnelblick.config.json`.
1. Set `configuration-name` field to the VPN configuration name already
   imported to Tunnelblick.
1. Create a symlink.

   ```console
   ln -s "$(pwd)/tunnelblick.py" /usr/local/bin/tunnelblick
   ```

### Usage

```console
./tunnelblick.py <connect/quit>
tunnelblick <connect/quit>
```
