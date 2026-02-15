from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
from datetime import datetime
from risk_engine import calculate_risk

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


# ✅ FIXED FLASK INITIALIZATION (IMPORTANT)
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


# ================= DATABASE INIT ================= #

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        symptoms TEXT,
        blood_pressure INTEGER,
        heart_rate INTEGER,
        temperature REAL,
        conditions TEXT,
        risk_level TEXT,
        department TEXT,
        confidence REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ================= PATIENT ID GENERATOR ================= #

def generate_patient_id():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    year = datetime.now().year

    cursor.execute(
        "SELECT patient_id FROM patients WHERE patient_id LIKE ? ORDER BY patient_id DESC LIMIT 1",
        (f"ATR-{year}-%",)
    )

    last = cursor.fetchone()

    if last:
        last_number = int(last[0].split("-")[-1])
    else:
        last_number = 0

    new_number = last_number + 1
    new_id = f"ATR-{year}-{str(new_number).zfill(4)}"

    conn.close()
    return new_id


# ================= HOME ================= #

@app.route("/")
def index():
    return render_template("index.html")


# ================= REDIRECT TO ADD PATIENT ================= #

@app.route("/patient_checkup")
def patient_checkup():
    return redirect("/add_patient")


# ================= DASHBOARD ================= #

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    total = len(patients)
    stable = len([p for p in patients if p[8] == "Stable"])
    moderate = len([p for p in patients if p[8] == "Moderate Attention"])
    critical = len([p for p in patients if p[8] == "Critical Priority"])

    return render_template(
        "dashboard.html",
        total=total,
        stable=stable,
        moderate=moderate,
        critical=critical
    )


# ================= VIEW PATIENTS ================= #

@app.route("/patients/<risk_type>")
def view_patients(risk_type):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if risk_type == "All":
        cursor.execute("SELECT * FROM patients")
    else:
        cursor.execute("SELECT * FROM patients WHERE risk_level = ?", (risk_type,))

    patients = cursor.fetchall()
    conn.close()

    return render_template(
        "patients.html",
        patients=patients,
        risk_type=risk_type
    )


# ================= ADD PATIENT ================= #

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        age = int(request.form["age"])
        gender = request.form["gender"]

        symptoms_list = request.form.getlist("symptoms")
        conditions_list = request.form.getlist("conditions")

        symptoms = ", ".join(symptoms_list)
        conditions = ", ".join(conditions_list)

        bp = int(request.form["blood_pressure"])
        hr = int(request.form["heart_rate"])
        temp = float(request.form["temperature"])

        (
            risk,
            confidence,
            severity_index,
            department,
            priority,
            wait_time,
            explanation,
            key_factors,
            factor_weights
        ) = calculate_risk(
            age,
            bp,
            hr,
            temp,
            conditions_list,
            symptoms_list
        )

        if request.form.get("action") == "save":

            patient_id = generate_patient_id()

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id,
                age,
                gender,
                symptoms,
                bp,
                hr,
                temp,
                conditions,
                risk,
                department,
                confidence / 100
            ))

            conn.commit()
            conn.close()

            return redirect("/dashboard")

        return render_template(
            "add_patient.html",
            analyzed=True,
            risk=risk,
            confidence=confidence,
            severity_index=severity_index,
            department=department,
            priority=priority,
            wait_time=wait_time,
            explanation=explanation,
            key_factors=key_factors,
            factor_weights=factor_weights,
            form_data=request.form
        )

    return render_template(
        "add_patient.html",
        analyzed=False,
        form_data=None
    )


# ================= PDF EXPORT ================= #

@app.route("/export_pdf/<risk_type>")
def export_pdf(risk_type):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if risk_type == "All":
        cursor.execute("SELECT * FROM patients")
    else:
        cursor.execute("SELECT * FROM patients WHERE risk_level = ?", (risk_type,))

    patients = cursor.fetchall()
    conn.close()

    if not patients:
        return redirect("/dashboard")

    file_name = os.path.join(BASE_DIR, f"{risk_type.replace(' ', '_')}_patients_report.pdf")

    doc = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(
        Paragraph(f"<b>AURA TRIAGE - {risk_type} Patients Report</b>", styles['Title'])
    )
    elements.append(Spacer(1, 0.3 * inch))

    data = [["ID", "Age", "Gender", "Risk", "Department", "Confidence"]]

    for p in patients:
        data.append([
            p[0],
            str(p[1]),
            p[2],
            p[8],
            p[9],
            f"{round(p[10] * 100, 2)}%"
        ])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)
    doc.build(elements)

    return send_file(file_name, as_attachment=True)


# ================= MAIN ================= #

if __name__ == "__main__":
    app.run(debug=True)
