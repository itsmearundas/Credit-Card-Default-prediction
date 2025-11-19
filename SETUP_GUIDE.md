# Complete Setup Guide - CreditRisk AI Platform

## 📋 Table of Contents
1. [Folder Structure](#folder-structure)
2. [File Placement](#file-placement)
3. [Quick Setup](#quick-setup)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)

## 📁 Folder Structure

Create the following folder structure:

```
credit-risk-ai/
│
├── app.py                                    # Main Flask application
├── requirements.txt                          # Python dependencies
├── README.md                                 # Project documentation
├── random_forest_credit_default_model.joblib # Your trained ML model
│
└── templates/                                # HTML templates folder
    ├── home.html                             # Landing page
    ├── input.html                            # Assessment form
    ├── result.html                           # Results page
    ├── about.html                            # About page
    ├── 404.html                              # 404 error page
    └── 500.html                              # 500 error page
```

## 📝 File Placement Guide

### Step 1: Create Project Directory

```bash
# Create main project folder
mkdir credit-risk-ai
cd credit-risk-ai

# Create templates folder
mkdir templates
```

### Step 2: Place Files in Correct Locations

#### Root Directory Files:
- `app.py` → Place in `credit-risk-ai/`
- `requirements.txt` → Place in `credit-risk-ai/`
- `README.md` → Place in `credit-risk-ai/`
- `random_forest_credit_default_model.joblib` → Place in `credit-risk-ai/`

#### Templates Directory Files:
- `home.html` → Place in `credit-risk-ai/templates/`
- `input.html` → Place in `credit-risk-ai/templates/`
- `result.html` → Place in `credit-risk-ai/templates/`
- `about.html` → Place in `credit-risk-ai/templates/`
- `404.html` → Place in `credit-risk-ai/templates/`
- `500.html` → Place in `credit-risk-ai/templates/`

## 🚀 Quick Setup

### Option 1: Using Command Line (Windows)

```bash
# Navigate to project directory
cd credit-risk-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 2: Using Command Line (macOS/Linux)

```bash
# Navigate to project directory
cd credit-risk-ai

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 3: Manual Installation

```bash
# Install each package individually
pip install Flask==3.0.0
pip install pandas==2.1.3
pip install numpy==1.26.2
pip install scikit-learn==1.3.2
pip install joblib==1.3.2

# Run the application
python app.py
```

## 🧪 Testing

### 1. Verify Installation

After running `python app.py`, you should see:

```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 2. Test Each Page

Open your browser and test these URLs:

| Page | URL | Expected Result |
|------|-----|----------------|
| Home | `http://localhost:5000/` | Landing page loads |
| Assessment | `http://localhost:5000/assess` | Form page loads |
| About | `http://localhost:5000/about` | About page loads |
| 404 Error | `http://localhost:5000/test` | 404 page displays |

### 3. Test Prediction Flow

1. Go to `http://localhost:5000/`
2. Click "Start Assessment"
3. Fill in the form with sample data:
   - Credit Limit: 50000
   - Age: 35
   - Gender: 1
   - Education: 2
   - Marriage: 1
   - Fill remaining fields with sample values
4. Click "Analyze Default Risk"
5. Verify results page displays

## 🔧 Troubleshooting

### Issue 1: "Module not found" Error

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Issue 2: "Template not found" Error

**Problem**: `jinja2.exceptions.TemplateNotFound: home.html`

**Solution**:
- Verify `templates/` folder exists in project root
- Check that all HTML files are in `templates/` folder
- Ensure file names match exactly (case-sensitive)

### Issue 3: Model File Not Found

**Problem**: `FileNotFoundError: random_forest_credit_default_model.joblib`

**Solution**:
- Ensure model file is in project root directory
- Check file name spelling matches exactly
- Verify file is not corrupted

### Issue 4: Port Already in Use

**Problem**: `OSError: [Errno 98] Address already in use`

**Solution**:
```bash
# Change port in app.py (last line):
app.run(host='0.0.0.0', port=5001, debug=True)

# Or kill process using port 5000:
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue 5: Form Submission Not Working

**Problem**: Form doesn't submit or shows error

**Solution**:
- Check browser console for JavaScript errors (F12)
- Verify all required fields are filled
- Ensure numeric fields contain valid numbers
- Check Flask terminal for error messages

## 📊 Sample Test Data

Use this data to test the application:

### Low Risk Profile:
```
Credit Limit: 100000
Age: 35
Gender: 1
Education: 2
Marriage: 1

Payment Status (all months): -1
Bill Amounts (all months): 20000
Payment Amounts (all months): 20000
```

### High Risk Profile:
```
Credit Limit: 50000
Age: 28
Gender: 0
Education: 3
Marriage: 2

Payment Status (all months): 2
Bill Amounts (all months): 45000
Payment Amounts (all months): 1000
```

## 🌐 Production Deployment Checklist

Before deploying to production:

- [ ] Set `debug=False` in `app.py`
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure proper WSGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Add backup for model file
- [ ] Test all routes thoroughly

## 📞 Getting Help

If you encounter issues not covered here:

1. Check Flask documentation: https://flask.palletsprojects.com/
2. Check scikit-learn docs: https://scikit-learn.org/
3. Review error messages in terminal
4. Check browser console (F12) for frontend errors
5. Create an issue in the project repository

## ✅ Success Checklist

Your setup is complete when:

- [ ] All dependencies installed without errors
- [ ] Flask server starts successfully
- [ ] Home page loads at `http://localhost:5000/`
- [ ] Navigation between pages works
- [ ] Assessment form accepts input
- [ ] Prediction results display correctly
- [ ] About page displays information
- [ ] Error pages work (test 404 by visiting invalid URL)

---

**Need Help?** Review the README.md for additional information or create an issue in the repository.