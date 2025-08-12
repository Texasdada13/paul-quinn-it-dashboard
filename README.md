# Paul Quinn College IT Analytics Suite

A comprehensive IT spend management and project tracking dashboard built with Streamlit.

## Features

- **Multi-Persona Views**: Tailored dashboards for CFO, CIO, CTO, and Project Managers
- **Budget Analysis**: Track IT spending across categories with variance analysis
- **Project Management**: Monitor active projects, timelines, and resource allocation
- **Vendor Management**: Analyze vendor spend and optimize contracts
- **Security Monitoring**: Track security metrics and vulnerabilities
- **Benchmarking**: Compare performance against peer institutions

## Deployment to Streamlit Cloud

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at share.streamlit.io)

### Step-by-Step Deployment

1. **Prepare Your GitHub Repository**
   - Create a new repository or use an existing one
   - Upload these files to your repository:
     - `app.py` (the main application file)
     - `requirements.txt` (dependencies)
     - `README.md` (this file)

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account if not already connected
   - Select your repository
   - Select branch (usually `main` or `master`)
   - Set **Main file path** to `app.py`
   - Click "Deploy"

3. **Wait for Deployment**
   - Streamlit will build and deploy your app
   - This usually takes 2-5 minutes
   - You'll get a URL like `https://your-app-name.streamlit.app`

### Troubleshooting Common Issues

1. **Module Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check that package versions are compatible

2. **File Not Found Errors**
   - Make sure all file paths are relative
   - Don't reference local files that aren't in the repository

3. **Memory Issues**
   - Streamlit Cloud has resource limits
   - Optimize data loading and caching if needed

## Local Development

To run locally:

```bash
# Clone the repository
git clone [your-repo-url]

# Navigate to the directory
cd [your-repo-name]

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

### Adding New Features
1. Modify `app.py` to add new visualizations or data sources
2. Update `requirements.txt` if adding new dependencies
3. Push changes to GitHub - Streamlit will auto-redeploy

### Connecting to Real Data
Replace the `generate_sample_data()` function with connections to your actual data sources:
- Database connections
- API integrations
- CSV/Excel file uploads

## Support

For issues with:
- **Streamlit Cloud**: Check [Streamlit documentation](https://docs.streamlit.io)
- **Application bugs**: Create an issue in the GitHub repository

## License

This project is provided as-is for Paul Quinn College's use.
