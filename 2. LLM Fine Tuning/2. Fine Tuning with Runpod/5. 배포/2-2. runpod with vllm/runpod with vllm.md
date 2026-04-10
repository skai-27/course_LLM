---
style: |
  img {
    display: block;
    float: none;
    margin-left: auto;
    margin-right: auto;
  }
marp: true
paginate: true
---
# Docker

---
### 단계1: Docker Server 실행 및 로그인 
![alt text](image.png)

---
### 단계2: Docker Image 생성
```bash
# 도커파일이 있는 폴더에서 실행 
docker build --platform linux/amd64 -t [YOUR_USERNAME]/runpod-vllm:latest .
```
![alt text](image-1.png)

---
![alt text](image-2.png)

---
### 단계3: Docker Hub 배포 
```shell
docker push [YOUR_USERNAME]/runpod-vllm:latest
```
![alt text](image-3.png)

---
![alt text](image-4.png)

---
# Runpod  

---
### 단계 1: 템플릿 생성








