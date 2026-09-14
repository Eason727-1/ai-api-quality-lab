# AI API Quality Lab

[![tests](https://github.com/Eason727-1/ai-api-quality-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/Eason727-1/ai-api-quality-lab/actions/workflows/tests.yml)

一个面向 **软件测试开发 / AI 质量工程** 的小型作品集项目：用 FastAPI 构造 AI 回答质量评测接口，
再用 pytest 对接口契约、边界值、异常输入、中文内容与安全风险进行自动化验证。

项目不调用付费模型 API，评分结果可重复，适合本地演示和持续集成。

## 项目亮点

- API 自动化：覆盖状态码、响应结构、请求校验和链路追踪字段。
- 测试设计：使用等价类、边界值和参数化用例覆盖正常流与异常流。
- AI 质量规则：从关键词覆盖度、回答清晰度、安全性三个维度生成质量分数。
- 安全测试：识别系统提示词泄漏、API Key、脚本标签和自定义敏感词。
- 持续集成：GitHub Actions 自动运行测试，代码覆盖率门槛为 90%。

## 技术栈

`Python` · `FastAPI` · `Pydantic` · `pytest` · `HTTPX` · `GitHub Actions`

## 目录结构

```text
src/ai_quality_lab/   API、数据模型与质量规则
tests/                接口、边界、规则和安全测试
docs/test-plan.md     测试范围、方法与退出标准
.github/workflows/    CI 自动化配置
```

## 快速开始

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
pytest
uvicorn ai_quality_lab.app:app --reload
```

启动后可访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/health`

请求示例：

```json
{
  "question": "如何保证接口质量？",
  "answer": "通过边界测试、异常测试和持续回归保证接口质量。",
  "expected_keywords": ["边界测试", "异常测试", "持续回归"],
  "forbidden_phrases": ["内部机密"],
  "pass_threshold": 70
}
```

## 已覆盖的测试场景

- 健康检查与 OpenAPI 契约
- 中英文关键词匹配与去重
- `pass_threshold` 上下界及非法取值
- 空白输入、超长回答与字段缺失
- 部分命中、零关键词和评分范围不变量
- Prompt Injection、敏感信息泄漏与脚本标签
- 响应 Trace ID 一致性

详细方案见 [docs/test-plan.md](docs/test-plan.md)。

## 简历表述参考

> 设计并实现 AI 回答质量评测接口，基于关键词覆盖度、清晰度与安全规则构建可解释质量门禁；
> 使用 pytest 完成接口契约、边界值、异常流与风险文本的参数化测试，并通过 GitHub Actions 持续集成与 90% 覆盖率阈值保证回归质量。

