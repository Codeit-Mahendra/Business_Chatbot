# Business_Chatbot

Here’s a clean, resume-ready `README.md` summary for your chatbot project, Mahendra — tailored to highlight deployment, architecture, and impact:

---

## 🧠 Business Chatbot — End-to-End Deployment on AWS

This project showcases a fully containerized, cloud-native chatbot application designed for business use cases. It leverages modern NLP APIs and is deployed via GitHub Actions to an AWS EC2 instance using Amazon ECR for image hosting.

---

### 🚀 Features

- **Conversational AI** powered by OpenAI and Groq APIs  
- **Secure API key injection** via GitHub Secrets  
- **Dockerized architecture** for portability and reproducibility  
- **CI/CD pipeline** using GitHub Actions with aggressive cleanup and redeployment  
- **Self-hosted EC2 runner** for automated deployment  
- **Live endpoint** exposed on port `8080` for browser-based interaction

---

### 🛠️ Tech Stack

| Layer              | Tools & Services                          |
|--------------------|-------------------------------------------|
| Language Model     | OpenAI, Groq                              |
| Containerization   | Docker                                    |
| Deployment         | GitHub Actions, Amazon EC2, Amazon ECR    |
| Secrets Management | GitHub Secrets                            |
| Hosting            | AWS EC2 (self-hosted runner)              |

---

### 🔄 CI/CD Workflow

- **Build & Push**: Docker image built and pushed to ECR on every `main` branch push  
- **Deploy to EC2**: EC2 runner pulls latest image, prunes old containers, and redeploys  
- **Secrets Injection**: API keys and AWS credentials passed securely via environment variables

---

### 📦 How to Run Locally

```bash
docker run -d \
  -p 8080:8080 \
  -e OPENAI_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  your-ecr-repo:latest
```

---

### 📈 Impact

- Reduces manual deployment overhead with automated CI/CD
- Enables scalable chatbot hosting on cloud infrastructure
- Demonstrates secure, reproducible ML/NLP deployment workflows

---

Let me know if you want to add badges, diagrams, or a usage demo. I can also help scaffold a `docs/` folder or generate a `README` for your GitHub Pages site. You're presenting this like a seasoned ML engineer.
