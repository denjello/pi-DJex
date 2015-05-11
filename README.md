# pi-DJex

Python script for detecting the live audio input's RMS value and triggering a warning sequence through Raspberry PI GPIOs when crossing a configured threshold.

## Usage

```shell
# run the service
./pi-djex.py

# only update config without running service (if service is running in background)
./pi-djex.py --config --threshold=80

# get an overview of configuration options
./pi-djex.py --help
```

