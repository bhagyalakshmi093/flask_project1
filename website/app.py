from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import math

app = Flask(__name__)

# PostgreSQL connection parameters
DATABASE_URL = 'postgresql://postgres:Chinnu12?@127.0.0.1:5432/transactions'

# Database setup
def init_db():
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            description TEXT
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Pagination setup
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Get total record count
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_records = cursor.fetchone()[0]

    # Set the number of records per page
    records_per_page = 5

    # Get the current page from the query parameters, default is 1
    page = request.args.get('page', 1, type=int)
    total_pages = math.ceil(total_records / records_per_page)

    # Calculate the offset for the SQL query
    offset = (page - 1) * records_per_page

    # Fetch records for the current page
    cursor.execute("SELECT * FROM transactions LIMIT %s OFFSET %s", (records_per_page, offset))
    transactions = cursor.fetchall()
    conn.close()

    return render_template('index.html', transactions=[{
        'id': row[0],
        'name': row[1],
        'category': row[2],
        'amount': row[3],
        'date': row[4],
        'description': row[5],
    } for row in transactions], page=page, total_pages=total_pages)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        description = request.form['description']

        # Connect to PostgreSQL and insert the new transaction
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (name, category, amount, date, description) VALUES (%s, %s, %s, %s, %s)",
            (name, category, amount, date, description)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    # Render the form template for GET request
    return render_template('add_transaction.html')

@app.route('/delete/<int:id>')
def delete_transaction(id):
    # Connect to PostgreSQL and delete the transaction
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="127.0.0.1", 
        database="transactions", 
        user="postgres", 
        password="Chinnu12?"
    )
    cursor = conn.cursor()

    if request.method == 'POST':
        # Get updated form data
        name = request.form['name']
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        description = request.form['description']

        
        cursor.execute("""
            UPDATE transactions
            SET name = %s, category = %s, amount = %s, date = %s, description = %s
            WHERE id = %s
        """, (name, category, amount, date, description, transaction_id))

        conn.commit()
        conn.close()
        


        # Redirect to the transaction list after update
        return redirect(url_for('index'))
            # Use %s for placeholder
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()

    # If the transaction doesn't exist, redirect to the index
    if not transaction:
        return redirect(url_for('index'))

    # Render the edit form with the transaction data pre-filled
    return render_template('edit_transaction.html', transaction=transaction)


if __name__ == '__main__':
    init_db()  # Initialize the database if it doesn't exist
    app.run(debug=True)
