# 💸 Expense Tracker API

A backend service for tracking personal expenses — flexible, secure, and ready for production.  
Built with **FastAPI**, **PostgreSQL**, and **Docker** — perfect as a standalone backend or for integration with a mobile or web frontend.

## ✨ Features

- 📊 Expense tracking via clean, RESTful API  
- 🐳 Dockerized for fast local setup  
- ⚡ Asynchronous FastAPI architecture  
- 🔌 Dependency Injection via punq for decoupled, testable components  
- 🛢 PostgreSQL + volume-mounted data persistence  
- 🔐 Environment-based config handling  

> ✅ Designed to be lightweight, extensible, and ideal for learning or small-scale production use.

---

## 🚀 Quick start

### 1. Clone the repository

```bash
git clone https://github.com/Moses-93/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create the .env file in the project root

```bash
touch .env
```

### 3. Set environment variables for PostgreSQL

Open `.env` and paste the following:

```env
PG_USER=your_user
PG_PASSWORD=your_password
PG_DB=your_database
PG_HOST=your_hostname
PG_PORT=your_port
```

### 4. Create a folder to persist Postgres data

```bash
mkdir -p ./pg_data
```

Normally, Docker will handle permissions automatically on first run if the folder belongs to your user.

If you run into permission errors:

```bash
sudo chown -R $USER:$USER ./pg_data
```

### 5. Build and run the Docker containers

```bash
docker compose up --build
```
