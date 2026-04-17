# ☕ Smart Cafe API - Reservation System

## Deskripsi Proyek
**Smart Cafe API** adalah RESTful API untuk sistem reservasi meja kafe yang dibangun menggunakan **FastAPI**. Proyek ini memungkinkan pengguna untuk:

- ✅ Mendaftar dan login ke sistem
- ✅ Melihat daftar meja yang tersedia
- ✅ Membuat reservasi meja dengan validasi waktu
- ✅ Melihat riwayat reservasi sendiri
- ✅ Membatalkan reservasi yang sudah dibuat

Proyek ini dibuat sebagai **Ujian Tengah Semester (UTS)** mata kuliah **Pemrograman Web Lanjutan** dengan menerapkan konsep:
- Microservices architecture
- RESTful API design
- JWT Authentication
- ORM dengan SQLAlchemy
- Validasi input dengan Pydantic

---

## Teknologi yang Digunakan

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| **Framework** | FastAPI | 0.104.1 |
| **Bahasa** | Python | 3.11+ |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Database** | SQLite | - |
| **Autentikasi** | JWT (python-jose) | 3.3.0 |
| **Password Hashing** | bcrypt | 4.0.1 |
| **Validasi** | Pydantic | 2.10.4 |
| **Server** | Uvicorn | 0.24.0 |

---

Relasi: User 1:N Reservation
Table 1:N Reservation

---

## Instalasi & Menjalankan

### Prasyarat
- Python 3.11 atau lebih baru
- pip (Python package manager)

### Langkah-langkah

#### 1. Masuk ke folder proyek
```bash
cd smart-cafe-api
2. Buat Virtual Environment (Rekomendasi)
Windows:

bash
python -m venv venv
venv\Scripts\activate
MacOS / Linux:

bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
Atau install manual:

bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart email-validator
4. Jalankan Server
bash
uvicorn main:app --reload
5. Buka di Browser
API Server: http://127.0.0.1:8000

Swagger UI (Dokumentasi): http://127.0.0.1:8000/docs

ReDoc (Alternatif): http://127.0.0.1:8000/redoc

Daftar Endpoint API
🔐 Autentikasi
Method	Endpoint	Deskripsi	Auth	Status Code
POST	/auth/register	Registrasi user baru	No	201 Created
POST	/auth/login	Login & dapatkan token JWT	No	200 OK
🪑 Manajemen Meja
Method	Endpoint	Deskripsi	Auth	Status Code
POST	/tables/	Menambah meja baru	No	201 Created
GET	/tables/	Mendapatkan semua daftar meja	No	200 OK
📅 Reservasi
Method	Endpoint	Deskripsi	Auth	Status Code
POST	/reservations/	Membuat reservasi baru	Bearer Token	201 Created
GET	/reservations/	Mendapatkan reservasi user sendiri	Bearer Token	200 OK
DELETE	/reservations/{id}	Membatalkan reservasi	Bearer Token	200 OK
ℹ️ Lainnya
Method	Endpoint	Deskripsi	Auth	Status Code
GET	/	Root endpoint (welcome message)	No	200 OK
GET	/health	Health check	No	200 OK
Contoh Request & Response
1. Register User
Request:

http
POST http://127.0.0.1:8000/auth/register
Content-Type: application/json

{
    "username": "mahasiswa",
    "email": "mahasiswa@unhas.ac.id",
    "password": "123456"
}
Response (201 Created):

json
{
    "id": 1,
    "username": "mahasiswa",
    "email": "mahasiswa@unhas.ac.id"
}
2. Login
Request:

http
POST http://127.0.0.1:8000/auth/login
Content-Type: application/json

{
    "username": "mahasiswa",
    "password": "123456"
}
Response (200 OK):

json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
3. Create Table
Request:

http
POST http://127.0.0.1:8000/tables/
Content-Type: application/json

{
    "table_number": 1,
    "capacity": 4
}
Response (201 Created):

json
{
    "id": 1,
    "table_number": 1,
    "capacity": 4,
    "is_available": true
}
4. Create Reservation (Butuh Token)
Request:

http
POST http://127.0.0.1:8000/reservations/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
    "table_id": 1,
    "start_time": "2026-04-25T19:00:00",
    "end_time": "2026-04-25T21:00:00"
}
Response (201 Created):

json
{
    "id": 1,
    "user_id": 1,
    "table_id": 1,
    "start_time": "2026-04-25T19:00:00",
    "end_time": "2026-04-25T21:00:00",
    "created_at": "2026-04-17T10:40:14.789012"
}
5. Double Booking (Error)
Request (waktu sama):

http
POST http://127.0.0.1:8000/reservations/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
    "table_id": 1,
    "start_time": "2026-04-25T19:00:00",
    "end_time": "2026-04-25T21:00:00"
}
Response (400 Bad Request):

json
{
    "detail": "Table already booked for this time slot"
}
6. Get My Reservations (Butuh Token)
Request:

http
GET http://127.0.0.1:8000/reservations/
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Response (200 OK):

json
[
    {
        "id": 1,
        "user_id": 1,
        "table_id": 1,
        "start_time": "2026-04-25T19:00:00",
        "end_time": "2026-04-25T21:00:00",
        "created_at": "2026-04-17T10:40:14.789012"
    }
]
7. Delete Reservation (Butuh Token)
Request:

http
DELETE http://127.0.0.1:8000/reservations/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Response (200 OK):

json
{
    "message": "Reservation cancelled successfully"
}
Fitur Validasi
Pydantic Validations
Field	Validasi	Error Message
username	min 3 chars, max 50 chars	"String should have at least 3 characters"
email	Must be valid email format	"value is not a valid email address"
password	min 6 chars	"String should have at least 6 characters"
table_number	≥ 1	"Input should be greater than or equal to 1"
capacity	1 - 20	"Input should be less than or equal to 20"
start_time	Cannot be in the past	"start_time cannot be in the past"
end_time	Must be > start_time	"end_time must be after start_time"
Business Logic Validations
Validasi	Deskripsi	HTTP Status
Double Booking	Cek apakah meja sudah dibooking pada waktu yang sama	400 Bad Request
User Exists	Cek username/email sudah terdaftar	400 Bad Request
Table Exists	Cek apakah meja dengan ID tersebut ada	404 Not Found
Reservation Ownership	User hanya bisa cancel reservasi milik sendiri	403 Forbidden
Testing dengan Postman
Import Collection
Buka Postman

Klik Import → Upload Files

Pilih file SmartCafeAPI.postman_collection.json

Klik Import

Setup Environment Variables
Buat environment baru: Smart Cafe Local

Tambahkan variable:

base_url = http://127.0.0.1:8000

authToken = (kosongkan dulu)

Testing Sequence
No	Request	Method	Endpoint	Expected
1	Register	POST	/auth/register	201 Created
2	Login	POST	/auth/login	200 OK + Token
3	Create Table	POST	/tables/	201 Created
4	Create Reservation	POST	/reservations/	201 Created
5	Double Booking Test	POST	/reservations/	400 Bad Request
6	Get My Reservations	GET	/reservations/	200 OK
7	Delete Reservation	DELETE	/reservations/{id}	200 OK
Note: Request 4-7 memerlukan Bearer Token yang otomatis tersimpan setelah login.

Troubleshooting
Error: bcrypt version / AttributeError
Solusi:

bash
pip uninstall bcrypt passlib -y
pip install bcrypt==4.0.1 passlib==1.7.4
Error: password cannot be longer than 72 bytes
Solusi: Sudah otomatis ditangani oleh bcrypt version 4.0.1

Error: ModuleNotFoundError
Solusi: Install dependencies yang kurang

bash
pip install -r requirements.txt
Port 8000 sudah digunakan
Solusi: Gunakan port berbeda

bash
uvicorn main:app --reload --port 8001
Postman tidak bisa akses localhost
Solusi:

Gunakan 127.0.0.1 bukan localhost

Atau install Postman Desktop Agent

Author
Nama: Indira Ramayani
NIM: H071241056
Mata Kuliah: Pemrograman Web Lanjutan
Semester: Genap 2025/2026
Universitas: Universitas Hasanuddin