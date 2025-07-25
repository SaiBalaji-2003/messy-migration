# CHANGES.md

## 🛠 Refactoring Summary: messy-migration User Management API

---

### ✅ Major Issues Identified

1. **SQL Injection Vulnerability**  
   - The original code used f-strings directly in SQL queries.  
   - Resolved by switching to parameterized queries to prevent SQL injection.

2. **Plaintext Password Storage**  
   - Passwords were being stored in plain text in the database.  
   - Replaced with secure hashing using `werkzeug.security.generate_password_hash` and verification via `check_password_hash`.

3. **Lack of Separation of Concerns**  
   - All logic was embedded inside `app.py`.  
   - Refactored into:
     - `db.py`: Database connection handling
     - `routes/user_routes.py`: All route logic
     - `utils/security.py`: Password hashing utilities

4. **Missing Error Handling**  
   - No `try/except` blocks were used, risking crashes with malformed input.  
   - Added structured error handling and meaningful HTTP status codes.

5. **Unsafe JSON Parsing**  
   - Replaced `request.get_data()` with safer and cleaner `request.get_json()`.

6. **Poor Code Readability**  
   - Introduced meaningful variable names, consistent formatting, and modular structure.

---

### 🔧 Refactoring Details

#### 📁 Project Structure
- Implemented a modular design with clear separation of route logic and utilities.
- Used Flask Blueprints to register routes cleanly.

#### 🔐 Security Enhancements
- Passwords are now securely hashed before storage.
- Parameterized SQL queries used throughout to prevent injection.

#### 🧪 Maintainability
- Code is now easier to test, debug, and extend.
- Functions are single-responsibility and logically grouped.

---

### 📘 Tools & Libraries Used

- **ChatGPT (OpenAI)** – Used for code suggestions and guidance.
- **Flask** – Web framework for API handling.
- **Werkzeug** – For secure password hashing and verification.

---

### 📌 Assumptions

- User IDs are numeric and auto-incremented.
- Basic input validation is acceptable for this refactor (can be extended later).

---

### ⏱ Time Taken

- Approximately 2 hours (excluding testing/debugging cycles).

---

### 🚀 If I Had More Time

- Add unit and integration tests using `pytest`.
- Implement schema validation with `marshmallow` or `pydantic`.
- Add centralized logging and configuration handling via `.env`.
- Integrate Swagger/Postman for auto-generating API documentation.

---

✅ **Application fully tested and running at**: `http://localhost:5009`