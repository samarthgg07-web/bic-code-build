# Code, Bid & Build - Event Registration Web Application

A complete, responsive web application for managing team registrations for the "Code, Bid & Build" competitive event. Built with Python Flask backend, SQLite database, and Bootstrap frontend.

## 📋 Features

### Participant Features
- **Team Registration Form** - Easy-to-use registration interface
- **Form Validation** - Real-time validation for phone numbers and USNs
- **Success Notifications** - Confirmation messages after registration
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Admin Login Access** - Secure link to admin panel

### Admin Features
- **Secure Admin Login** - Session-based authentication
- **Dashboard Overview** - Total teams and participants statistics
- **Team Management** - View all registered teams in a table
- **Search Functionality** - Search by team name, leader name, USN, or phone
- **Pagination** - Browse registrations with 10 teams per page
- **PDF Export** - Download all registrations as a formatted PDF report
- **Logout** - Secure session logout

### Technical Features
- **SQLite Database** - Local persistent storage
- **Session-Based Authentication** - Secure admin login
- **Input Validation** - Backend and frontend validation
- **Error Handling** - Custom error pages (404, 500)
- **Responsive Bootstrap UI** - Modern design with Animate.css
- **Flash Messages** - User-friendly notification system

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.0
- **Database**: SQLite3 (Python built-in)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **PDF Generation**: ReportLab
- **Authentication**: Flask Sessions
- **Templating**: Jinja2

## 📁 Project Structure

```
Register/
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Team registration page
│   ├── admin_login.html       # Admin login page
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
└── static/
    ├── css/
    │   └── style.css          # Custom CSS styling
    └── js/
        └── script.js          # JavaScript utilities
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd Register

# Or simply download and extract the zip file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌐 Usage Guide

### For Participants

1. **Open the Website**
   - Navigate to `http://localhost:5000`
   - You'll see the Team Registration page

2. **Fill Registration Form**
   - Enter Team Name
   - Fill Team Leader details (Name, USN, College, Phone)
   - Add three team member details
   - All fields are required

3. **Form Validation**
   - Phone number: 10 digits starting with 6-9
   - USN Format: ABC21DE001 (3 letters, 2 digits, 2 letters, 3 digits)
   - All fields must be filled

4. **Submit**
   - Click "Submit Registration"
   - Success message will appear if registration is complete

### For Admins

1. **Admin Login**
   - Click "Admin Login" button in top-right corner
   - **Default Credentials:**
     - Username: `admin`
     - Password: `Admin@123`
   - ⚠️ Change these credentials in production!

2. **View Dashboard**
   - See total teams and participants statistics
   - Browse all registrations in a table
   - Each row shows team and member details

3. **Search Registrations**
   - Use the search box to find teams by:
     - Team name
     - Leader name
     - USN
     - Phone number

4. **Pagination**
   - Navigate through pages (10 teams per page)
   - Use "First", "Previous", "Next", "Last" buttons

5. **Export to PDF**
   - Click "Download PDF" button
   - A formatted PDF with all registrations will download
   - PDF includes team names, leader details, teammates, and registration time

6. **Logout**
   - Click "Logout" button
   - You'll be redirected to the home page

## 🔐 Security Notes

### Important: Change Default Credentials

Before deploying to production:

1. Open `app.py`
2. Find the Admin Credentials section (around line 55)
3. Change `ADMIN_PASSWORD` to a strong password
4. Change `SECRET_KEY` to a random value

```python
# app.py (lines 55-57)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Admin@123'  # ⚠️ Change this!
```

Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

## 📊 Database Schema

### TeamRegistration Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| team_name | String(100) | Unique team name |
| leader_name | String(100) | Team leader full name |
| leader_usn | String(20) | Team leader USN (unique) |
| leader_college | String(150) | College name |
| leader_phone | String(15) | Contact phone |
| teammate1_name | String(100) | First teammate name |
| teammate1_usn | String(20) | First teammate USN (unique) |
| teammate2_name | String(100) | Second teammate name |
| teammate2_usn | String(20) | Second teammate USN (unique) |
| teammate3_name | String(100) | Third teammate name |
| teammate3_usn | String(20) | Third teammate USN (unique) |
| registration_time | DateTime | Auto-generated timestamp |

## 🎨 Customization

### Change Event Name
Edit template files:
- `templates/base.html` - Change "Code, Bid & Build" in navigation
- `templates/index.html` - Change in hero section and forms

### Change Colors
Edit `static/css/style.css`:
- Primary color: `--primary-color: #1f4788`
- Secondary color: `--secondary-color: #ff6b35`
- Success color: `--success-color: #00d4aa`

### Change Admin Credentials
Edit `app.py` lines 55-57:
```python
ADMIN_USERNAME = 'your-username'
ADMIN_PASSWORD = 'your-strong-password'
```

### Add More Form Fields
1. Add column to `TeamRegistration` model in `app.py`
2. Add form input in `templates/index.html`
3. Add validation in `validate_team_registration()` function
4. Update PDF export function if needed

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py --port 5001
```

### Database Issues
If you get database errors:
```bash
# Delete the old database
rm database.db

# The app will create a new one automatically
python app.py
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Form Not Submitting
1. Check browser console for errors (F12)
2. Ensure all required fields are filled
3. Check phone number is 10 digits
4. Check USN format matches: ABC21DE001

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: Below 768px

## 🚀 Deployment Guide

### For Development
Current setup is perfect for local development and testing.

### For Production (Linux Server)

1. **Install Python and dependencies**
```bash
sudo apt-get update
sudo apt-get install python3.9 python3-pip
```

2. **Set up Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Use Nginx as reverse proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

4. **Run with Supervisor for auto-restart**
```bash
pip install supervisor
```

Create `/etc/supervisor/conf.d/app.conf`:
```ini
[program:codebiduild]
directory=/path/to/Register
command=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
autostart=true
autorestart=true
```

5. **Enable HTTPS with Let's Encrypt**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📝 License

This project is created for educational purposes. Feel free to modify and use it for your events.

## 👥 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check application logs

## 📞 Contact

For event-specific questions, contact the event organizers.

---

**Built with ❤️ for Code, Bid & Build Event**

Version: 1.0.0
Last Updated: 2024
