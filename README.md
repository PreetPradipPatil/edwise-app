# 🎓 EdWise - Vendor Certification Platform

A comprehensive Streamlit application for validating vendor-submitted student, contact, and association data against Ed-Fi ODS (Operational Data Store) 2026 APIs.

**Live URL:** https://vendorcertification.streamlit.app/

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

EdWise is a vendor certification platform designed for Indiana DOE and other educational institutions using Ed-Fi ODS. It enables vendors to:

- **Validate** student, contact, and association records
- **Debug** API integration issues in real-time
- **Generate** comprehensive validation reports
- **Download** results in Excel format

The platform performs real-time field-level validation and descriptor API checking to ensure data quality before submission to production systems.

---

## ✨ Features

### Core Validation Features
- ✅ **Student Data Validation** - Comprehensive student record validation
- ✅ **Contact Data Validation** - Contact information verification
- ✅ **Association Validation** - Student-contact relationship validation
- ✅ **Field-Level Validation** - Column-by-column data quality checks
- ✅ **Descriptor Validation** - Real-time API descriptor verification

### API Management
- 🔧 **API Endpoint Manager** - Add, edit, and manage custom API endpoints
- 📊 **Fetch Individual Endpoints** - Debug specific API calls
- 🔍 **Real-Time Debugging** - Live API response inspection

### Reporting & Export
- 📥 **Excel Report Generation** - Download comprehensive validation results
- 📊 **Validation Summary** - Entity-level validation statistics
- 🔐 **Detailed Results** - Row-by-row validation details with reasons

### User Experience
- 🌓 **Dark/Light Theme Support** - Automatic OS theme detection
- 📱 **Responsive Design** - Works on all devices
- ⚡ **Real-time Updates** - Instant validation feedback

---

## 🔧 System Requirements

### Runtime
- **Python** 3.10+
- **Streamlit** 1.28.0+
- **Pandas** 2.2.0+

### Browser
- Chrome, Firefox, Safari, Edge (latest versions)
- JavaScript enabled
- Cookies enabled

### Internet
- Stable internet connection
- Access to Ed-Fi ODS API endpoints
- HTTPS enabled

---

## 📦 Installation

### Local Installation

#### 1. Clone Repository
```bash
git clone https://github.com/preetpradippatil/edwise-app.git
cd edwise-app
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Secrets (Local)
Create `.streamlit/secrets.toml`:
```toml
[ods_api]
token_url = "https://your-oauth-server.com/token"
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
```

#### 5. Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## ⚙️ Configuration

### Environment Variables

Create `.streamlit/secrets.toml` in your project root:

```toml
[ods_api]
token_url = "https://doe-edfiods-a-c-v2026-ca.grayisland-7cb4ec7b.eastus.azurecontainerapps.io/oauth/token"
api_key = "YOUR_API_KEY_HERE"
api_secret = "YOUR_API_SECRET_HERE"
```

### API Base URL

The application uses the following base API URL:
```
https://doe-edfiods-a-c-v2026-ca.grayisland-7cb4ec7b.eastus.azurecontainerapps.io/2026/data/v3/ed-fi
```

### Default API Endpoints

Three pre-configured endpoints are included:

| Endpoint | Purpose |
|----------|---------|
| `/students` | Student data validation |
| `/contacts` | Contact data validation |
| `/studentContactAssociations` | Student-contact relationships |

---

## 🚀 Usage

### Basic Workflow

#### 1. Enter Query Parameters
```
Student Unique ID: 127013241
Contact Unique ID: 10378101730000
```

#### 2. Configure Sample Data
- View/edit sample student, contact, and association records
- All editable via built-in data editor

#### 3. Manage API Endpoints
- Add custom endpoints as needed
- Edit existing endpoint URLs
- Fetch individual endpoint data for debugging

#### 4. Run Validation
```
Click: "🚀 Fetch Target & Run Validation"
```

#### 5. Review Results
- See field-level validation results
- Check descriptor validation status
- Review API debug outputs

#### 6. Download Report
```
Click: "📥 Download Full Validation Report"
Saves as: Excel file with:
  - Summary sheet
  - Student validation details
  - Contact validation details
  - Association validation details
```

---

## 📁 Project Structure

```
edwise-app/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration (optional)
│   └── secrets.toml         # API credentials (NOT in git)
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── LICENSE                  # License file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python package dependencies |
| `.streamlit/secrets.toml` | API credentials (LOCAL ONLY) |
| `.gitignore` | Ignore secrets and cache files |

---

## 🔗 API Endpoints

### Authentication

All API calls require OAuth 2.0 Bearer token authentication:

```bash
POST {token_url}
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
Basic Auth: {base64(api_key:api_secret)}
```

### Student Validation Endpoint

```
GET /students?offset=0&totalCount=true&studentUniqueId={id}
Authorization: Bearer {token}
```

**Response:**
```json
{
  "value": [
    {
      "studentUniqueId": "127013241",
      "firstName": "LILY",
      "middleName": "SOFVIA",
      "lastSurname": "ACRA",
      "birthSexDescriptor": "Female",
      "birthDate": "2008-03-24",
      "birthCountryDescriptor": "USA"
    }
  ]
}
```

### Contact Validation Endpoint

```
GET /contacts?offset=0&totalCount=true&contactUniqueId={id}
Authorization: Bearer {token}
```

### Association Validation Endpoint

```
GET /studentContactAssociations?offset=0&totalCount=true&studentUniqueId={id}&contactUniqueId={id}
Authorization: Bearer {token}
```

### Descriptor Validation Endpoints

```
GET /sexDescriptors?offset=0&totalCount=true&codeValue={value}
GET /countryDescriptors?offset=0&totalCount=true&codeValue={value}
GET /electronicMailTypeDescriptors?offset=0&totalCount=true&codeValue={value}
```

---

## 🌐 Deployment

### Deploy on Streamlit Community Cloud

#### 1. Create Streamlit Cloud Account
```
https://streamlit.io/cloud
Sign in with GitHub
```

#### 2. Deploy App
```
1. Click "Deploy an app"
2. Select repository: edwise-app
3. Branch: main
4. Main file: app.py
5. Click "Deploy"
```

#### 3. Configure Secrets
```
After deployment:
1. Click app settings (⋯)
2. Click "Secrets"
3. Paste:

[ods_api]
token_url = "YOUR_TOKEN_URL"
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

4. Save
```

#### 4. Access Live App
```
https://vendorcertification.streamlit.app/
```

### Updating Your App

After making code changes:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

Streamlit Cloud automatically redeploys within 2-3 minutes!

---

## 🆘 Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'openpyxl'"

**Solution:**
```bash
pip install openpyxl
```

Update `requirements.txt`:
```
openpyxl>=3.1.0
```

#### Issue: "KeyError: 'ods_api'"

**Solution (Local):**
Create `.streamlit/secrets.toml` with API credentials

**Solution (Streamlit Cloud):**
1. Go to app settings
2. Click "Secrets"
3. Add [ods_api] section with credentials

#### Issue: "Connection Error — cannot reach API"

**Check:**
- API URL is correct
- API server is running
- Network connection is stable
- API key/secret are valid

#### Issue: Theme shows incorrectly (light/dark)

**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Refresh page (Ctrl+R or Cmd+R)
- Check OS theme settings

#### Issue: API calls seem to be looping

**Check:**
- Network tab in DevTools
- Should see requests complete (not infinite)
- Timeouts prevent infinite retries

---

## 📊 Performance Tips

### For Better Performance

1. **Cache Results**
   - Results are cached for 5 minutes
   - Reduces unnecessary API calls

2. **Manage Endpoints**
   - Only keep endpoints you need
   - Remove unused custom endpoints

3. **Optimize Sample Data**
   - Keep sample data minimal
   - Large datasets slow validation

4. **Monitor Logs**
   - Check Streamlit Cloud logs regularly
   - Look for slow API responses

---

## 🔐 Security Best Practices

### Secrets Management

✅ **DO:**
- Store credentials in `.streamlit/secrets.toml` (local)
- Use Streamlit Cloud Secrets (production)
- Rotate API keys regularly
- Use environment variables for CI/CD

❌ **DON'T:**
- Commit `secrets.toml` to GitHub
- Hardcode credentials in code
- Share API keys via email/chat
- Store passwords in plaintext

### Code Security

✅ **Always:**
- Keep dependencies updated
- Use HTTPS for API calls
- Validate input data
- Handle errors gracefully

---

## 🔄 CI/CD Integration

### GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python -m py_compile app.py
```

---

## 📝 Contributing

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Commit** changes: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature/my-feature`
5. **Submit** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Test changes locally first
- Update documentation
- Keep commits atomic and descriptive

---

## 🐛 Bug Reports

Found a bug? Please report it!

**Create an Issue:**
1. Go to GitHub Issues
2. Click "New Issue"
3. Describe the bug in detail
4. Include steps to reproduce
5. Add screenshots if helpful

**Include:**
- App version
- Your Python version
- Browser and OS
- Error messages/logs

---

## 📚 Documentation

### Additional Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Ed-Fi ODS API Docs](https://edfi.atlassian.net/wiki/spaces/EdFiODS)
- [Python Documentation](https://docs.python.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💼 Support

### Get Help

**For Issues:**
- Check existing GitHub Issues
- Create a new Issue with details

**For Questions:**
- Check Documentation above
- Review Troubleshooting section
- Contact development team

**For Deployment Help:**
- Read Deployment section
- Check Streamlit Cloud docs
- Review configuration steps

---

## 🎉 Acknowledgments

- **Ed-Fi Alliance** - ODS specification and standards
- **Indiana DOE** - Project requirements and testing
- **Streamlit** - Application framework
- **Contributors** - Community improvements

---

## 📊 Version History

### Version 1.0.0 (Current)
- ✅ Student data validation
- ✅ Contact data validation
- ✅ Association validation
- ✅ API endpoint management
- ✅ Real-time debugging
- ✅ Excel report generation
- ✅ Dark/light theme support

### Planned Features
- 🔜 Batch validation import
- 🔜 User authentication
- 🔜 Validation history
- 🔜 Advanced filtering
- 🔜 Custom validation rules

---

## 📧 Contact

**Project Lead:** [Your Name]  
**Email:** [your.email@example.com]  
**GitHub:** [preetpradippatil](https://github.com/preetpradippatil)

---

## 🙏 Thank You!

Thank you for using EdWise! Your feedback helps us improve.

⭐ **Star this repository** if you found it helpful!

---

**Last Updated:** March 2026  
**Status:** ✅ Production Ready
