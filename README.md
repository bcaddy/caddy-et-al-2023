# Caddy et al. 2023

This is the repo for the 2023 MHD Code paper

## Dependencies

This are the versions that I ran everything with. It will likely work with other versions as well but I provide no guarantees.

- Python = 3.11.3
- matplotlib = 3.7.1
- numpy = 1.24.3
- h5py = 3.7.0

## Python Scripts

The python scripts are primarily for making plots, often including the tools to run Cholla to generate the data for
those plots. They are linked into the paper via a pickled dictionary and the `get_link.py` script. Shared functions are
in the `shared_tools.py` file.
