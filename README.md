# Excel TSS Converter Web App

A Streamlit web application for converting Excel files to TSS template format (Step 1 Processing).

## Features

- Upload Excel files (.xlsx, .xls) up to 200MB
- Automatic detection of non-empty sheets
- Template creation for each non-empty sheet
- Individual file downloads and bulk ZIP download
- Clean, modern UI following Ngoc Son TSS Converter App design
- Real-time processing progress indicators
- Comprehensive error handling and validation

## How It Works

1. **Upload**: Select your Excel file using the drag-and-drop interface
2. **Analysis**: The app analyzes the file and identifies non-empty sheets
3. **Processing**: Creates a Step 1 template for each non-empty sheet
4. **Download**: Download individual files or all files as a ZIP

### Output Files

For each non-empty sheet, the app creates a template file named:
```
[SheetName] - Step1.xlsx
```

Each template contains:
- Row 1: "Article name" (with green background)
- Row 2: "Article number" (with green background) 
- Row 3: 17 column headers (A-Q) with yellow background
- Proper formatting and column widths

## Installation & Setup

### Local Development

1. **Clone/Download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```
4. **Open your browser** to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Push code** to a GitHub repository
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub** account
4. **Select your repository** and branch
5. **Set main file path** to `app.py`
6. **Deploy** - the app will be available at your custom URL

## Project Structure

```
excel-converter/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── modules/
│   ├── __init__.py
│   ├── file_handler.py        # Excel file reading and processing
│   ├── converter.py           # Template creation logic
│   └── exporter.py            # File export and download handling
├── utils/
│   ├── __init__.py
│   └── validators.py          # File validation functions
├── output/                    # Generated template files (auto-created)
├── input/                     # Sample input files
└── README.md                  # This file
```

## Technical Details

### Dependencies

- **Streamlit** (>=1.28.0) - Web application framework
- **Pandas** (>=2.0.0) - Excel file reading and data processing
- **OpenPyXL** (>=3.1.0) - Excel file writing and formatting
- **xlrd** (>=2.0.0) - Legacy Excel file support
- **Pillow** (>=10.0.0) - Image handling (optional)

### File Processing Logic

The application follows this workflow:

1. **Upload Validation**: Checks file size, format, and content
2. **Sheet Analysis**: Identifies all sheets and filters non-empty ones
3. **Template Generation**: Creates formatted Excel templates using OpenPyXL
4. **File Export**: Packages files for download (individual + ZIP)

### Error Handling

- File size validation (200MB limit)
- Format validation (Excel files only)
- Content validation (readable Excel structure)
- Processing error recovery
- User-friendly error messages

## Configuration

### Streamlit Settings (.streamlit/config.toml)

```toml
[theme]
primaryColor="#000000"
backgroundColor="#FFFFFF" 
secondaryBackgroundColor="#F7F9FB"
textColor="#333333"
font="sans serif"

[server]
maxUploadSize=200
enableXsrfProtection=true
```

### Template Structure

The generated templates follow this format:
- **Row 1**: Article name (bold, green background)
- **Row 2**: Article number (bold, green background)
- **Row 3**: 17 headers (A-Q columns, yellow background)
- **Column widths**: 15 units each
- **Fonts**: Bold for headers, regular for content

## Usage Examples

### Basic Usage

1. Open the web app
2. Drag and drop your Excel file
3. Review the file information and non-empty sheets
4. Click "Process File"
5. Download individual files or the complete ZIP

### Sample Input

The app works with any Excel file containing data. For each sheet with content:

**Input**: `Sample File.xlsx` with sheets "44x53" and "65x43"

**Output**: 
- `44x53 - Step1.xlsx`
- `65x43 - Step1.xlsx`
- `Sample File_Step1_Templates.zip` (containing both files)

## Deployment Notes

### Streamlit Cloud Deployment

- **Memory**: 1GB RAM available
- **File Upload**: 200MB maximum
- **Processing**: Handles multiple sheets efficiently
- **Storage**: Temporary file storage only
- **Security**: No data persistence, files cleaned up automatically

### Keep-Alive System

The repository includes a GitHub Actions workflow that prevents the Streamlit app from sleeping:

- **Schedule**: Automatically pings the app every 4 hours
- **Compliance**: Follows Streamlit's terms of service with conservative timing
- **Monitoring**: Includes error handling and detailed logging
- **Manual Control**: Can be triggered manually or disabled when needed

#### Setup Keep-Alive

1. **Deploy to Streamlit Cloud** first to get your app URL
2. **Configure App URL** (optional):
   - Go to repository Settings → Secrets and variables → Actions
   - Add secret `STREAMLIT_APP_URL` with your app URL
   - If not configured, defaults to `https://cpc-tss-converter.streamlit.app`
3. **Monitor**: Check the "Actions" tab for workflow status

For detailed instructions, see [`.github/KEEP_ALIVE.md`](.github/KEEP_ALIVE.md)

### Environment Variables

No environment variables required for basic functionality.

## Troubleshooting

### Common Issues

1. **"File too large"**: Reduce file size or split into smaller files
2. **"Cannot read Excel file"**: Ensure file is a valid Excel format
3. **"No non-empty sheets"**: Check that your Excel file contains data
4. **"Processing failed"**: Check file structure and try again

### Debug Mode

To enable detailed logging, modify `app.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Support

For issues or questions:
1. Check this README for common solutions
2. Ensure your Excel file meets the requirements
3. Try with a simpler test file first

## License

This project is created for internal TSS conversion processes.

## Changelog

### Version 1.0 (Initial Release)
- Excel file upload and validation
- Template creation for non-empty sheets
- Download functionality (individual + ZIP)
- Custom UI styling matching reference design
- Comprehensive error handling