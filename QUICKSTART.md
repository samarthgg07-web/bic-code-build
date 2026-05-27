# Code, Bid & Build - Quick Start Guide

## ⚡ 5-Minute Setup

### For Windows Users

1. **Open Command Prompt** (Windows + R → type `cmd` → Enter)

2. **Navigate to project folder**
```bash
cd C:\Users\YourUsername\Desktop\Register
```

3. **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\activate
```

4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the Application**
```bash
python app.py
```

6. **Open in Browser**
   - Go to: `http://localhost:5000`
   - Enjoy! 🎉

---

### For macOS/Linux Users

1. **Open Terminal**

2. **Navigate to project folder**
```bash
cd ~/Desktop/Register
```

3. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the Application**
```bash
python app.py
```

6. **Open in Browser**
   - Go to: `http://localhost:5000`
   - Enjoy! 🎉

---

## 🔐 Admin Credentials

**Default Login (CHANGE BEFORE PRODUCTION)**
- Username: `admin`
- Password: `Admin@123`

To login:
1. Click "Admin Login" button (top-right)
2. Enter credentials
3. Click Login

---

## 📋 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `config.py` | Configuration settings |
| `database.db` | Data storage (auto-created) |
| `templates/` | HTML pages |
| `static/css/style.css` | Styling |
| `static/js/script.js` | JavaScript |

---

## 🎯 First Steps

### Step 1: Register a Team
1. Fill in all required fields
2. Click "Submit Registration"
3. See success message

### Step 2: Access Admin Dashboard
1. Click "Admin Login" (top-right)
2. Enter: admin / Admin@123
3. View all registered teams

### Step 3: Export to PDF
1. In admin dashboard, click "Download PDF"
2. PDF will download automatically

---

## ❓ Common Issues & Fixes

### Error: "No module named Flask"
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 already in use"
Edit the last line in `app.py`:
```python
# Change this line:
app.run(debug=True, host='0.0.0.0', port=5000)

# To this (for port 5001):
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then visit: `http://localhost:5001`

### Database Error
Delete `database.db` and restart the app - it will create a new one.

### Form won't submit
- Ensure all fields are filled (red * indicates required)
- Phone must be 10 digits
- USN format: ABC21DE001

---

## 🔄 Deactivating Virtual Environment

When you're done:

**Windows:**
```bash
deactivate
```

**macOS/Linux:**
```bash
deactivate
```

---

## 📞 Need Help?

1. **Check README.md** for detailed documentation
2. **Review app.py** comments for code explanation
3. **Look at templates** for UI/UX structure

---

## 🚀 Next: Production Deployment

When ready for production:

1. Change admin password in `config.py`
2. Generate new SECRET_KEY
3. Set up HTTPS
4. Use production server (Gunicorn)
5. See README.md for details

---

**Happy Coding! 🎉**
