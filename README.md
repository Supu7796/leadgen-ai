# LeadGen AI（销售获客智能系统）

一个可被 Coze 调用的 Flask API 服务，支持：

- 公司域名查询潜在邮箱（Hunter API）
- 自动生成英文销售话术（长文案 + 短触达）
- 线索入库 MySQL（去重）
- 批量 JSON / CSV 导入处理

---

## 1. 架构分层

- API 层（`app/api/`）：
  - 路由定义、参数校验、REST 输出
- Service 层（`app/services/`）：
  - 业务编排（查重、调用 Hunter、生成话术、入库、批处理）
- 数据层（`app/models/`）：
  - SQLAlchemy ORM 模型（`Lead`、`QueryLog`）
- 外部 API 层（`app/external/`）：
  - Hunter API 封装、重试机制、空结果处理

数据流：

1. 请求进入 API 路由
2. 参数校验器验证输入
3. Service 层做 domain 归一化与查重
4. 未命中缓存则调用 Hunter API
5. 生成销售话术
6. 入库 leads + 记录 query_logs
7. 统一 JSON 返回

---

## 2. 项目结构

```text
leadgen-ai/
├─ app/
│  ├─ __init__.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ lead_routes.py
│  ├─ external/
│  │  └─ hunter_client.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ db.py
│  │  ├─ lead.py
│  │  └─ query_log.py
│  ├─ services/
│  │  ├─ lead_service.py
│  │  └─ pitch_service.py
│  └─ utils/
│     ├─ error_handlers.py
│     ├─ response.py
│     └─ validators.py
├─ sql/
│  └─ schema.sql
├─ .env.example
├─ requirements.txt
├─ run.py
└─ README.md
```

---

## 3. API 说明

### 3.1 单条查询

- `POST /api/lead/find`
- 请求体：

```json
{
  "company": "openai.com"
}
```

- 响应：

```json
{
  "success": true,
  "data": {
    "email": "contact@openai.com",
    "confidence": 0.95,
    "pitch": "...",
    "short_pitch": "..."
  }
}
```

### 3.2 批量导入

- `POST /api/lead/batch`
- 支持：
  - JSON 数组：`["openai.com", {"company":"example.com"}]`
  - CSV（`Content-Type: text/csv`，至少包含 `company` 列）

### 3.3 查询列表

- `GET /api/leads?page=1&page_size=20`

---

## 4. Windows 本地运行

1. 安装 Python 3.10+
2. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. 安装依赖：

```powershell
pip install -r requirements.txt
```

4. 配置环境变量：

```powershell
copy .env.example .env
```

5. 创建数据库并执行建表 SQL（`sql/schema.sql`）
6. 启动服务：

```powershell
python run.py
```

7. 健康检查：`GET http://127.0.0.1:5000/health`

---

## 5. Coze 调用方式（重点）

在 Coze 中创建 HTTP/API 类型插件，配置：

- Base URL：`http://<你的服务地址>:5000`
- 鉴权：如需可在网关层补充（当前示例未加 token）
- 接口定义：

1) 查找线索
- Method: `POST`
- Path: `/api/lead/find`
- Body(JSON):

```json
{
  "company": "{{company}}"
}
```

2) 批量导入
- Method: `POST`
- Path: `/api/lead/batch`
- Body(JSON):

```json
{{company_list_json}}
```

3) 查询列表
- Method: `GET`
- Path: `/api/leads?page={{page}}&page_size={{page_size}}`

建议在 Coze 工作流里串联：
1. 用户输入公司域名
2. 调用 `/api/lead/find`
3. 读取返回的 `email / confidence / pitch`
4. 自动进入后续触达节点
