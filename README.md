# Solute Tracer Data Explorer

This Django project is designed to visualize solute tracer data, offering a comprehensive web interface for users to explore, visualize, and download time-series data related to river databases.

## Features

### Explore Data
Users can filter and visualize data based on specific criteria such as:
- River names
- Tracer types
- Stream order
- Channel width
- Date range
- Geographic features
- Flow rate

### Download Data
Allows users, especially those logged in, to download selected datasets.

### Additional Pages
- **About**: Provides information about the project.
- **Login**: Allows users to log in and access more features, such as downloading specific datasets.
- **Upload (Coming Soon)**: Users will be able to upload datasets. An AI-powered file detection feature will detect the type of data, the rows, and columns, and seamlessly upload them to the database.

### Map Selection (Coming Soon)
In the explore page, users will soon be able to select a part of a map, and the data from the selected geo-location will be displayed. Users can also use dropdown menus to specify the type of data they wish to view.

## Installation & Setup

1. **Clone the Repository**:
   \```
   git clone https://github.com/aabusang/cwe
   ```

2. **Set Up Virtual Environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```
   python manage.py runserver
   ```

## Database & External Integration

- **Local Database**: We have all the data from the sheet uploaded into a relational database locally, on hydroshare. Will be accessible from them site also with
  
- **HydroShare Integration**: The project's database is also hosted on HydroShare, and there are plans to allow users to query it directly from HydroShare very soon.

## User Roles

- **Guests**: Can browse the site and view visualizations.
- **Logged-In Users**: Can visualize or select specific data and have the ability to download it.

## Future Improvements

- **AI-Powered File Detection**: In the upload page, there is currently a traditional selection of features, and a file and upload. But an upcoming AI feature will detect the type of data being uploaded, identify the rows and columns, and streamline the data upload process.
  
- **Geo-Location Data Visualization**: Users will be able to select specific parts of a map in the explore page, and the data from that geo-location will be displayed below.

## Contributing

Your contributions are always welcome! Please read the contributing guidelines (to be created) before submitting any pull requests.
