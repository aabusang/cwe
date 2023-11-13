# Sheets Class Documentation

The `Sheets` class provides utility functions for generating CSV data based on various search parameters and for creating a ZIP archive of multiple CSV files.

## Methods

### generate_csv

#### Description:
Generates a CSV representation of the data based on the provided search criteria.

#### Parameters:
- `river_name`: Name of the river. Default is `None`.
- `tracer_type`: Type of the tracer. Default is `None`.
- `from_date`: Start date for the date range. Default is `None`.
- `to_date`: End date for the date range. Default is `None`.
- `flow_rate`: Flow rate or range of flow rates (e.g., "10-20"). Default is `None`.
- `channel_width`: Channel width or range of channel widths (e.g., "5-15"). Default is `None`.

#### Returns:
A string representation of the CSV data.

### get_timeseries_data

#### Description:
Fetches the `CONC_TIMESERIES` data based on the provided search criteria.

#### Parameters:
- `river_name`: Name of the river. Default is `None`.
- `tracer_type`: Type of the tracer. Default is `None`.
- `from_date`: Start date for the date range. Default is `None`.
- `to_date`: End date for the date range. Default is `None`.
- `flow_rate`: Flow rate or range of flow rates. Default is `None`.
- `channel_width`: Channel width or range of channel widths. Default is `None`.

#### Returns:
A list of `CONC_TIMESERIES` objects that match the search criteria.

### handle_range_filtering

#### Description:
Filters a queryset based on a field name and value. The value can be either a single number or a range.

#### Parameters:
- `queryset`: The initial queryset to be filtered.
- `field_name`: Name of the field to filter by.
- `value`: Value or range of values for filtering.

#### Returns:
A filtered queryset based on the given criteria.

### get_file_name

#### Description:
Generates a file name for the CSV based on the river name and date range.

#### Parameters:
- `river_name`: Name of the river.
- `from_date`: Start date for the date range.
- `to_date`: End date for the date range.

#### Returns:
A string representation of the file name.

### generate_zip

#### Description:
Creates a ZIP archive containing multiple CSV files.

#### Parameters:
- `river_names`: A list of river names.
- `from_date`: Start date for the date range.
- `to_date`: End date for the date range.

#### Returns:
The path to the generated ZIP file.

## Usage:

To generate a CSV for a specific river and date range:
```python
csv_data = Sheets.generate_csv(river_name="RiverName", from_date="2022-01-01", to_date="2022-01-31")
