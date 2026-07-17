# 😊 Emotion Recognition using AWS

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)
![Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900)
![S3](https://img.shields.io/badge/Amazon-S3-blue)
![API Gateway](https://img.shields.io/badge/API-Gateway-red)
![Rekognition](https://img.shields.io/badge/Amazon-Rekognition-green)
![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-blue)
![SQS](https://img.shields.io/badge/Amazon-SQS-yellow)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![HTML](https://img.shields.io/badge/HTML-Frontend-orange)

---

## 📌 Project Overview

Emotion Recognition using AWS is a cloud-based serverless application that captures an image from a user's webcam, uploads it to Amazon S3, detects facial emotions using Amazon Rekognition, stores the results in DynamoDB, and displays them on a responsive web interface.

The project demonstrates how multiple AWS services can work together to build a real-world AI-powered application.

---

# 🚀 Features

- Live webcam capture
- Upload image to Amazon S3
- REST API using API Gateway
- AWS Lambda backend
- Amazon Rekognition emotion detection
- Amazon DynamoDB result storage
- Amazon SQS asynchronous processing
- Responsive HTML frontend
- Real-time emotion analysis

---

# ☁ AWS Services Used

| Service | Purpose |
|----------|----------|
| Amazon S3 | Store uploaded images |
| AWS Lambda | Serverless backend |
| API Gateway | REST APIs |
| Amazon Rekognition | Detect facial emotions |
| Amazon DynamoDB | Store analysis results |
| Amazon SQS | Queue processing |

---

# 🏗 Architecture

Workflow:

User

↓

Frontend (HTML)

↓

API Gateway

↓

Lambda (upload.py)

↓

Amazon S3

↓

Amazon SQS

↓

Lambda (detect.py)

↓

Amazon Rekognition

↓

Amazon DynamoDB

↓

Lambda (results.py)

↓

Frontend

---

# 📂 Folder Structure

```
Emotion-Recognition-AWS
│
├── architecture
├── frontend
├── lambda
├── screenshots
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 📸 Project Screenshots

<img width="1875" height="891" alt="image" src="https://github.com/user-attachments/assets/c627a411-2b34-444b-b467-ea37e5891a0a" />
---
<img width="1895" height="902" alt="image" src="https://github.com/user-attachments/assets/57e3e0d7-5940-453e-a408-ac88e67e1d73" />

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/AbhishekPawar-1904/Emotion-Recognition-AWS.git
```

Go inside the project

```bash
cd Emotion-Recognition-AWS
```

Deploy Lambda functions to AWS.

Create an API Gateway.

Configure S3.

Create DynamoDB table.

Connect Rekognition and SQS.

Open the frontend.

---

# REST APIs

## Upload Image

POST

```
/upload
```

Uploads image to S3.

---

## Get Result

GET

```
/results?key=<image-key>
```

Returns detected emotions.

---

# Technologies Used

- HTML
- JavaScript
- Python
- AWS Lambda
- Amazon S3
- Amazon Rekognition
- Amazon SQS
- DynamoDB
- API Gateway

---

# Future Improvements

- User Authentication
- Emotion History
- Analytics Dashboard
- Mobile Support
- Face Comparison
- Multi-user Support

---

# Author

**Abhishek Pawar**

Computer Engineering Student

GitHub:

https://github.com/AbhishekPawar-1904

---

⭐ If you like this project, consider giving it a star.
