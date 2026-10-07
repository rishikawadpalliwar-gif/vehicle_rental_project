from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection
from datetime import datetime

app = Flask(__name__)
app.secret_key = "vehicle-rental-secret-key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vehicles")
def vehicles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.vehicle_id, v.registration_no, v.brand, v.model,
               v.vehicle_year, v.rental_price_per_day, v.status,
               c.category_name
        FROM vehicle v
        JOIN category c ON v.category_id = c.category_id
        ORDER BY v.vehicle_id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("vehicles.html", vehicles=rows)


@app.route("/customer")
def customer():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_id, name, email, phone FROM customer ORDER BY customer_id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("customer.html", customers=rows)


@app.route("/rental", methods=["GET", "POST"])
def rental():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        customer_id = request.form["customer_id"]
        vehicle_id = request.form["vehicle_id"]
        rental_date = request.form["rental_date"]
        return_date = request.form["return_date"]

        cursor.execute("""
            SELECT rental_price_per_day
            FROM vehicle
            WHERE vehicle_id = %s AND status = 'Available'
        """, (vehicle_id,))
        vehicle = cursor.fetchone()

        if not vehicle:
            cursor.close()
            conn.close()
            flash("Vehicle is not available.", "error")
            return redirect(url_for("rental"))

        start = datetime.strptime(rental_date, "%Y-%m-%d").date()
        end = datetime.strptime(return_date, "%Y-%m-%d").date()
        days = (end - start).days
        if days <= 0:
            days = 1

        total = float(vehicle["rental_price_per_day"]) * days

        cursor.execute("""
            INSERT INTO rental
            (customer_id, vehicle_id, rental_date, return_date, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, 'Booked')
        """, (customer_id, vehicle_id, rental_date, return_date, total))

        cursor.execute("""
            UPDATE vehicle SET status = 'Rented'
            WHERE vehicle_id = %s
        """, (vehicle_id,))

        conn.commit()
        cursor.close()
        conn.close()
        flash("Vehicle booked successfully!", "success")
        return redirect(url_for("bookings"))

    cursor.execute("SELECT customer_id, name FROM customer ORDER BY name")
    customers = cursor.fetchall()

    cursor.execute("""
        SELECT vehicle_id, registration_no, brand, model, rental_price_per_day
        FROM vehicle
        WHERE status = 'Available'
        ORDER BY vehicle_id
    """)
    available_vehicles = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template(
        "rental.html",
        customers=customers,
        vehicles=available_vehicles
    )


@app.route("/booking")
def bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            r.rental_id,
            c.name,
            v.brand,
            v.model,
            r.rental_date,
            r.return_date,
            r.total_amount,
            r.status
        FROM rental r
        JOIN customer c ON r.customer_id = c.customer_id
        JOIN vehicle v ON r.vehicle_id = v.vehicle_id
        ORDER BY r.rental_id DESC
    """)
    bookings_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("booking.html", bookings=bookings_data)


@app.route("/return/<int:rental_id>")
def return_vehicle(rental_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT vehicle_id FROM rental WHERE rental_id = %s",
        (rental_id,)
    )
    rental_row = cursor.fetchone()

    if rental_row:
        vehicle_id = rental_row["vehicle_id"]

        cursor.execute("""
            UPDATE rental
            SET status = 'Returned', return_date = CURDATE()
            WHERE rental_id = %s
        """, (rental_id,))

        cursor.execute("""
            UPDATE vehicle
            SET status = 'Available'
            WHERE vehicle_id = %s
        """, (vehicle_id,))

        conn.commit()
        flash("Vehicle returned successfully!", "success")
    else:
        flash("Rental record not found.", "error")

    cursor.close()
    conn.close()
    return redirect(url_for("bookings"))


if __name__ == "__main__":
    app.run(debug=True)
