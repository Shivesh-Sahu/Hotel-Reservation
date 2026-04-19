# 🏨 Hotel Grand — Room Reservation System

A full-stack hotel booking web application built with Flask, MySQL, and PySpark, designed to provide a seamless reservation experience for users and real-time analytics for administrators.

## ✨ Features

### 👤 Guest Features
- Browse rooms with images, amenities, and pricing
- Filter by room type (Single, Double, Suite)
- Sort by price (low → high / high → low)
- Book rooms with real-time availability check
- Conflict-free booking using SQL date overlap logic
- View bookings using email
- One-click cancellation

### 🧑‍💼 Admin Features
- Dashboard with live KPIs (Bookings, Revenue, Rooms)
- 📊 Booking Trends Chart (Chart.js)
- 💰 Revenue Trends Chart
- 🔥 Most Booked Room (PySpark analytics)
- Full bookings table with guest details

### ⚡ Big Data Analytics
- PySpark processes booking data
- Computes total revenue & booking trends
- Ranks most booked rooms
- Outputs CSV for dashboard integration

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, Jinja2
- **Charts:** Chart.js
- **Analytics:** Apache PySpark + Pandas

## 🧠 Key Highlights
- Real-time conflict detection (no double booking)
- End-to-end data pipeline (Flask → MySQL → PySpark → Dashboard)
- Booking.com-inspired UI
- Scalable and modular architecture

## 🚀 Future Improvements
- Authentication system (Login/Register)
- Payment gateway integration (Razorpay/Stripe)
- Email notifications
- Predictive analytics (ML models)
- Mobile responsive UI

## 👨‍💻 Author
**Shivesh Kumar Sahu**  
B.Tech IT (Data Engineering)
