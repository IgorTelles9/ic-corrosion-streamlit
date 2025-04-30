# Image Database Management System

A Streamlit application for managing image records in MongoDB.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Change the __init__ method in `models.py` file with your MongoDB connection details.

3. Run the application:
```bash
streamlit run app.py
```

## Features

- Form-based interface for adding image records
- Support for multiple image creation with the same characteristics
- Optional fields for resolution and degradation information
- Automatic path generation for multiple images

## Usage

1. Fill in the image path 
2. Select the object type and environment
3. Specify how many images you want to create
4. Fill in the optional fields 
5. Click Submit to insert the records

The application will automatically generate paths for multiple images by appending an index to the base path. 