# Quote0 Client Python SDK

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![CI](https://github.com/YetYeti/quote0-client/workflows/CI/badge.svg)
![PyPI version](https://badge.fury.io/py/quote0-client.svg)

用于通过 Dot. App API 控制 Quote0 电子墨水设备的 Python SDK。

## 功能特性

- 完整覆盖 Quote0 的全部 6 个 API 端点
- 基于 Pydantic v2 模型的类型安全
- 全面的错误处理
- 支持文本和图像内容
- 设备任务管理
- 易于使用的同步客户端

## 安装

```bash
# 使用 pip
pip install quote0-client

# 使用 uv
uv add quote0-client
```

## 快速开始

```python
from quote0_client.client import Quote0Client
from quote0_client.models import TextContentRequest

# 初始化客户端
client = Quote0Client(api_key="your-api-key-from-dot-app")

# 获取设备列表
devices = client.get_devices()
print(f"找到 {len(devices)} 个设备")

# 发送文本内容
text_req = TextContentRequest(
    title="你好",
    message="Quote0 设备！"
)
response = client.send_text(devices[0].id, text_req)
if response.success:
    print("文本发送成功！")
```

## API 参考

| 方法 | 说明 | 参数 | 返回类型 |
|------|------|------|----------|
| `get_devices()` | 获取所有设备列表 | 无 | `List[Device]` |
| `get_device_status(device_id)` | 获取设备状态 | `device_id`: 设备序列号 | `DeviceStatus` |
| `switch_to_next(device_id)` | 切换到下一个内容 | `device_id`: 设备序列号 | `APIResponse` |
| `list_tasks(device_id, task_type)` | 列出设备任务 | `device_id`: 设备序列号, `task_type`: 任务类型 | `List[Task]` |
| `send_text(device_id, content)` | 发送文本内容 | `device_id`: 设备序列号, `content`: TextContentRequest | `APIResponse` |
| `send_image(device_id, content)` | 发送图像内容 | `device_id`: 设备序列号, `content`: ImageContentRequest | `APIResponse` |

### 数据模型

- `Device`: 设备信息（series, model, edition, id）
- `DeviceStatus`: 设备状态（电池、WiFi、渲染信息等）
- `TextContentRequest`: 文本内容（title, message, signature）
- `ImageContentRequest`: 图像内容（base64编码图片, border, ditherType）
- `APIResponse`: 通用响应包装器（success, message, data）

## 错误处理

所有 SDK 方法都可能抛出以下异常：

- `Quote0Error` - 基础异常类
- `AuthenticationError` - API 密钥无效或已过期（HTTP 401）
- `NotFoundError` - 设备未找到（HTTP 404）
- `PermissionError` - 权限不足（HTTP 403）
- `ValidationError` - 参数无效（HTTP 400）
- `RateLimitError` - 超过速率限制（10 次/秒）

```python
from quote0_client.exceptions import AuthenticationError, NotFoundError

try:
    devices = client.get_devices()
except AuthenticationError:
    print("API 密钥无效！")
except NotFoundError:
    print("设备未找到！")
except Quote0Error as e:
    print(f"错误: {e}")
```

## 配置

### 获取 API 密钥
1. 打开 Dot. App
2. 进入"更多"标签页
3. 点击"API Key"
4. 创建并保存密钥

### 获取设备序列号
1. 打开 Dot. App
2. 进入设备详情
3. 复制序列号（如 "ABCD1234ABCD"）

### 自定义 API 端点
```python
client = Quote0Client(
    api_key="your-api-key",
    base_url="https://your-custom-endpoint.com"
)
```

## 使用示例

### 上下文管理器模式

```python
from quote0_client.client import Quote0Client

with Quote0Client(api_key="your-api-key") as client:
    devices = client.get_devices()
    print(f"找到 {len(devices)} 个设备")

# 退出上下文时客户端会自动关闭
```

### 发送图像

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

image_req = ImageContentRequest(
    image=image_data,
    border=0,
    refreshNow=True
)
response = client.send_image("ABCD1234ABCD", image_req)
```

## 故障排除

- **ModuleNotFoundError** - 使用 `pip install -e .` 安装包
- **AuthenticationError** - 检查 API 密钥是否有效且未过期
- **NotFoundError** - 确认设备 ID 正确且已在 Dot. App 中注册
- **RateLimitError** - API 限制为 10 次/秒，添加退避机制
- **ValidationError** - 检查设备 ID 格式和 base64 编码

启用调试日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```



## 许可证

MIT License

## 贡献

欢迎贡献！请提交 pull request 或 issue。

## 相关链接

- [Quote0 官方文档](https://dot.mindreset.tech/docs/service/open)
- [Dot. App](https://dot.mindreset.tech/app)

