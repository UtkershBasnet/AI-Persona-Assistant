
# AI-Study-Planner

## Description


## Languages
TypeScript, Python, JavaScript, CSS

## Topics


## Stars
0

## README
  # cap at 3000 chars per repo
# AI Study Planner - Backend

Backend API for the AI-Powered Adaptive Study Planner built with FastAPI, Gemini API, and Pinecone.

## Features

- 🔐 **User Authentication** - JWT-based authentication with secure password hashing
- 📄 **Document Upload** - Upload and process PDF study materials  
- 🤖 **RAG System** - Retrieval-Augmented Generation for intelligent Q&A
- 🔍 **Smart Search** - Semantic search using Gemini embeddings and Pinecone
- 💬 **AI Answers** - Context-aware answers powered by Gemini Pro

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM with SQLite
- **Gemini API** - Google's AI for embeddings and text generation
- **Pinecone** - Vector database for semantic search
- **LangChain** - Document processing and chunking
- **JWT** - Secure authentication tokens

## Prerequisites

- Python 3.8+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Pinecone API key ([Sign up here](https://www.pinecone.io/))

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
DATABASE_URL=sqlite:///./study_planner.db
SECRET_KEY=your-secret-key-here-generate-a-random-string

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=study-planner-docs

# Application Settings
UPLOAD_DIR=./uploads
VECTORSTORE_DIR=./vectorstores
```

**To generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run the Server

```bash
python run.py
```

The API will be available at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires auth)

### Documents

- `POST /api/documents/upload` - Upload PDF document (requires auth)
- `POST /api/documents/query` - Ask questions about documents (requires auth)
- `GET /api/documents/list` - List all uploaded documents (requires auth)
- `DELETE /api/documents/{id}` - Delete a document (requires auth)

## Usage Examples

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "username": "student1",
    "password": "securepass123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Upload a PDF

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@physics_textbook.pdf"
```

### 4. Ask Questions

```bash
curl -X POST http://localhost:8000/api/documents/query \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Newton'\''s second law?"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   └── documents.py     # Document routes
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── document.py      # Document model
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py          # Auth schemas
│   │   └── document.py      # Document schemas
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── rag_engine.py    # RAG processing
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── security.py      # Auth utilities
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt         # Python dependencies
└── run.py                   # Development server
```

## Development

### Running with Auto-Reload

```bash
python run.py
```

This starts the server with auto-reload enabled for development.

### Accessing API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Pinecone Index Not Found

**Solution:** Create a Pinecone index manually:
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with dimension `768` and metric `cosine`
3. Update `.env` with the index name

### Issue: "Could not validate credentials"

**Solution:** Make sure you're passing the Bearer token correctly:
```bash
-H "Authorization: Bearer YOUR_ACTUAL_TOKEN"
```

## Next Steps (Week 2)

- [ ] Study planner agent with schedule generation
- [ ] Pomodoro timer endpoints
- [ ] Progress tracking and analytics
- [ ] Exam score prediction

## License

MIT
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.


---


# knowledge_vault-frontend

## Description


## Languages
JavaScript, TypeScript

## Topics


## Stars
0

## README
# Knowledge Vault - Mobile App

A modern, cross-platform mobile application built with React Native and Expo. Knowledge Vault serves as your AI-assisted "second brain," allowing you to capture ideas and find them using semantic search.

## Problem Statement
Users frequently encounter interesting information or have creative ideas that they document but later struggle to find because they cannot remember the exact keywords used. Knowledge Vault addresses this by integrating with an AI backend to provide meaning-based retrieval, making personal knowledge truly accessible.

## Tech Stack Used
- **Frontend Framework:** [React Native](https://reactnative.dev/) with [Expo](https://expo.dev/) (SDK 54)
- **Navigation:** [Expo Router](https://docs.expo.dev/router/introduction/) (File-based routing)
- **Styling:** Vanilla React Native Stylesheets with Lucide Icons
- **Networking:** [Axios](https://axios-http.com/)
- **State Management:** React Context API (AuthContext)
- **Animations:** React Native Reanimated

## Features Implemented
- **Secure Authentication:** Persistent login session management.
- **Dynamic Knowledge Feed:** View and manage your stored knowledge items.
- **AI-Powered Search:** Dedicated search tab for semantic, meaning-based queries.
- **Rich Editor:** Intuitive interface for adding and editing knowledge items with titles, content, and tags.
- **Native Experience:** Smooth navigation and haptic feedback.

## How to Run Locally

### Prerequisites
- Node.js (LTS version)
- Expo Go app on your mobile device (for testing on physical hardware)
- Backend service running (see [Backend README](../backend/README.md))

### Steps
1. **Navigate to frontend directory:**
   ```bash
   cd knowledge_vault-frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Configure API URL:**
   Update the `API_URL` in `app.json` to point to your backend's local IP address:
   ```json
   "extra": {
     "API_URL": "http://YOUR_LOCAL_IP:8000"
   }
   ```
4. **Start the development server:**
   ```bash
   npx expo start
   ```
5. **Open the app:**
   Scan the QR code with the Expo Go app (Android) or Camera app (iOS).

## Project Structure
- `/app`: Main application routes and screens (using Expo Router).
- `/components`: Reusable UI elements (cards, inputs, buttons).
- `/context`: Global state providers (Authentication).
- `/api`: API client configuration and network calls.
- `/constants`: Theme and styling constants.

---


# web-chatting-app

## Description


## Languages
JavaScript, HTML, CSS

## Topics


## Stars
0

## README
# Real-Time Web Chatting Application

## Overview

A live chat platform built using the MERN stack (MongoDB, Express.js, React.js, Node.js) combined with Socket.IO for real-time interactions. The application enables users to message each other instantly, check online presence, exchange images, and personalize the interface with various themes.

## Features

- **Instant Messaging**: Seamless real-time chat functionality powered by WebSockets (Socket.IO).
- **User Authentication**: Secure sign-up and login system with encrypted password storage.
- **Online Users**: Real-time indicators showing which users are currently online.
- **Image Uploads**: Users can send and receive image messages.
- **User Search & Filtering**: Easily find users and filter by online status.
- **Theme Options**: Customize the interface with multiple available themes via the settings page.

## Tech Stack

### Frontend
- React.js  
- Zustand (for state management)  
- Tailwind CSS (for UI styling)  

### Backend
- Node.js  
- Express.js  
- MongoDB  

### Real-time Communication
- Socket.IO  

### Cloud Storage
- Cloudinary (for media/image uploads)  

## Getting Started

### Run Locally

To run the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Install dependencies and build the project:
   ```bash
   npm install
   npm run build
3. Start the server:
   ```bash
   npm run start
4. Open your browser and navigate to http://localhost:3000 to use the application.

### Using the Browser by the deployed link
1. Launch the application in your preferred browser.
2. Register for an account or log in using existing credentials.
3. Start chatting with connected users in real time!

---

## License

This project is open-source and available for modification and distribution under the MIT License.

---


# CampusFixIt

## Description


## Languages
JavaScript

## Topics


## Stars
0

## README
# Campus FixIt

## Overview
Campus FixIt is a React Native mobile application designed for reporting and tracking campus maintenance issues. It features a robust backend built with Node.js and Express, connected to a MongoDB database.

## Features
- **User Authentication**: Student and Admin login/registration using JWT.
- **Role-based Access**: 
  - Students can report issues with titles, descriptions, categories, and photos.
  - Admins can view all issues and update their status (Open -> In Progress -> Resolved).
- **Issue Tracking**: Real-time status updates and filtering.

## Tech Stack
- **Frontend**: React Native (Expo), React Navigation, Axios, Expo Image Picker.
- **Backend**: Node.js, Express, MongoDB (Mongoose), JSON Web Token (JWT).

## Setup Instructions

### Prerequisites
- Node.js installed
- MongoDB installed and running locally

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd campus-fixit/backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```
   The server runs on `http://localhost:5000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd campus-fixit/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Update API URL (If testing on Emulator/Physical Device):
   - Open `src/utils/api.js`
   -  Replace `localhost` with your machine's local IP address (e.g., `192.168.1.X`) if using a physical device or Android Emulator (use `10.0.2.2`).
4. Start the Expo app:
   ```bash
   npx expo start
   ```

## API Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/issues` - Create a new issue (Student only)
- `GET /api/issues` - Get all issues
- `PATCH /api/issues/:id` - Update issue status (Admin only)

## License
MIT
  # cap at 3000 chars per repo


---


# knowledge_vault-backend

## Description


## Languages
Python

## Topics


## Stars
0

## README
# Knowledge Vault - Backend

An AI-powered backend for a personal knowledge management system. This service provides secure authentication, CRUD operations for knowledge items, and semantic search capabilities using machine learning embeddings.

## Problem Statement
In an era of information overload, individuals often struggle to organize and retrieve specific insights from their various notes and documents. Traditional keyword-based search often fails to find relevant information if the exact terms aren't used. Knowledge Vault solves this by using AI embeddings to enable semantic search, allowing users to find information based on meaning rather than just keywords.

## Tech Stack Used
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database:** [MongoDB](https://www.mongodb.com/) (NoSQL)
- **AI/ML:** [Sentence-Transformers](https://www.sbert.net/) (for text embeddings)
- **Authentication:** JWT (JSON Web Tokens) with `python-jose` and `passlib`
- **Other:** `python-dotenv`, `pymongo`, `uvicorn`

## Features Implemented
- **User Authentication:** Secure registration and login using hashed passwords and JWT.
- **Knowledge Management:** Full CRUD (Create, Read, Update, Delete) for knowledge items.
- **AI Embeddings:** Automatic generation of vector embeddings for all stored knowledge.
- **Semantic Search:** Meaning-based retrieval using vector similarity.
- **CORS Middleware:** Enabled for cross-origin communication with the mobile frontend.

## How to Run Locally

### Prerequisites
- Python 3.8+
- MongoDB instance (Local or Atlas)

### Steps
1. **Navigate to backend directory:**
   ```bash
   cd knowledge_vault-backend
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   Create a `.env` file in the `backend/` directory with:
   ```env
   MONGODB_URL=your_mongodb_connection_string
   SECRET_KEY=your_secret_key_for_jwt
   ```
5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`.

## API Documentation (Basic)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Login and receive a JWT token | No |
| `GET`  | `/knowledge/` | Fetch all knowledge items for the user | Yes |
| `POST` | `/knowledge/` | Create a new knowledge item (triggers embedding) | Yes |
| `PUT`  | `/knowledge/{id}` | Update an existing knowledge item | Yes |
| `DELETE` | `/knowledge/{id}` | Delete a knowledge item | Yes |
| `POST` | `/search` | Perform a semantic search query | Yes |

*Detailed Swagger documentation is available at `http://localhost:8000/docs` when the server is running.*
  # cap at 3000 chars per repo


---


# Config_Validator_Service

## Description


## Languages
Java, Dockerfile

## Topics


## Stars
0

## README
  # cap at 3000 chars per repo
# Config Validator Service - Project Summary

## 📋 Quick Reference

**Project Name:** Config Validator Service with CI/CD Pipeline  
**Technology Stack:** Java 17, Spring Boot 4.0.1, Maven, Docker, Kubernetes  
**Infrastructure:** AWS EC2, Self-hosted Kubernetes Cluster  
**Deployment URL:** http://3.80.114.190:30080

---

## 🎯 Project Overview

A **stateless REST service** that validates application configuration data for correctness and security, integrated with a **production-grade CI/CD pipeline** featuring comprehensive security scanning and automated deployment.

### Core API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/validate-config` | POST | Validate configuration against predefined rules |
| `/schema` | GET | Retrieve configuration contract/schema |
| `/health` | GET | Health check for monitoring |

---

## 🔄 CI/CD Pipeline Architecture

### CI Pipeline (12 Stages)
1. ✅ **Checkout Code** - Clone repository
2. ☕ **Setup Java 17** - Configure build environment
3. 🔍 **Linting (Checkstyle)** - Code quality validation
4. 🛡️ **SAST (CodeQL)** - Static security analysis
5. 📦 **SCA (OWASP)** - Dependency vulnerability scan
6. 🧪 **Unit Tests** - Automated testing
7. 🏗️ **Build (Maven)** - Compile and package
8. 🐳 **Docker Build** - Containerization
9. 🔒 **Container Scan (Trivy)** - Image security scan
10. ✔️ **Container Testing** - Smoke tests
11. 🔑 **DockerHub Login** - Registry authentication
12. 📤 **Push to Registry** - Publish image

### CD Pipeline (3 Stages)
1. ⚙️ **Deploy to Kubernetes** - Rolling update deployment
2. 🔐 **DAST (OWASP ZAP)** - Dynamic security testing
3. 📊 **Upload Reports** - Security findings

---

## 🔐 Security Controls

### Multi-Layered Security Approach

| Layer | Tool | Stage | Coverage |
|-------|------|-------|----------|
| **SAST** | CodeQL | CI - Before Build | Source code vulnerabilities |
| **SCA** | OWASP Dependency Check | CI - Before Build | Third-party CVEs |
| **Container** | Trivy | CI - After Build | OS + App vulnerabilities |
| **DAST** | OWASP ZAP | CD - After Deploy | Runtime vulnerabilities |

### Security Scan Results
- ✅ **CodeQL**: 0 critical, 0 high severity issues
- ✅ **OWASP Dependency Check**: 0 known vulnerabilities
- ✅ **Trivy**: 0-2 high severity (base image dependent)
- ✅ **ZAP**: 0 exploitable vulnerabilities

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Pipeline Duration** | 10-15 minutes |
| **CI Pipeline** | 8-12 minutes |
| **CD Pipeline** | 2-3 minutes |
| **Docker Image Size** | ~280 MB |
| **Success Rate** | 95%+ |
| **Deployment Strategy** | Rolling Update (zero downtime) |

---

## ✨ Key Features

### Application Features
- ✅ Environment-aware validation (dev/test/prod)
- ✅ Security-first password validation
- ✅ Boundary condition checks
- ✅ Clear, human-readable error messages
- ✅ Stateless design (no database)
- ✅ RESTful API design

### DevOps Features
- ✅ Automated quality gates
- ✅ Multi-stage Docker builds
- ✅ Kubernetes orchestration
- ✅ Zero-downtime deployments
- ✅ Comprehensive security scanning
- ✅ Fast feedback loop (10-15 min)

---

## 🏗️ Infrastructure

### Kubernetes Configuration
```yaml
Deployment:
  - Replicas: 1
  - Container Port: 8080
  - Image Pull Policy: Always
  - Namespace: default

Service:
  - Type: NodePort
  - Port: 80
  - Target Port: 8080
  - Node Port: 30080
```

### AWS EC2 Instance
- **Instance Type**: Self-hosted Kubernetes cluster
- **Public IP**: 3.80.114.190
- **Exposed Port**: 30080

---

## 🧪 Validation Rules

| Field | Type | Validation |
|-------|------|------------|
| `environment` | String | Required; One of: dev, test, prod |
| `debug` | Boolean | Required; Must be false in prod |
| `maxConnections` | Integer | Required; 1-100 (dev), 1-500 (test), 1-2000 (prod) |
| `adminPassword` | String | Required; Min 8 chars, mixed case, numbers, special chars |

---

## 📈 Test Results

### Successful Test Cases
✅ Valid production configuration  
✅ Environment-specific connection limits  
✅ Password complexity enforcement  

### Failed Test Cases (As Expected)
❌ Debug enabled in production → Rejected  
❌ Weak password → Rejected  
❌ Connection limit exceeded → Rejected  
❌ Invalid environment → Rejected  

---

## 🚀 Deployment Workflow

```
Developer Push → GitHub
    ↓
CI Pipeline (12 stages)
    ↓
Docker Image → DockerHub
    ↓
CD Pipeline Triggered
    ↓
Kubernetes Deployment
    ↓
Rolling Update
    ↓
DAST Security Scan
    ↓
Production Ready ✅
```

---

## 📝 Current Limitations

1. **Versioning**: Using `latest` tag (no semantic versioning)
2. **High Availability**: Single replica, single EC2 instance
3. **Monitoring**: No centralized logging or APM
4. **Testing**: No integration or performance tests
5. **Security**: No runtime monitoring or image signing
6. **Network**: No ingress controller or SSL/TLS

---

## 🎯 Recommended Improvements

### High Priority
1. ⭐ Implement semantic versioning
2. ⭐ Add Kubernetes health checks
3. ⭐ Configure horizontal pod autoscaling
4. ⭐ Add integration tests

### Medium Priority
5. 🔒 Implement Ingress with SSL/TLS
6. 📊 Add Prometheus & Grafana monitoring
7. 📝 Centralized logging (ELK stack)
8. ⚡ Performance testing in pipeline

### Low Priority
9. 🔄 Blue-green deployment
10. 🌪️ Chaos engineering tests
11. 🔧 GitOps with ArgoCD
12. 🚪 API Gateway implementation

---

## 📚 Project Files

### Key Files
- **CI Pipeline**: [.github/workflows/ci.yml](file:///Users/utkershbasnet/Downloads/config-validator-service/.github/workflows/ci.yml)
- **CD Pipeline**: [.github/workflows/cd.yml](file:///Users/utkershbasnet/Downloads/config-validator-service/.github/workflows/cd.yml)
- **Dockerfile**: [Dockerfile](file:///Users/utkershbasnet/Downloads/config-validator-service/Dockerfile)
- **K8s Deployment**: [k8s/deployment.yaml](file:///Users/utkershbasnet/Downloads/config-validator-service/k8s/deployment.yaml)
- **K8s Service**: [k8s/service.yaml](file:///Users/utkershbasnet/Downloads/config-validator-service/k8s/service.yaml)
- **Build Config**: [pom.xml](file:///Users/utkershbasnet/Downloads/config-validator-service/pom.xml)
- **Code Quality**: [checkstyle.xml](file:///Users/utkershbasnet/Downloads/config-validator-service/checkstyle.xml)

### Application Code
- **Controller**: `ValidationController.java` - REST endpoints
- **Service**: `ValidationService.java` - Validation logic
- **Models**: `ConfigRequest.java`, `ValidationResult.java`, `SchemaDefinition.java`
- **Tests**: `ValidationServiceTest.java`

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Building production-grade CI/CD pipelines
- ✅ Implementing DevSecOps practices
- ✅ Container orchestration with Kubernetes
- ✅ Multi-layered security scanning
- ✅ Automated testing and deployment
- ✅ Infrastructure as Code
- ✅ Zero-downtime deployment strategies

---

## 📞 Quick Test Commands

### Test Valid Configuration
```bash
curl -X POST http://3.80.114.190:30080/validate-config \
  -H "Content-Type: application/json" \
  -d '{
    "environment": "prod",
    "debug": false,
    "maxConnections": 1500,
    "adminPassword": "SecureP@ss123"
  }'
```

### Get Schema
```bash
curl http://3.80.114.190:30080/schema
```

### Health Check
```bash
curl http://3.80.114.190:30080/health
```

---

**Date**: January 20, 2026  
**Author**: Utkersh Basnet

---


# CityNavigator

## Description


## Languages
TypeScript, CSS, JavaScript

## Topics


## Stars
0

## README
Deployed Link: https://city-navigator-pi.vercel.app/

Demo Video: https://drive.google.com/file/d/1padZ5S9XxEvvR2Ep6BMu56KkMd5C4ezU/view?usp=sharing

## 🎯 Project Goals

**Primary Objective**: Create an interactive web-based route-finding application that demonstrates real-world applications of graph algorithms through city navigation, showcasing the practical implementation of shortest path algorithms with visual feedback.

**Educational Goals**:

- Demonstrate graph theory concepts in a tangible, real-world context
- Compare algorithm performance and behavior differences
- Provide interactive visualization of algorithm execution
- Bridge theoretical computer science with practical applications


## 🚀 Key Features

### **Interactive Map Interface**

- **OpenStreetMap Integration**: Real map tiles with Leaflet.js
- **Dynamic Node Selection**: Click-to-select start/end points via dropdowns or map popups
- **Real-time Path Visualization**: Animated route display with directional arrows
- **Bidirectional Edge Display**: Visual representation of two-way streets


### **Dual Algorithm Implementation**

- **Dijkstra's Algorithm**: Guaranteed shortest path with uniform exploration
- **A* Algorithm**: Heuristic-guided pathfinding for faster convergence
- **Algorithm Switching**: Real-time comparison between approaches
- **Performance Metrics**: Step counting, distance calculation, and exploration tracking


### **Educational Visualization**

- **Node State Tracking**: Visual indicators for start, end, and explored nodes
- **Algorithm Statistics**: Complexity analysis, pros/cons comparison
- **Exploration Order**: Step-by-step visualization of node visitation
- **Path Reconstruction**: Clear route display with distance labels


### **Responsive Design**

- **Mobile-Friendly Interface**: Adaptive layout for all screen sizes
- **Interactive Controls**: Intuitive algorithm selection and route planning
- **Real-time Feedback**: Loading states and calculation progress


## 🛠️ Implementation Highlights

### **Frontend Architecture**

- **Next.js 15 + React**: Modern full-stack framework with App Router
- **TypeScript**: Type-safe development with custom interfaces
- **Tailwind CSS + shadcn/ui**: Consistent, responsive design system
- **Client-Side Rendering**: Proper hydration handling for map components


### **Graph Data Structure**

```typescript
interface GraphNode {
  id: string
  name: string
  lat: number
  lng: number
  type: "landmark" | "transport" | "education" | "commercial" | "medical" | "recreation"
}

interface GraphEdge {
  from: string
  to: string
  weight: number
  distance: number
  time: number
}
```

### **Algorithm Optimizations**

- **Early Termination**: Stops search immediately upon reaching target
- **Bidirectional Edge Handling**: Treats all roads as two-way unless specified
- **Efficient Data Structures**: Uses Sets and Maps for O(1) lookups
- **Memory Management**: Proper cleanup of map instances and event listeners


### **Real-World Mapping**

- **Coordinate System**: Latitude/longitude positioning
- **Distance Calculations**: Euclidean distance heuristics for A*
- **Visual Scaling**: Automatic map bounds fitting
- **Interactive Markers**: Custom styled nodes with type indicators


## 📚 Graph Concepts & Algorithms Implemented

### **Core Graph Theory Concepts**

- **Graph Representation**: Adjacency list structure with weighted edges
- **Bidirectional Graphs**: Two-way traversal for realistic city navigation
- **Weighted Edges**: Distance, time, and cost considerations
- **Graph Connectivity**: Path existence validation


### **Shortest Path Algorithms**

#### **1. Dijkstra's Algorithm**

- **Implementation**: Complete single-source shortest path
- **Data Structures**: Priority queue simulation with distance tracking
- **Complexity**: O((V + E) log V) time complexity
- **Features**:

- Guaranteed optimal solution
- Uniform exploration pattern
- Works with non-negative weights
- Early termination optimization





#### **2. A* (A-Star) Algorithm**

- **Implementation**: Heuristic-guided pathfinding
- **Heuristic Function**: Euclidean distance to target
- **Data Structures**: Open/closed sets with f-score tracking
- **Features**:

- Faster convergence than Dijkstra
- Goal-directed search
- Admissible heuristic ensures optimality
- Reduced node exploration





### **Graph Traversal Techniques**

- **Neighbor Discovery**: Bidirectional edge traversal
- **Path Reconstruction**: Backtracking through parent pointers
- **Visited Node Tracking**: Exploration order visualization
- **Distance Propagation**: Relaxation of edge weights


### **Algorithm Analysis & Comparison**

- **Performance Metrics**: Step counting and exploration tracking
- **Space Complexity**: Memory usage optimization
- **Time Complexity**: Big-O analysis display
- **Practical Trade-offs**: Speed vs. guarantee comparisons


### **Visualization Techniques**

- **Graph Rendering**: Node and edge visualization on map
- **Algorithm Animation**: Step-by-step exploration display
- **State Management**: Real-time algorithm state tracking
- **Interactive Feedback**: User-driven algorithm execution


## 🎓 Educational Value

This project demonstrates:

- **Real-world Applications**: How graph algorithms solve practical problems
- **Algorithm Comparison**: Trade-offs between different approaches
- **Visual Learning**: Interactive exploration of abstract concepts
- **Performance Analysis**: Understanding computational complexity
- **Data Structure Design**: Efficient graph representation

---


# Patient-Management-System

## Description


## Languages
Java, Dockerfile

## Topics


## Stars
0

## README
# 🏥 Patient Management System

A **microservices-based** Patient Management System built with **Spring Boot**, featuring inter-service communication via **gRPC** and **Apache Kafka**, secured with **JWT authentication**, and unified through a **Spring Cloud API Gateway**.

> [!NOTE]
> This project is currently **under active development** and not all features are fully implemented yet.

---

## 📐 Architecture Overview

```
                         ┌─────────────────────┐
                         │    API Gateway       │
                         │    (Port 4004)       │
                         └──────┬───────┬───────┘
                     JWT        │       │
                  Validation    │       │
                         ┌──────┘       └──────┐
                         ▼                     ▼
               ┌──────────────────┐  ┌──────────────────┐
               │  Auth Service    │  │ Patient Service   │
               │  (Port 4005)     │  │ (Port 4000)       │
               │  [PostgreSQL]    │  │ [PostgreSQL]       │
               └──────────────────┘  └──┬──────────┬─────┘
                                        │ gRPC     │ Kafka
                                        ▼          ▼
                              ┌──────────────┐  ┌─────────────────┐
                              │   Billing    │  │  Analytics      │
                              │   Service    │  │  Service        │
                              │ (Port 4001)  │  │  (Port 4002)    │
                              │ (gRPC: 9001) │  │                 │
                              └──────────────┘  └─────────────────┘
```

---

## 🧩 Services

| Service | Port | Description |
|---|---|---|
| **API Gateway** | `4004` | Routes external requests to internal services, validates JWT tokens on protected routes |
| **Auth Service** | `4005` | Handles user authentication — login & JWT token generation/validation |
| **Patient Service** | `4000` | Core CRUD operations for patient records; publishes events to Kafka; calls Billing Service via gRPC |
| **Billing Service** | `4001` (HTTP) / `9001` (gRPC) | Creates billing accounts for patients; exposes a gRPC API |
| **Analytics Service** | `4002` | Consumes patient events from Kafka for analytics processing |

---

## 🛠 Tech Stack

- **Language:** Java 21
- **Framework:** Spring Boot 3.x / 4.x
- **API Gateway:** Spring Cloud Gateway (WebFlux)
- **Security:** Spring Security + JWT (jjwt)
- **Database:** PostgreSQL (patient-service, auth-service)
- **ORM:** Spring Data JPA / Hibernate
- **Inter-Service Communication:**
  - **gRPC** — Patient Service → Billing Service
  - **Apache Kafka** — Patient Service → Analytics Service (Protobuf-serialized events)
- **API Docs:** Springdoc OpenAPI (Swagger UI)
- **Build:** Maven
- **Containerization:** Docker (multi-stage builds)

---

## 📁 Project Structure

```
patient_management/
├── api-gateway/            # Spring Cloud Gateway — routing & JWT filter
├── auth-service/           # Authentication — login, token validation
├── patient-service/        # Patient CRUD, gRPC client, Kafka producer
├── billing-service/        # gRPC billing account service
├── analytics-service/      # Kafka consumer for patient events
├── api-requests/           # HTTP request files for testing REST APIs
│   ├── auth-service/
│   └── patient-service/
└── grpc-requests/          # HTTP request files for testing gRPC APIs
    └── billing-service/
```

---

## 🔌 API Endpoints

### Auth Service

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/login` | Authenticate with email & password, returns JWT |
| `GET` | `/validate` | Validate a JWT token (via `Authorization: Bearer <token>` header) |

**Default test credentials:**
```
Email:    testuser@test.com
Password: password123
```

### Patient Service

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/patients` | List all patients |
| `POST` | `/patients` | Create a new patient |
| `PUT` | `/patients/{id}` | Update an existing patient |
| `DELETE` | `/patients/{id}` | Delete a patient |

**Example — Create Patient:**
```json
POST /patients
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main Street",
  "dateOfBirth": "1995-09-09",
  "registeredDate": "2024-11-28"
}
```

### Billing Service (gRPC)

| RPC | Method | Description |
|---|---|---|
| `BillingService` | `CreateBillingAccount` | Creates a billing account for a patient |

**gRPC endpoint:** `localhost:9001`

---

## 🚀 Running Locally with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- Ports `4000–4005`, `5001`, `9001`, `9092`, `9094` available

---

### Step 1 — Create a Docker Network

All services communicate on a shared Docker network called `internal`:

```bash
docker network create internal
```

---

### Step 2 — Start PostgreSQL Containers

The **Patient Service** and **Auth Service** each require their own PostgreSQL instance.

#### PostgreSQL for Patient Service

```bash
docker run -d \
  --name patient-service-db \
  --network internal \
  -e POSTGRES_USER=admin_user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=db \
  postgres:17
```

> [!NOTE]
> No host port is mapped for `patient-service-db` — it is only accessible from within the `internal` Docker network. If you need to connect from your host (e.g., via a DB client), add `-p 5432:5432`.

#### PostgreSQL for Auth Service

```bash
docker run -d \
  --name auth-service-db \
  --network internal \
  -e POSTGRES_USER=admin_user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=db \
  -v $(pwd)/../auth-service-db:/var/lib/postgresql/data \
  -p 5001:5432 \
  postgres:17
```

---

### Step 3 — Start Apache Kafka (KRaft Mode)

Kafka is used for async event streaming between Patient Service and Analytics Service. This project uses the official **Apache Kafka** image in **KRaft mode** (no Zookeeper required).

```bash
docker run -d \
  --name kafka \
  --network internal \
  -e KAFKA_NODE_ID=0 \
  -e KAFKA_PROCESS_ROLES=controller,broker \
  -e KAFKA_CLUSTER_ID=test-cluster-1 \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,EXTERNAL://localhost:9094 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=0@kafka:9093 \
  -p 9092:9092 \
  -p 9094:9094 \
  apache/kafka:latest
```

---

### Step 4 — Build & Run the Application Services

Build each service Docker image from the project root:

```bash
# Build all service images
docker build -t billing-service:latest  ./billing-service
docker build -t patient-service:latest  ./patient-service
docker build -t auth-service:latest     ./auth-service
docker build -t analytics-service:latest ./analytics-service
docker build -t api-gateway:latest      ./api-gateway
```

Run each service on the `internal` network, passing the required environment variables:

#### Billing Service

```bash
docker run -d \
  --name billing-service \
  --network internal \
  -p 4001:4001 \
  -p 9001:9001 \
  billing-service:latest
```

#### Patient Service

```bash
docker run -d \
  --name patient-service \
  --network internal \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://patient-service-db:5432/db \
  -e SPRING_DATASOURCE_USERNAME=admin_user \
  -e SPRING_DATASOURCE_PASSWORD=password \
  -e SPRING_JPA_HIBERNATE_DDL_AUTO=update \
  -e SPRING_SQL_INIT_MODE=always \
  -e SPRING_KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
  -e BILLING_SERVICE_ADDRESS=billing-service \
  -e BILLING_SERVICE_GRPC_PORT=9001 \
  patient-service:latest
```

#### Auth Service

```bash
docker run -d \
  --name auth-service \
  --network internal \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://auth-service-db:5432/db \
  -e SPRING_DATASOURCE_USERNAME=admin_user \
  -e SPRING_DATASOURCE_PASSWORD=password \
  -e SPRING_JPA_HIBERNATE_DDL_AUTO=update \
  -e SPRING_SQL_INIT_MODE=always \
  -e JWT_SECRET=IImy3y2vJQpr/+lgD5xf7N+pwkoffvpkEvXCfEv0Q0I= \
  auth-service:latest
```

> [!CAUTION]
> The `JWT_SECRET` value above is for **local development only**. Never commit production secrets to version control. Use a secrets manager or environment-specific configuration in production.

#### Analytics Service

```bash
docker run -d \
  --name analytics-service \
  --network internal \
  -e SPRING_KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
  -p 4002:4002 \
  analytics-service:latest
```

#### API Gateway

```bash
docker run -d \
  --name api-gateway \
  --network internal \
  -e AUTH_SERVICE_URL=http://auth-service:4005 \
  -p 4004:4004 \
  api-gateway:latest
```

---

### Step 5 — Verify Everything is Running

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

You should see **8 containers** running:

| Container | Role |
|---|---|
| `patient-service-db` | PostgreSQL for Patient Service |
| `auth-service-db` | PostgreSQL for Auth Service |
| `kafka` | Apache Kafka (KRaft mode) |
| `billing-service` | gRPC Billing Service |
| `patient-service` | Patient CRUD Service |
| `auth-service` | Authentication Service |
| `analytics-service` | Kafka Consumer Service |
| `api-gateway` | Spring Cloud API Gateway |

---

## 🧪 Testing the APIs

### Via API Gateway (Recommended)

All requests through the gateway go via `http://localhost:4004`.

**1. Login to get a JWT:**
```bash
curl -X POST http://localhost:4004/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@test.com", "password": "password123"}'
```

**2. Use the token to access Patient Service:**
```bash
curl http://localhost:4004/api/patients \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Swagger UI (Direct Access)

- **Patient Service:** [http://localhost:4000/swagger-ui.html](http://localhost:4000/swagger-ui.html)
- **Auth Service:** [http://localhost:4005/swagger-ui.html](http://localhost:4005/swagger-ui.html)

### IntelliJ HTTP Client

Pre-made `.http` request files are available in:
- `api-requests/auth-service/` — login & token validation
- `api-requests/patient-service/` — CRUD operations
- `grpc-requests/billing-service/` — gRPC billing account creation

---

## 🧹 Cleanup

Stop and remove all containers and the network:

```bash
docker stop api-gateway analytics-service auth-service patient-service billing-service kafka auth-service-db patient-service-db
docker rm api-gateway analytics-service auth-service patient-service billing-service kafka auth-service-db patient-service-db
docker network rm internal
```

---

## 🗺 Roadmap

- [ ] Docker Compose file for one-command setup
- [ ] Service discovery (Eureka / Consul)
- [ ] Centralized configuration (Spring Cloud Config)
- [ ] Distributed tracing (Zipkin / Jaeger)
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment manifests
- [ ] Frontend application

---

## 📄 License

This project is for educational / portfolio purposes.

---

