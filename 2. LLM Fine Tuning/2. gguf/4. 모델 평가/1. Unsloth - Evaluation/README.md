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
# Docker Hub에 배포하는 명령어
> Docker Image 생성
```shell
docker build -t <Docker ID>/unsloth-deepeval-runpod:3.7.6 .
```

> Docker Container 실행 
```shell
# CPU용
docker run -it --rm -p 8080:8080 -v ./workspace:/workspace <Docker ID>/unsloth-deepeval-runpod:3.7.6
```

> Docker Hub 배포 
```shell
docker push <Docker ID>/unsloth-deepeval-runpod:3.7.6
```
