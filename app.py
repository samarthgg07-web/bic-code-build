from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from datetime import datetime
from functools import wraps
import os
import io
import sqlite3
import re
import types
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

# ===========================
# Flask Application Setup
# ===========================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Path for local SQLite database
DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Make Python builtins available in Jinja templates
app.jinja_env.globals['enumerate'] = enumerate

# ===========================
# Admin Credentials (Secure Config)
# ===========================
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Admin@123'  # Change this in production

# ===========================
# SQLite helpers
# ===========================

def get_db_connection():
    """Return a sqlite3 connection with row factory"""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create database and table if they do not exist. Migrate if necessary to allow optional teammates."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Check if table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team_registration'")
    exists = cur.fetchone()
    if not exists:
        # Create table with teammate2 and teammate3 nullable (optional)
        cur.execute(
            '''
            CREATE TABLE team_registration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL UNIQUE,
                leader_name TEXT NOT NULL,
                leader_usn TEXT NOT NULL UNIQUE,
                leader_college TEXT NOT NULL,
                leader_phone TEXT NOT NULL,
                teammate1_name TEXT NOT NULL,
                teammate1_usn TEXT NOT NULL UNIQUE,
                teammate2_name TEXT,
                teammate2_usn TEXT UNIQUE,
                teammate3_name TEXT,
                teammate3_usn TEXT UNIQUE,
                registration_time TEXT NOT NULL
            )
            '''
        )
        conn.commit()
    else:
        # Table exists - ensure optional columns allow NULL. If current schema has NOT NULL set for optional columns, recreate table.
        cur.execute("PRAGMA table_info(team_registration)")
        cols = cur.fetchall()
        col_info = {c['name']: c for c in cols}
        need_migration = False
        # If teammate2_usn or teammate3_usn exist and are NOT NULL, migrate
        for opt_col in ('teammate2_usn', 'teammate3_usn'):
            info = col_info.get(opt_col)
            if info and info['notnull'] == 1:
                need_migration = True
        if need_migration:
            # Create new table
            cur.execute(
                '''
                CREATE TABLE team_registration_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_name TEXT NOT NULL UNIQUE,
                    leader_name TEXT NOT NULL,
                    leader_usn TEXT NOT NULL UNIQUE,
                    leader_college TEXT NOT NULL,
                    leader_phone TEXT NOT NULL,
                    teammate1_name TEXT NOT NULL,
                    teammate1_usn TEXT NOT NULL UNIQUE,
                    teammate2_name TEXT,
                    teammate2_usn TEXT UNIQUE,
                    teammate3_name TEXT,
                    teammate3_usn TEXT UNIQUE,
                    registration_time TEXT NOT NULL
                )
                '''
            )
            # Copy data, converting empty strings to NULL for optional columns
            cur.execute(
                '''
                INSERT INTO team_registration_new (id, team_name, leader_name, leader_usn, leader_college, leader_phone,
                    teammate1_name, teammate1_usn, teammate2_name, teammate2_usn, teammate3_name, teammate3_usn, registration_time)
                SELECT id, team_name, leader_name, leader_usn, leader_college, leader_phone,
                    teammate1_name, teammate1_usn,
                    NULLIF(teammate2_name, ''), NULLIF(teammate2_usn, ''),
                    NULLIF(teammate3_name, ''), NULLIF(teammate3_usn, ''), registration_time
                FROM team_registration;
                '''
            )
            cur.execute('DROP TABLE team_registration')
            cur.execute('ALTER TABLE team_registration_new RENAME TO team_registration')
            conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# ===========================
# Authentication Decorator
# ===========================
def login_required(f):
    """Decorator to protect routes that require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ===========================
# Validation Functions
# ===========================

def validate_phone_number(phone):
    """Validate phone number (10 digits for Indian numbers)"""
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None


def validate_usn(usn):
    """(Deprecated) USN format validation removed to allow flexible USN values"""
    # Allow any non-empty alphanumeric string (no strict format enforced)
    return bool(usn and usn.strip())


def validate_team_registration(data):
    """Validate all team registration fields"""
    errors = []
    
    # Required fields: team_name, leader fields, teammate1 fields, phone
    required_fields = [
        'team_name', 'leader_name', 'leader_usn', 'leader_college', 'leader_phone',
        'teammate1_name', 'teammate1_usn'
    ]
    
    for field in required_fields:
        if not data.get(field, '').strip():
            errors.append(f'{field.replace("_", " ").title()} is required.')
    
    # Validate phone number
    if data.get('leader_phone') and not validate_phone_number(data.get('leader_phone')):
        errors.append('Invalid phone number. Please enter a valid 10-digit number.')
    
    return errors

# ===========================
# Routes - Public (Participant)
# ===========================
@app.route('/')
def index():
    """Home page with team registration form"""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_team():
    """Handle team registration using sqlite3"""
    try:
        data = request.form.to_dict()
        errors = validate_team_registration(data)
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('index'))
        
        # Normalize input
        team_name = data['team_name'].strip()
        leader_name = data['leader_name'].strip()
        leader_usn = data['leader_usn'].strip()
        leader_college = data['leader_college'].strip()
        leader_phone = data['leader_phone'].strip()
        teammate1_name = data['teammate1_name'].strip()
        teammate1_usn = data['teammate1_usn'].strip()
        # Optional teammate2
        teammate2_name = data.get('teammate2_name', '').strip() or None
        teammate2_usn = data.get('teammate2_usn', '').strip() or None
        # Optional teammate3 (legacy field; kept for compatibility)
        teammate3_name = data.get('teammate3_name', '').strip() or None
        teammate3_usn = data.get('teammate3_usn', '').strip() or None
        reg_time = datetime.utcnow().isoformat()
        
        conn = get_db_connection()
        cur = conn.cursor()
        # Check duplicates: team name
        cur.execute('SELECT 1 FROM team_registration WHERE team_name = ?', (team_name,))
        if cur.fetchone():
            flash('Team name already registered. Please choose a different name.', 'danger')
            conn.close()
            return redirect(url_for('index'))
        
        # Check USN duplicates for non-empty USNs
        usns = [leader_usn, teammate1_usn]
        if teammate2_usn:
            usns.append(teammate2_usn)
        if teammate3_usn:
            usns.append(teammate3_usn)
        placeholders = ' OR '.join([f"leader_usn = ?", f"teammate1_usn = ?", f"teammate2_usn = ?", f"teammate3_usn = ?"])
        for usn in usns:
            cur.execute(f'SELECT 1 FROM team_registration WHERE {placeholders}', (usn, usn, usn, usn))
            if cur.fetchone():
                flash(f'USN {usn} is already registered.', 'danger')
                conn.close()
                return redirect(url_for('index'))
        
        # Insert registration
        cur.execute(
            '''
            INSERT INTO team_registration (team_name, leader_name, leader_usn, leader_college, leader_phone,
                teammate1_name, teammate1_usn, teammate2_name, teammate2_usn, teammate3_name, teammate3_usn, registration_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (team_name, leader_name, leader_usn, leader_college, leader_phone,
             teammate1_name, teammate1_usn, teammate2_name, teammate2_usn, teammate3_name, teammate3_usn, reg_time)
        )
        conn.commit()
        conn.close()
        
        flash('Team registered successfully! We look forward to seeing you at Code, Bid & Build!', 'success')
        return redirect(url_for('index'))
    except sqlite3.IntegrityError as ie:
        # Unique constraint violated
        flash(f'Duplicate entry: {str(ie)}', 'danger')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred during registration: {str(e)}', 'danger')
        return redirect(url_for('index'))

# ===========================
# Routes - Admin Authentication
# ===========================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Verify credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ===========================
# Routes - Admin Dashboard
# ===========================
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard showing all registrations"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    per_page = 10
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cur = conn.cursor()
    params = []
    where_clause = ''
    if search_query:
        search_term = f'%{search_query}%'
        where_clause = 'WHERE team_name LIKE ? OR leader_name LIKE ? OR leader_usn LIKE ? OR leader_phone LIKE ?'
        params.extend([search_term, search_term, search_term, search_term])
    # Total count
    total_query = f'SELECT COUNT(*) FROM team_registration {where_clause}'
    cur.execute(total_query, params)
    total_teams = cur.fetchone()[0]
    # Fetch paginated rows
    list_query = f'SELECT * FROM team_registration {where_clause} ORDER BY registration_time DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    cur.execute(list_query, params)
    rows = cur.fetchall()
    registrations = []
    for row in rows:
        d = dict(row)
        # convert registration_time to datetime
        try:
            d['registration_time'] = datetime.fromisoformat(d['registration_time'])
        except Exception:
            d['registration_time'] = datetime.utcnow()
        # convert to simple object for template attribute access
        registrations.append(types.SimpleNamespace(**d))
    conn.close()
    # Build a simple pagination object
    total_pages = (total_teams + per_page - 1) // per_page
    pagination = types.SimpleNamespace(page=page, pages=total_pages, items=registrations, has_prev=(page>1), has_next=(page<total_pages), prev_num=(page-1), next_num=(page+1))
    return render_template('admin_dashboard.html', registrations=pagination, search_query=search_query, total_teams=total_teams)

# ===========================
# Routes - PDF Export
# ===========================
@app.route('/admin/export-pdf')
@login_required
def export_pdf():
    """Export all registrations to PDF using sqlite3 data"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM team_registration ORDER BY registration_time DESC')
        rows = cur.fetchall()
        conn.close()
        
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=1
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=1
        )
        elements.append(Paragraph('Code, Bid & Build', title_style))
        elements.append(Paragraph('Team Registration Report', subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        table_data = [['Team Name', 'Leader (USN)', 'Phone', 'College', 'Teammates', 'Registered']]
        for row in rows:
            teammates = f"{row['teammate1_name']} ({row['teammate1_usn']}), {row['teammate2_name']} ({row['teammate2_usn']}), {row['teammate3_name']} ({row['teammate3_usn']})"
            try:
                reg_time = datetime.fromisoformat(row['registration_time']).strftime('%Y-%m-%d %H:%M')
            except Exception:
                reg_time = ''
            table_data.append([
                row['team_name'],
                f"{row['leader_name']}\n({row['leader_usn']})",
                row['leader_phone'],
                row['leader_college'],
                teammates,
                reg_time
            ])
        
        table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 0.9*inch, 1.2*inch, 2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        elements.append(table)
        doc.build(elements)
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name=f'Code_Bid_Build_Registrations_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf')
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))

# ===========================
# Routes - Admin Delete
# ===========================
@app.route('/admin/delete/<int:team_id>', methods=['POST'])
@login_required
def delete_team(team_id):
    """Delete a team registration by id (admin only)"""
    try:
        # Preserve pagination/search parameters to return to the same view
        page = request.form.get('page', 1)
        search = request.form.get('search', '')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT team_name FROM team_registration WHERE id = ?', (team_id,))
        row = cur.fetchone()
        if not row:
            flash('Team not found.', 'warning')
            conn.close()
            return redirect(url_for('admin_dashboard', page=page, search=search))
        team_name = row['team_name']
        cur.execute('DELETE FROM team_registration WHERE id = ?', (team_id,))
        conn.commit()
        conn.close()
        flash(f"Team '{team_name}' deleted successfully.", 'success')
        return redirect(url_for('admin_dashboard', page=page, search=search))
    except Exception as e:
        flash(f'Error deleting team: {str(e)}', 'danger')
        return redirect(url_for('admin_dashboard'))

# ===========================
# Error Handlers
# ===========================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ===========================
# Run Application
# ===========================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
