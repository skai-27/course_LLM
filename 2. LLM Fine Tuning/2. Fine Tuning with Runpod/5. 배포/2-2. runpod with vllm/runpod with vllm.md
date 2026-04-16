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
### [단계 1: Template 생성](https://console.runpod.io/user/templates)
![alt text](image-5.png)

---
> Name, Public template 등 

![bg right w:600](image-6.png)

---
> Container image 등 

![bg right w:600](image-7.png)

---
> (옵션) 환경변수 등록 

![alt text](image-8.png)

---
> 결과 확인 

![alt text](image-9.png)

---
### [단계 2: Serverless 생성](https://console.runpod.io/serverless)
![alt text](image-10.png)

---
> Choose a template

![alt text](image-11.png)

---
> Configure endpoint

![alt text](image-12.png)

---
> Create endpoint

![alt text](image-13.png)

---
### [단계 3: Active Workers 적용](https://console.runpod.io/serverless)
![alt text](image-14.png)

---
> Active Workers

![bg right w:600](image-15.png)

---
> Save Endpoint

![bg right w:600](image-16.png)

---
> 적용 확인 

![bg right w:600](image-17.png)

---
### 단계 4: 테스트 
![alt text](image-18.png)

---




