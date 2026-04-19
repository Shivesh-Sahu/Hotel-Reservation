import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
from datetime import date

app = Flask(__name__)
app.secret_key = "hotel_secret_123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "hotel@123"

# --- Database Connection ---
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sh82@iv53",       
        database="hotel_db"
    )

# --- HOME PAGE ---
@app.route('/')
def index():
    room_type = request.args.get('type', 'All')
    sort = request.args.get('sort', 'default')

    if sort == 'low':
        order = "ORDER BY price_per_night ASC"
    elif sort == 'high':
        order = "ORDER BY price_per_night DESC"
    else:
        order = "ORDER BY id ASC"

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if room_type != 'All':
        cursor.execute(
            f"SELECT * FROM rooms WHERE is_available = TRUE AND room_type = %s {order}",
            (room_type,)
        )
    else:
        cursor.execute(
            f"SELECT * FROM rooms WHERE is_available = TRUE {order}"
        )

    rooms = cursor.fetchall()
    db.close()
    return render_template('index.html', rooms=rooms, selected_type=room_type, sort=sort)

# --- BOOK A ROOM ---
@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book(room_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    #  ALWAYS fetch room (needed for both GET & POST)
    cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()

    # ---------------- POST ----------------
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        check_in = request.form['check_in']
        check_out = request.form['check_out']

        days = (datetime.strptime(check_out, '%Y-%m-%d') -
                datetime.strptime(check_in, '%Y-%m-%d')).days

        total = room['price_per_night'] * days

        # 🔍 Check conflict
        cursor.execute("""
            SELECT * FROM bookings
            WHERE room_id = %s
            AND NOT (%s <= check_in OR %s >= check_out)
        """, (room_id, check_out, check_in))

        conflict = cursor.fetchone()

        if conflict:
            db.close()
            return render_template(
                'book.html',
                room=room,
                error="Room already booked for selected dates"
            )

        #  Insert booking
        cursor.execute("""
            INSERT INTO bookings
            (guest_name, guest_email, guest_phone, room_id, check_in, check_out, total_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, email, phone, room_id, check_in, check_out, total))

        db.commit()
        db.close()

        #  REDIRECT (DO NOT render admin here)
        return redirect(url_for('admin'))

    # ---------------- GET ----------------
    db.close()
    return render_template('book.html', room=room)





# --- MY BOOKINGS ---
@app.route('/my_bookings')
def my_bookings():
    email = request.args.get('email', '')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, r.room_number, r.room_type
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE b.guest_email = %s
        ORDER BY b.booked_at DESC
    """, (email,))
    bookings = cursor.fetchall()
    db.close()
    return render_template('my_bookings.html', bookings=bookings, email=email)

# --- CANCEL BOOKING ---
@app.route('/cancel/<int:booking_id>')
def cancel(booking_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT room_id, guest_email FROM bookings WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    cursor.execute("UPDATE rooms SET is_available = TRUE WHERE id = %s", (booking['room_id'],))
    db.commit()
    db.close()
    return redirect(url_for('my_bookings', email=booking['guest_email']))

# --- ADMIN LOGIN ---
@app.route('/admin')
def admin():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 🔥 Spark data
    try:
        stats = pd.read_csv("room_stats.csv")
        top_room = stats.iloc[0]['room_id']
    except:
        top_room = "No data"

    #  Total bookings
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()['COUNT(*)']

    #  Revenue
    cursor.execute("SELECT SUM(total_price) FROM bookings")
    total_revenue = cursor.fetchone()['SUM(total_price)'] or 0

    #  Total rooms
    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()['COUNT(*)']

    #  Revenue per day
    cursor.execute("""
    SELECT check_in, SUM(total_price)
    FROM bookings
    GROUP BY check_in
    ORDER BY check_in
    """)

    rev_data = cursor.fetchall()

    rev_dates = [str(row['check_in']) for row in rev_data]
    revenues = [float(row['SUM(total_price)']) for row in rev_data]

    #  Availability
    today = date.today()

    cursor.execute("""
    SELECT COUNT(DISTINCT room_id)
    FROM bookings
    WHERE check_in <= %s AND check_out > %s
    """, (today, today))

    booked_rooms = cursor.fetchone()['COUNT(DISTINCT room_id)']
    available_rooms = total_rooms - booked_rooms
    
    #  Bookings per day
    cursor.execute("""
    SELECT check_in, COUNT(*) 
    FROM bookings 
    GROUP BY check_in
    ORDER BY check_in
    """)
    data = cursor.fetchall()

    dates = [str(row['check_in']) for row in data]
    counts = [row['COUNT(*)'] for row in data]
    cursor.execute("""
    SELECT b.*, r.room_number, r.room_type
    FROM bookings b
    JOIN rooms r ON b.room_id = r.id
    ORDER BY b.check_in DESC
    """)

    bookings = cursor.fetchall()

    db.commit()
    db.close()

    
    return render_template(
    'admin.html',
    total_bookings=total_bookings,
    total_revenue=total_revenue,
    total_rooms=total_rooms,
    available_rooms=available_rooms,
    top_room=top_room,
    dates=dates,
    counts=counts,
    rev_dates=rev_dates,
    revenues=revenues,
    bookings=bookings
)
if __name__ == '__main__':
     app.run(debug=True)
