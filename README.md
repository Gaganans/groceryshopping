"# groceryshopping" 
# Grocery Shopping Web Application

## 📌 Project Overview
The Grocery Shopping Web Application is a full-stack web project designed to facilitate online grocery shopping. It allows users to browse products, add items to their cart, and place orders conveniently. Admins can manage inventory and track orders efficiently. The application also integrates PayPal for secure and seamless online payments.

## 🚀 Features
- User authentication (Login/Register)
- Browse and search grocery items
- Add/remove items from the cart
- Secure PayPal payment gateway integration
- Order management for users and admins
- Responsive UI for mobile and desktop

## 🛠️ Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite / PostgreSQL
- **Payment Gateway:** PayPal
- **Version Control:** Git & GitHub

## 📂 Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Gaganans/grocery-shopping.git
   cd grocery-shopping
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (Admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Start the server:
   ```sh
   python manage.py runserver
   ```

## 📜 Usage
- Access the application at `http://127.0.0.1:8000/`
- Register or log in to start shopping
- Add items to your cart and proceed to checkout using PayPal
- Admins can log in at `/admin/` to manage inventory and orders

## 🤝 Contribution
Contributions are welcome! Feel free to fork the repo and submit a pull request.

## 📞 Contact
For any queries or collaboration, reach out via [GitHub](https://github.com/Gaganans).

---
🛠 **Developed by Gagana** 🚀
