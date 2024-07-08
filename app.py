from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/HospitalDB"
mongo = PyMongo(app)

# Important Information
SPECIALIZATIONS = ["Radiologist", "Hematologist", "Allergist", "Pathologist", "Cardiologist"]
START_HOUR = 900
END_HOUR = 1700

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "@dm1n"

# Home route
@app.route('/')
def home():
    return "Welcome to the Medical Appointment System"

# Admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data['username'] == ADMIN_USERNAME and data['password'] == ADMIN_PASSWORD:
        return jsonify({"message": "Admin login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Admin creates a doctor
@app.route('/admin/doctor', methods=['POST'])
def create_doctor():
    data = request.get_json()
    if not mongo.db.doctors.find_one({"username": data['username']}) and not mongo.db.doctors.find_one({"email": data['email']}):
        doctor = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'username': data['username'],
            'password': data['password'],  # Store plain text password
            'specialization': data['specialization'],
            'appointment_cost': data['appointment_cost']
        }
        if data['specialization'] not in SPECIALIZATIONS:
            return jsonify({"message": f"Specialization must be one of {SPECIALIZATIONS}"}), 400
        mongo.db.doctors.insert_one(doctor)
        return jsonify({"message": "Doctor created successfully"}), 201
    else:
        return jsonify({"message": "Doctor with this username or email already exists"}), 400

# Admin updates doctor information
@app.route('/admin/doctor/<id>', methods=['PUT'])
def update_doctor(id):
    data = request.get_json()
    result = mongo.db.doctors.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Doctor updated successfully"}), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

# Admin changes doctor password
@app.route('/admin/doctor/password', methods=['PUT'])
def change_doctor_password():
    data = request.get_json()
    result = mongo.db.doctors.update_one({"username": data['username']}, {"$set": {"password": data['new_password']}})
    if result.matched_count:
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

# Admin deletes a doctor
@app.route('/admin/doctor/<id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(id)})
    if doctor:
        mongo.db.appointments.delete_many({"doctor_id": id})
        mongo.db.doctors.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Doctor and related appointments deleted successfully"}), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

# Admin deletes a patient
@app.route('/admin/patient/<id>', methods=['DELETE'])
def delete_patient(id):
    patient = mongo.db.patients.find_one({"_id": ObjectId(id)})
    if patient:
        mongo.db.appointments.delete_many({"patient_id": id})
        mongo.db.patients.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Patient and related appointments deleted successfully"}), 200
    else:
        return jsonify({"message": "Patient not found"}), 404

# Patient registration
@app.route('/patient/register', methods=['POST'])
def register_patient():
    data = request.get_json()
    if not mongo.db.patients.find_one({"username": data['username']}) and not mongo.db.patients.find_one({"email": data['email']}):
        patient = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'amka': data['amka'],
            'birthdate': data['birthdate'],
            'username': data['username'],
            'password': data['password']  # Store plain text password
        }
        mongo.db.patients.insert_one(patient)
        return jsonify({"message": "Patient registered successfully"}), 201
    else:
        return jsonify({"message": "Patient with this username or email already exists"}), 400

# Patient login
@app.route('/patient/login', methods=['POST'])
def patient_login():
    data = request.get_json()
    patient = mongo.db.patients.find_one({"username": data['username']})
    if patient and patient['password'] == data['password']:
        return jsonify({"message": "Patient login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Patient books an appointment
@app.route('/patient/book_appointment', methods=['POST'])
def book_appointment():
    data = request.get_json()
    doctor = mongo.db.doctors.find_one({"specialization": data['specialization']})
    if doctor:
        if data['time'] < START_HOUR or data['time'] >= END_HOUR:
            return jsonify({"message": "Doctor not available at this time"}), 400

        existing_appointments = mongo.db.appointments.find({
            "doctor_id": str(doctor['_id']),
            "date": data['date'],
            "time": data['time']
        })

        if existing_appointments.count() == 0:
            appointment = {
                'doctor_id': str(doctor['_id']),
                'doctor_name': f"{doctor['first_name']} {doctor['last_name']}",
                'patient_id': data['patient_id'],
                'patient_name': data['patient_name'],
                'date': data['date'],  # Format: YYYYMMDD as int
                'time': data['time'],  # Format: HHMM as int
                'reason': data['reason'],
                'cost': doctor['appointment_cost'],
                'specialization': doctor['specialization']
            }
            mongo.db.appointments.insert_one(appointment)
            return jsonify({"message": "Appointment booked successfully"}), 201
        else:
            return jsonify({"message": "Time slot already booked"}), 400
    else:
        return jsonify({"message": "No doctor available for the given specialization"}), 404

# View doctor's future appointments
@app.route('/doctor/<id>/appointments', methods=['GET'])
def view_doctor_appointments(id):
    appointments = list(mongo.db.appointments.find({"doctor_id": id}))
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
    return jsonify(appointments), 200

# Doctor login
@app.route('/doctor/login', methods=['POST'])
def doctor_login():
    data = request.get_json()
    doctor = mongo.db.doctors.find_one({"username": data['username']})
    if doctor and doctor['password'] == data['password']:
        return jsonify({"message": "Doctor login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Doctor changes appointment cost
@app.route('/doctor/change_cost', methods=['PUT'])
def change_appointment_cost():
    data = request.get_json()
    result = mongo.db.doctors.update_one({"username": data['username']}, {"$set": {"appointment_cost": data['new_cost']}})
    if result.matched_count:
        return jsonify({"message": "Appointment cost updated successfully"}), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

# Patient views their appointments
@app.route('/patient/<id>/appointments', methods=['GET'])
def view_patient_appointments(id):
    appointments = list(mongo.db.appointments.find({"patient_id": id}))
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
    return jsonify(appointments), 200

# Patient views details of a specific appointment
@app.route('/patient/appointment/<id>', methods=['GET'])
def view_appointment_details(id):
    appointment = mongo.db.appointments.find_one({"_id": ObjectId(id)})
    if appointment:
        appointment['_id'] = str(appointment['_id'])
        return jsonify(appointment), 200
    else:
        return jsonify({"message": "Appointment not found"}), 404

# Patient cancels an appointment
@app.route('/patient/cancel_appointment', methods=['DELETE'])
def cancel_appointment():
    data = request.get_json()
    result = mongo.db.appointments.delete_one({"_id": ObjectId(data['appointment_id'])})
    if result.deleted_count:
        return jsonify({"message": "Appointment cancelled successfully"}), 200
    else:
        return jsonify({"message": "Appointment not found"}), 404
 #admin sees every doctor   
@app.route('/admin/doctors', methods=['GET'])
def get_doctors():
    try:
        doctors = list(mongo.db.doctors.find({}))
        for doctor in doctors:
            doctor['_id'] = str(doctor['_id'])
            doctor['password'] = "hidden"  # To hide the password in the response
        return jsonify(doctors), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
