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
### 단계1: Docker Image 생성
```shell
docker build -t <Docker ID>/evaluation-deepeval-runpod:3.7.6 .
```
![alt text](image.png)

---
> 결과확인

![alt text](image-1.png)

---
### 단계2: Docker Container 실행 
```shell
# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace <Docker ID>/evaluation-deepeval-runpod:3.7.6
```
![alt text](image-2.png)

---
> [결과확인](http://localhost:8080/?folder=/workspace)

![alt text](image-3.png)

---
### 단계3: Docker Hub 배포 
```shell
docker push <Docker ID>/evaluation-deepeval-runpod:3.7.6
```
![alt text](image-4.png)

---
> 결과확인

![alt text](image-5.png)

---
# Runpod

---
![alt text](image-6.png)

---
![alt text](image-7.png)

---
![alt text](image-8.png)

---
![alt text](image-9.png)

---
![alt text](image-10.png)

---
![alt text](image-11.png)


