from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="EDU_AIMuseum"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

# Visitors Management
@app.route('/visitors')
def visitors():
    cursor.execute("SELECT * FROM Visitors")
    visitors = cursor.fetchall()
    return render_template('visitors.html', visitors=visitors)

@app.route('/add_visitor', methods=['POST'])
def add_visitor():
    name = request.form['name']
    nid = request.form['nid']
    contact = request.form['contact']
    visit_date = request.form['visit_date']
    cursor.execute("INSERT INTO Visitors (name, nid, contact, visit_date) VALUES (%s, %s, %s, %s)", 
                   (name, nid, contact, visit_date))
    db.commit()
    return redirect('/visitors')

# Sections Management
@app.route('/sections')
def sections():
    cursor.execute("SELECT * FROM Sections")
    sections = cursor.fetchall()
    return render_template('sections.html', sections=sections)

@app.route('/add_section', methods=['POST'])
def add_section():
    section_name = request.form['section_name']
    description = request.form['description']
    cursor.execute("INSERT INTO Sections (section_name, description) VALUES (%s, %s)", 
                   (section_name, description))
    db.commit()
    return redirect('/sections')

# Specimens Management
@app.route('/specimens')
def specimens():
    cursor.execute("""
        SELECT Specimens.specimen_id, Specimens.name, Specimens.description, 
               Specimens.developer_name, Specimens.developer_type, Sections.section_name 
        FROM Specimens 
        JOIN Sections ON Specimens.section_id = Sections.section_id
    """)
    specimens = cursor.fetchall()
    return render_template('specimens.html', specimens=specimens)

@app.route('/add_specimen', methods=['POST'])
def add_specimen():
    name = request.form['name']
    description = request.form['description']
    developer_name = request.form['developer_name']
    developer_type = request.form['developer_type']
    section_id = request.form['section_id']
    cursor.execute("""
        INSERT INTO Specimens (name, description, developer_name, developer_type, section_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, description, developer_name, developer_type, section_id))
    db.commit()
    return redirect('/specimens')

# Visits Management
@app.route('/visits')
def visits():
    cursor.execute("""
        SELECT Visits.visit_id, Visitors.name AS visitor_name, Sections.section_name, Visits.visit_time
        FROM Visits
        JOIN Visitors ON Visits.visitor_id = Visitors.visitor_id
        JOIN Sections ON Visits.section_id = Sections.section_id
    """)
    visits = cursor.fetchall()
    return render_template('visits.html', visits=visits)

@app.route('/add_visit', methods=['POST'])
def add_visit():
    visitor_id = request.form['visitor_id']
    section_id = request.form['section_id']
    visit_time = request.form['visit_time']
    cursor.execute("INSERT INTO Visits (visitor_id, section_id, visit_time) VALUES (%s, %s, %s)", 
                   (visitor_id, section_id, visit_time))
    db.commit()
    return redirect('/visits')

if __name__ == '__main__':
    app.run(debug=True)
