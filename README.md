# FastAPI Heroku App 🚀

This is a simple backend project built with **FastAPI**, containerized using **Docker**, and deployed to **Heroku**.

## 🌐 Live Demo

🔗 [https://fastapi-ishan-1fb4dd547b79.herokuapp.com](https://fastapi-ishan-1fb4dd547b79.herokuapp.com)  
📄 Swagger Docs: [https://fastapi-ishan-1fb4dd547b79.herokuapp.com/docs](https://fastapi-ishan-1fb4dd547b79.herokuapp.com/docs)

## 🛠 Tech Stack

- FastAPI
- Docker & Docker Compose
- Heroku
- Python 3.9+

## 🚀 How to Run Locally

**### 1. Clone the repo**
```bash
git clone https://github.com/IshanLenin/Social-Media-API-with-FastAPI.git
cd Social-Media-API-with-FastAPI
```
**###2. Run with Docker**
```
docker build -t fastapi .
docker run -d -p 8000:8000 fastapi
```
** OR**
```
docker-compose up --build
```
