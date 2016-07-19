# Seismology Workflow

This workflow performs seismogram deconvolutions to estimate earthquake source time functions (STFs) for the 2013 Craig, Alaska Earthquake. Signals in the subdirectory `input/EGF` are deconvolved from the corresponding signals in the subdirectory `input/MShock`.

<img src="docs/images/seismology-workflow.png?raw=true" width="600">

### Description

__`sG1IterDecon`__: receives a pair of signals, one from `input/EGF` and another from `input/MShock`, and computes seismogram deconvolutions to estimate earthquake source time functions (STFs). The output file is in the SAC (Seismic Analysis Code) format.

__`siftSTFByMisfit`__: receives all STFs generated from the `sG1IterDecon` jobs and sifts the data by misfit. Only the good fits are kept and compressed into a single `.tar.gz` file.

## Generating the Workflow
The `generate_dax.sh` script creates a Pegasus DAX workflow using the signals found in the subdirectories `input/EGF` and `input/MShock`.
The number of `sG1IterDecon` jobs will depend on the number of EGF signals and their corresponding signals in MShock. The command should be executed as follows:

```
./generate_dax.sh seismology.dax
```
This command will generate a `seismology.dax` file, which is the Pegasus workflow containing all jobs (with their corresponding executables) and their dependencies (data dependency in this case).

## Running the Seismology Workflow
To run the workflow, execute the following command:
```
./plan_dax.sh seismology.dax
```
Once the workflow execution is completed, the compressed output file with the good fits, will be available in `output/good-fit.tar.gz`.

