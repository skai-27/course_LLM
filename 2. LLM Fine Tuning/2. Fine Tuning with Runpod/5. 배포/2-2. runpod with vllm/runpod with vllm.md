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


---
### 단계2: Docker Image 생성
```bash
# 도커파일이 있는 폴더에서 실행 
docker build --platform linux/amd64 -t [YOUR_USERNAME]/runpod-vllm:latest .
```


---


---
### 단계3: Docker Hub 배포 
```shell
docker push [YOUR_USERNAME]/runpod-vllm:latest
```


---


---
# Runpod  

---
### [단계 1: Serverless Endpoint 생성](https://console.runpod.io/serverless)


---
### 단계2: Create a new deployment


---
> Container image


---
> Configure endpoint



---
> Create endpoint



---
### 단계3: Active Workers 적용 
> cold Start 문제 해결 



---
> Active Workers 설정 



---
> (옵션) Environment Variables 



---
### 단계4: 배포 확인


---
### 단계5: 테스트 


---


