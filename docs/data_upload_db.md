# Django Data Upload Script 

This script is designed to upload data from Excel sheets into a Django-based web application postgres database for the project.

## Overview

- The script reads data from an Excel file named `db.xlsm` inside data folder in project root.
- Each sheet in the Excel file represents a dataset that will be extracted
- The data from the sheets is structured and saved to the database using Django's ORM.

## Prerequisites

1. **Django Environment**: The script assumes that it's run within the context of a Django project. It requires `django.setup()` to be called after setting the correct Django settings module.
2. **Python Libraries**: The script utilizes the `pandas` library to read and manipulate Excel data. Ensure you have `pandas` installed in your environment.

## Usage

1. Ensure the script is in the `scripts` directory, which should be at the same level as `manage.py`.
2. Navigate to the directory containing `manage.py`.
3. Run the script using Python: `python scripts/script_name.py`.

## How It Works

1. The script first adjusts the Python path to include the top-level directory of the Django project.
2. The Django settings module (`tracer.settings.dev`) is specified, and the Django environment is set up.
3. Models from `datashow.models` are imported.
4. The `upload_data` function reads and processes each sheet in the Excel file, and the data is saved to the respective Django models.


## Key Considerations:

- **Settings**: The project uses a modular settings approach with `base.py`, `dev.py`, and `prod.py`. Ensure the correct settings file is used based on the environment.
  
- **Data**: The data to be uploaded resides in the `data/` directory. If the data source changes or if there are new files, ensure scripts and other components are updated accordingly.
  
- **Scripts**: All utility scripts, like the data upload script, reside in the `scripts/` directory. When running scripts, ensure the necessary environment variables and paths are set.
  
- **Dependencies**: Before deploying or running the project, ensure all dependencies listed in `requirements.txt` are installed.



## Potential Issues and other Considerations

1. **File Path**: The script expects the Excel file `db.xlsm` to be in the data directory at the project's root directory. Same level as manage.py, data, datashow, scripts. Ensure the file is present or adjust the file path accordingly.
2. **Data Structure**: The script assumes a specific structure in the Excel sheets. Changes in the Excel data structure might break the script.
3. **Missing Data**: Some data (e.g., latitude, longitude, duration) isn't available in the sheets and is set to `None`. Ensure this is the desired behavior or modify as needed.
4. **Django Model Changes**: If the Django models (`ST_HYDROLOGY`, `ST_CHARACTERISTICS`, etc.) undergo changes, the script might need adjustments to match the new model structures.
5. **Settings Module**: The `DJGANGO_SETTINGS_MODULE` in particular gave me lots of trouble recently, because the upload process and tightly integrate with the django models, we need it. You can either set it an environment variable just before running the script or add it to the script whit is what I did.
    The script uses the development settings module (`tracer.settings.dev`).   

    For production or other environments, adjust the settings module (`__init__.py` file in tracer/settins) accordingly.

## Future Improvements

1. **Error Handling**: Implement error handling for potential issues, such as missing Excel sheets or unexpected data formats.
2. **Logging**: Incorporate logging to capture detailed information about the upload process, which can be useful for debugging.
3. **Configuration**: Make aspects of the script (e.g., file path, settings module) configurable via command-line arguments or a configuration file.

