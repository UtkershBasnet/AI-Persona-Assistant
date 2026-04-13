
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