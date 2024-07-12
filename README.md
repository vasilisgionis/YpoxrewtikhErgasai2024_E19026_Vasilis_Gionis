 # Υποχρεωτική Άσκηση Πληροφοριακών Συστημάτων 2024
> ΑΜ Ε19026 Βασίλης Γκιώνης 

## Περιεχόμενα 
1. Επιπλέον παραδοχές
2. Τεχνολογίες
3. Περιγραφή των αρχείων
4. Τρόπος Εκτέλεσης
5. Τρόπος Χρήσης 
6. Βιβλιογραφία

### 1. Επιπλέον παραδοχές
- για δική μας ευκολία οι κωδικοί αποθηκεύονται σε απλό text format
- λόγω προβλημάτων με την Date επέλέχτηκε η χρήση integer για τα date datas

### 2. Τεχνολογίες 
- Python
- Flask-PyMongo
- MongoDB
- Docker

### 3. Περιγραφή των αρχείων 
- Ο φάκελος **data** περιλαμβάνει όλα τα απαραίτητα δεδομένα όπως ζητήθηκε από την εκφώνηση σε περίπτωση που το container διαγραφεί
- Ο φάκελος **venv** περιέχει ένα εικονικό περιβάλλον Python το οποίο περιλεμβλανει την έκδοση Python που χρησιμοποιείται στην εργασία και περιέχει τα εγκατεστημένα πακέτα Python και εξαρτήσεις που είναι αναγκαίες για την λειτουργία του προγράμματος
- Το **Dockerfile** περιέχει όλα τα απαραίτητα δεδομένα για τη δημιουργία του DOcker Image του Flask application
- Το **Dockerfile.mongo** περιέχει όλες τις απαραίτητες εντολές για την δημιουργία του Docker Image της βάσης δεδομένων MongoDB
- Το **docker-compose.yml** το οποίο έχει τις εντολές οι οποίες εκτελούν την εκκίνηση της Flask application και της βάσης μας.
- Το **app.py** το οποίο είναι το βασικό αρχείο της εφαρμογής μας. Εκεί βρίσκονται όλες οι εντολές οι οποίες υλοποιούν τα διάφορα routes. Πιο συγκεκριμένα :
  * admin :( login(*POST* /admin/login), create doctor(*POST* /admin/doctor), delete doctor(*DELETE* /admin/doctor/<id του γιατρου προς διαγραφη>), update doctor(*PUT* /admin/doctor/<id του γιατρου προς ενημέρωση>), delete patient(*DELETE* /admin/patient/<id του ασθενη προς διαγραφη>))
  * doctor :( login(*POST* /doctor/login), appointments(*GET* /doctor/<id του γιατρου>/appointments), αλλαγή του κόστους του ραντεβού του(*PUT* /doctor/change_cost))
  * patient :( register(*POST* /patient/register), login(*POST* /patient/login), ραντεβού με γιατρό(*POST* /patient/book_appointment), προβολή όλων των ραντεβού του(*GET* /patient/<id του ασθενούς>/appointments), προβολή συγκεκριμένου ραντεβού(*GET* /patient/appointment/<id του ραντεβού>), ακύρωση ραντεβού(*DELETE* /patient/cancel_appointment)
- Τέλος το **requiriments.txt** περιλαμβάνει όλες τις βιβλιοθήκες που χρειαστήκαμε για την εφαρμογή.

### 4. Τρόπος εκτέλεσης
Για την εκτέλεση της εφαρμογής θα χρειαστεί : 
- να εγκαταστήσουμε τις βιβλιοθληκες από το requirements.txt 
  ```
  pip install -r requirements.txt
  ```
- με την χρήση του Docker Desktop πρέπει να βεβαιωθούμε ότι η MongoDB βάση μας λειτουργεί. Μπορούμε να χρησιμοποιήσουμε την παρακάτω εντολή στο cmd επίσης για μεγαλύτερη ευκολία
  ```
  docker-compose up --build
  ```
  το οποίο θα εκτελέσει τα 2 containers που έχουμε δημιουργήσει 
- έπειτα τρέχουμε το app.py (προσωπικά το τρέχω στο visual studio)
  ```
  python app.py
  ```
- εφόσον το terminal μας ενημερώνει ότι όλα κυλάνε ομαλά, μπορούμε με την χρήση του Postman να τεστάρουμε την λειτουργικότητα της εφαρμογής μας.

### 5. Τρόπος Χρήσης
Προτεινόμενος τρόπος χρήσης είναι χρησιμοποιώντας την εφαρμογή Postman. Εφόσον τρέξουμε την εφαρμογή και υπάρξει σύνδεση μεταξύ server και database μπορουμε να χρησιμοποιήσουμε το link και να το εισάγουμε στο Postman για να κάνουμε διάφορες διαδικασίες. Πιο συγκεκριμένα θα αναφερθούν οι εντολές για τον admin, έναν γιατρό και έναν ασθενή. Για ευκολία το link http://127.0.0.1:5000 θα το ονομάσω Α. 
- **Admin**
  - Login :
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/admin/login.
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username": "admin",
     "password":"@dm1n"
    }
    ```
  - Create doctor :
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/admin/doctor.
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "first_name": "Panayiotis",
     "last_name": "karamolegkos",
     "email": "karmolegkos@.com",
     "username": "sonem",
     "password": "12345",
     "specialization": "Cardiologist",
     "appointment_cost": 100
    }
    ```
  - Update doctor :
    Πάμε Postman και παταμε **PUT**.
    Στο URL βάζουμε Α/admin/doctor/<id>.
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "first_name": "Panagiotis",
     "last_name": "karamolegkos",
     "email": "karmolegkos@.com",
     "username": "sonem",
     "password": "12345",
     "specialization": "Cardiologist",
     "appointment_cost": 200
    }
    ```
  - Delete doctor :
    Πάμε Postman και παταμε **DELETE**.
    Στο URL βάζουμε Α/admin/doctor/<id>.
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username":"sonem"
    }
    ```
  - Delete patient :
    Πάμε Postman και παταμε **DELETE**.
    Στο URL βάζουμε Α/admin/patient/<id>.
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username":"vasillisgio"
    }
    ```
- **Doctor**
  - Login :
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/doctor/login
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username": "sonem",
     "password": "12345"
    }
     ```
  - Προβολή των ραντεβού του :
    Πάμε Postman και παταμε **GET**.
    Στο URL βάζουμε Α/doctor/<id>/appointments
    
  - Change Cost :
    Πάμε Postman και παταμε **PUT**.
    Στο URL βάζουμε Α/doctor/change_cost
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username":"sonem",
     "new_cost":210
    }
    ```
- **Patient**
  - Register :
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/patient/register
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "first_name": "vasilis",
     "last_name": "gionis",
     "email": "vasillisgionis@gmail.com",
     "amka": "E19026",
     "birthdate": "2000-09-06",
     "username": "vasillisgio",
     "password": "54321"
    }
    ```
  - Login :
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/patient/login
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "username":"vasillisgio",
     "password":"54321"
    }
    ```
  - Ραντεβού με γιατρό
    Πάμε Postman και παταμε **POST**.
    Στο URL βάζουμε Α/patient/book_appointment
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "doctor_id": "<doctor_id>",
     "patient_name": "Vasilis Gionis",
     "date": 20240710,
     "time": 1000,
     "reason": "Checkup",
     "patient_id": "<patient_id>"
    }
    ```
    (τα date και time είναι σε int όπως αναφέρθηκε και στην ενότητα 1)

  - Προβολή ραντεβού (specific and not specific)
    Πάμε Postman και παταμε **GET**.
    Στο URL βάζουμε Α/patient/<id>/appointments για τα ραντεβού του ασθενή.
    Και Α/patient/appointment/<id> για ένα συγκεκριμένο ραντεβού

  - Ακύρωση ραντεβού :
    Πάμε Postman και παταμε **DELETE**.
    Στο URL βάζουμε Α/patient/cancel_appointment
    Έπειτα πάμε στο body, JSON format και γράφουμε :
    ```
    {
     "appointment_id": "<appointment_id>"
    }
    ```
### 6. Βιβλιογραφία 
- Διαφάνειες εργαστηριών
- GeeksForGeeks
- StackOverflow
- Youtube 

