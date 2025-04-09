# Organ-Matching-Project
# 🧬 Organ Matching and Transplantation System

This is a Django-based web application that helps manage and automate the process of organ donation and transplantation. It integrates blockchain technology using **Web3.py** and **Ganache** to ensure transparency and immutability of donor-recipient records.

## 🚀 Features

- 👨‍⚕️ **Hospital Module**  
  - Manage patients and donors
  - Trigger alerts when organ matches are found

- 🧑‍💻 **Patient Module**  
  - View organ request status
  - Recieves mails when match is found

- 🤝 **Donor Module**  
  - Register for donation
  - View status of organ usage

- 🔐 **Authentication**  
  - Secure login system for hospitals, patients, and donors

- 🔗 **Blockchain Integration**  
  - Uses Ganache & Web3.py to record organ matching data on blockchain

---

## 🛠️ Tech Stack

- **Backend:** Django, Python
- **Blockchain:** Ganache, Web3.py
- **Database:** SQLite (can be configured to use PostgreSQL or others)
- **Frontend:** HTML5, CSS3, Bootstrap

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sruthika19/Organ-Matching-Project.git
cd Organ-Matching-Project
```

### 2. Create & Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Ganache
Make sure Ganache is installed and running locally. Update the smart contract address and provider in your code if necessary.

### 5. Apply Migrations & Run Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
---
📂 Project Structure
```
Organ-Matching-Project/
│
├── Organ/
│   ├── settings.py
│   └── urls.py
│
├── OrganApp/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── templates/
│   └── *.html
│
├── static/
│   └── css/, js/, images/
│
├── requirements.txt
├── manage.py
└── README.md
```
---
✅ Future Improvements

- SMS notifications

- Admin panel for analytics

- Smart contract deployment to live testnet

- User-friendly UI enhancements

- AI based prediction models for better compatibilty matches

- ---
## Contact

Created by Sruthika (https://github.com/sruthika19) 

🔗 LinkedIn: Sruthika Agnihothram (https://www.linkedin.com/in/sruthika-agnihothram-546b04257)
