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
# MCP Server
- MCP 서버는 LLM이 사용할 수 있는 도구와 데이터 액세스 기능을 제공하는 프로그램

![w:900](./img/image-10.png)

---
## Setup

---
### 단계1: 프로젝트 생성 
```shell
uv init <프로젝트명> 
cd <프로젝트명>
```
![alt text](./img/image-9.png)

---
### 단계2: 가상환경 생성  
```shell
uv venv .venv 
.venv/Scripts/activate
```
![alt text](./img/image-7.png)

---
### 단계3: 관련 라이브러리 추가 
```shell
uv add "mcp[cli]"
```
![alt text](./img/image-8.png)

---
## MCP Servier > main.py
```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

```

---
## Claude Desktop에 적용
- 사전작업 
  - [Claude Desktop 설치](https://claude.ai/download)

---
### 단계1: MCP Server 적용 
```shell
mcp install main.py
```
![alt text](./img/image-6.png)

---
![alt text](./img/image-4.png)

---
### 단계2: Claude Desktop의 config.json 확인 
![alt text](./img/image-2.png)

---
![alt text](./img/image-3.png)

---
![alt text](./img/image.png)

---
### 단계3: add 툴 사용하기 
![alt text](./img/image-5.png)

---
![alt text](./img/image-1.png)

---
# 참고문서
- https://github.com/modelcontextprotocol/python-sdk



