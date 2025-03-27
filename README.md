# 📚 Peer Review System
A Django-based system where users can **submit assignments**, **review peers**, and **manage their work efficiently**. 📝✅

![Peer Review System](https://via.placeholder.com/800x400?text=Peer+Review+System) <!-- (Replace with actual screenshot) -->

---

## 🚀 **Features**
✔️ User Authentication (Login & Logout)  
✔️ Submit and Review Assignments  
✔️ Upload and Delete Assignments (Admin/Uploader only)  
✔️ Secure User Access (Only logged-in users can review or upload)  
✔️ Admin Panel Access for Management  

---

## 🏗 **Installation Guide**
### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/HyperCoder234/peer_review_system.git
cd peer_review_system
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
🛠 Tech Stack
Django (Backend)

SQLite / PostgreSQL (Database)

HTML, CSS (Bootstrap) (Frontend)

JavaScript (optional)

git checkout -b feature-branch
git add .
git commit -m "Added new feature"
git push origin feature-branch
🎯 To-Do (Future Features)
 Add Review Comments Feature

 Implement Rating System

 Dark Mode UI 🌙

