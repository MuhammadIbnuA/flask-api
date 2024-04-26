from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'


app.config['MYSQL_HOST'] = 'mysql-flask-mysqlflask.e.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_8x7avq3i6RhOwcdfb9y'
app.config['MYSQL_DB'] = 'crud'
app.config['MYSQL_PORT'] = 14168
# Configure SQLAlchemy
mysql = MySQL(app)

# Define your model (replace with your actual table structure)
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     phone = db.Column(db.String(15))
# with app.app_context():
#     db.create_all()

#     def serialize(self):
#         return {
#         'id': self.id,
#         'name': self.name,
#         'email': self.email,
#         'phone': self.phone
#     }



def check_mysql_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return True
    except Exception as e:
        print("Error connecting to MySQL:", str(e))
        return False


@app.route('/')
def index():
    return "Welcome to the CRUD application!"


@app.route('/insert', methods=['POST'])
def insert():
    # Basic input validation
    if not request.form.get('name') or not request.form.get('email'):
        return jsonify({'message': 'Please provide name and email'}), 400

    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')  # Handle optional phone number

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO student (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    mysql.connection.commit()
    return jsonify({'message': 'Data Inserted Successfully'})


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    try:
        # Convert ID to integer for validation
        id_data = int(id_data)
    except ValueError:
        return jsonify({'message': 'Invalid ID format'}), 400

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return jsonify({'message': 'Record Has Been Deleted Successfully'}) if cur.rowcount > 0 else jsonify({'message': 'Record not found'}), 404


@app.route('/update', methods=['POST'])
def update():
    # Basic input validation
    if not request.form.get('id') or not request.form.get('name') or not request.form.get('email'):
        return jsonify({'message': 'Please provide ID, name and email'}), 400

    id_data = request.form['id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')  # Handle optional phone number

    try:
        # Convert ID to integer for validation
        id_data = int(id_data)
    except ValueError:
        return jsonify({'message': 'Invalid ID format'}), 400

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE student
        SET name=%s, email=%s, phone=%s
        WHERE id=%s
    """, (name, email, phone, id_data))
    mysql.connection.commit()
    return jsonify({'message': 'Data Updated Successfully'}) if cur.rowcount > 0 else jsonify({'message': 'Record not found'}), 404


@app.route('/get', methods=['GET'])
def get_all_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

if __name__ == "__main__":
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
