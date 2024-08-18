# Main Experiment Control

This folder contains the necessary scripts and configurations for writing experiment sequences.

## Folder Structure

- **sequences/**
  - Contains scripts that define the execution sequence of experiments.
  - **device_testing/**
    - Scripts demonstrating individual functionality of different lab devices.

- **sequences_globals/**
  - Files containing global variables used across different sequences.

- **subsequences/**
  - **subsequences.py**: Contains utility functions for building up experiment sequences.

- **subsequences_globals/**
  - Global variables specific to subsequences.

- **connection_table.py**
  - Defines all hardware connections and configurations for the lab setup.

## Usage

1. Start by examining and potentially modifying the `connection_table.py` file to ensure it accurately represents your hardware setup.

2. Create new sequence scripts in the `sequences/` folder or modify existing ones to define your experiment procedures.

3. Use the `subsequences/subsequences.py` file to create reusable functions that can be incorporated into your main sequences.

4. Store any global variables needed for your sequences in the appropriate `*_globals/` folders.

5. When testing individual devices, create or use scripts in the `sequences/device_testing/` folder.

## Best Practices

- Always document your sequences and subsequences thoroughly.
- Use meaningful variable names and add comments to explain complex operations.
- When creating new global variables, consider their scope and place them in the appropriate `*_globals/` folder.
- Regularly backup your scripts and maintain version control.

For more detailed information on using this system, please refer to the full OneNote documentation `Labscript\Understanding the Labscript Environment\Organizing labscriptlib`.
