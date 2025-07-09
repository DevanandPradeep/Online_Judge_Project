# 🖥️ Online Judge Platform

A full-stack **Online Coding Judge** 

---

## 🚀 Features

✅ Multi-language Code Execution (Python, C, C++)  
✅ Run Code with Custom Inputs <br>
✅ Submission with Hidden Test Cases  
✅ Time Limit Exceeded (TLE) Detection  
✅ AI Hint Generation   
✅ Solved Problems Tracking  
✅ Leaderboard to display top performers  
✅ Fully Dockerized for quick deployment  
✅ AWS EC2 Deployment ready

---

## 🛠 Tech Stack

| Frontend      | Backend          | Database             | AI Integration | Deployment        |
|--------------|------------------|----------------------|----------------|-------------------|
| HTML, CSS    | Django (Python)   | SQLite / PostgreSQL   | Gemini API | Docker + AWS EC2  |

---

## 📦 How to Run Locally with Docker

```bash
# 1. Clone this repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Build Docker image
docker build -t online-judge .

# 3. Run the Docker container
docker run -d -p 8000:8000 online-judge
