<p align="center"><a href="README.md">English</a> | 中文</p>

# 浙江大学西报告厅 Extron 中控系统

> 平台：Extron IPCP Pro 350 + ControlScript Extension for VS Code

## 目录

- [项目概述](#项目概述)
- [系统架构](#系统架构)
- [硬件设备清单](#硬件设备清单)
- [网络拓扑](#网络拓扑)
- [目录结构](#目录结构)
- [核心模块说明](#核心模块说明)
  - [`main.py`](#mainpy)
  - [`devices.py`](#devicespy)
  - [`variables.py`](#variablespy)
  - [`control/av.py`](#controlavpy)
  - [`ui/tlp.py`](#uitlppy)
- [UI 界面说明](#ui-界面说明)
- [通信协议](#通信协议)
- [ThingsBoard 物联网集成](#thingsboard-物联网集成)
- [开关机时序](#开关机时序)
- [视频矩阵信号路由](#视频矩阵信号路由)
- [音频系统](#音频系统)
- [环境传感器](#环境传感器)
- [部署与调试](#部署与调试)

---

## 项目概述

本项目为浙江大学西报告厅 AV 集中控制系统，基于 Extron ControlScript 框架开发，运行于 IPCP Pro 350 控制器。系统集成了视频矩阵切换、音频处理、录制推流、追踪摄像头、LED 大屏、电视控制、环境传感器监测及 ThingsBoard 物联网状态上报等功能，并提供中英文双语触摸屏操作界面。

**主要功能：**

- 一键开关机时序控制（电源时序管理）
- 视频矩阵多路输入输出切换（5 路输入 × 6 路输出）
- TOT TIGER 音频处理器控制（音量、静音、输入选择）
- Extron SMP 351 录播系统控制（录制、推流）
- VISCA 协议追踪摄像头控制
- LED 屏继电器开关控制
- 三台电视电源控制（RS232/IR）
- 温湿度 / CO₂ 环境传感器数据采集
- ThingsBoard 平台物联网遥测数据上报

---

## 系统架构

```
触摸屏 (TLP Pro 1025M)
        │ 以太网
        ▼
IPCP Pro 350 ◄──────── IPL Pro S3
    │  │  │  │               │  │  │
  COM1 COM2 COM3 IRS1/IRS2 COM1 COM2 COM3
    │    │    │    │    │    │    │    │
视频  电源  录播  BYOD 电视3 电视1 电视2 音频
矩阵  时序  SMP351 切换器  (RS232)(RS232) 处理器
(RS232)(RS232)(RS232)(IR)(RS232)      (RS232/TOT)

以太网设备：
  ├── 环境传感器 (TCP 10.109.77.169:8002)
  ├── 追踪摄像头 (UDP 10.109.74.205:1259, VISCA)
  └── ThingsBoard (HTTP 10.105.5.170:8080)
```

---

## 硬件设备清单

| 设备名称 | 型号 | 连接方式 | IP / 端口 | 备注 |
|---------|------|---------|----------|------|
| 主控制器 | Extron IPCP Pro 350 | 以太网 | 10.109.74.169 | 别名 IPCP350 |
| 串口扩展器 | Extron IPL Pro S3 | 以太网 | 10.109.74.229 | 别名 IPLS3 |
| 触摸屏 | Extron TLP Pro 1025M | 以太网 | 10.109.74.232 | 别名 TLP1025M |
| 视频矩阵 | — | IPCP COM1, RS232 | — | 9600 8N1, 私有协议 |
| 电源时序器 | — | IPCP COM2, RS232 | — | 9600 8N1, Extron 协议 |
| 录播主机 | Extron SMP 351 | IPCP COM3, RS232 | — | 9600 8N1, Extron 协议 |
| BYOD 切换器 | Crestron | IPCP IRS1, IR | — | IR 控制（实用上等同于串口） |
| 电视 3 | 飞利浦 | IPCP IRS2, IR | — | IR 控制（实用上等同于串口），串口命令 |
| 电视 1 | 飞利浦 | IPL COM1, RS232 | — | 9600 8N1, 串口命令 |
| 电视 2 | 飞利浦 | IPL COM2, RS232 | — | 9600 8N1, 串口命令 |
| 音频处理器 | TOT TIGER | IPL COM3, RS232 | — | 9600 8N1, 私有协议 |
| LED 继电器 | — | IPCP RLY1 | — | 继电器控制 |
| 环境传感器 | — | 以太网 TCP | 10.109.77.169:8002 | Modbus-like 协议 |
| 追踪摄像头 | VISCA | 以太网 UDP | 10.109.74.205:1259 | VISCA 协议 |
| ThingsBoard | — | HTTP REST | 10.105.5.170:8080 | 物联网平台 |

---

## 网络拓扑

```
局域网 10.109.74.x / 10.109.77.x
│
├── 10.109.74.169   IPCP Pro 350 (主控制器)
├── 10.109.74.229   IPL Pro S3 (串口扩展器)
├── 10.109.74.232   TLP Pro 1025M (触摸屏)
├── 10.109.74.205   追踪摄像头 (UDP 1259)
└── 10.109.77.169   环境传感器 (TCP 8002)

物联网上报网络 10.105.x.x
└── 10.105.5.170    ThingsBoard 服务器 (HTTP 8080)
```

---

## 目录结构

```
ZU/
├── ZU.json                          # 项目配置（设备列表，版本 0.0.3）
├── ZU-certification.dat             # Extron 认证文件
├── ZU-credential.dat                # Extron 凭证文件
├── ir/                              # IR 红外驱动文件目录
├── sound/                           # 触摸屏按键音效目录
├── rfile/                           # UI 资源文件目录（图片等）
├── layout/
│   └── XBGT.gdl                     # TLP UI 布局定义文件
├── src/
│   ├── main.py                      # 入口，调用 system.Initialize()
│   ├── system.py                    # 核心逻辑：设备初始化、事件绑定
│   ├── devices.py                   # 所有设备实例化
│   ├── variables.py                 # 全局常量（矩阵映射、串口命令字节）
│   ├── control/
│   │   └── av.py                    # VideoMatrix + AudioProcessor 控制类
│   ├── ui/
│   │   └── tlp.py                   # 所有 Button/Slider/MESet UI 组件定义
│   └── modules/
│       ├── device/
│       │   ├── extr_sm_SMP_300_Series_v1_19_20_0.py   # 录播系统驱动
│       │   └── vsca_camera_Visca_v1_0_1_2.py           # VISCA 摄像头驱动
│       ├── helper/
│       │   └── ModuleSupport.py     # 辅助工具
│       └── project/
│           ├── thingsboard_power.py    # 电源状态 IoT 上报
│           ├── thingsboard_sensor.py   # 环境传感器数据 IoT 上报
│           ├── thingsboard_LED.py      # LED 状态 IoT 上报
│           ├── thingsboard_TV.py       # 电视状态 IoT 上报
│           └── martix.py              # 矩阵切换状态 IoT 上报
├── *.png                            # UI 截图（中文版界面）
```

---

## 核心模块说明

### `main.py`

程序入口，仅调用 `system.Initialize()` 启动整个系统。

### `devices.py`

集中实例化所有硬件接口：

```python
from extronlib.device import ProcessorDevice, UIDevice
from extronlib.interface import SerialInterface, EthernetClientInterface, RelayInterface

IPCP     = ProcessorDevice('IPCP350')
IPL      = ProcessorDevice('IPLS3')
TLP1025M = UIDevice('TLP1025M')

video_matrix    = SerialInterface(IPCP, 'COM1', 9600, 8, 'None', 1, 'Off', 0, 'RS232')
power_sequencer = SerialInterface(IPCP, 'COM2', ...)
recording_system = extr_sm_SMP_300_Series.SerialClass(IPCP, 'COM3', Model='SMP 351')
byod_switcher   = SerialInterface(IPCP, 'IRS1', ...)
tv_3            = SerialInterface(IPCP, 'IRS2', ...)
relay_led       = RelayInterface(IPCP, 'RLY1')

tv_1            = SerialInterface(IPL, 'COM1', ...)
tv_2            = SerialInterface(IPL, 'COM2', ...)
audio_processor = SerialInterface(IPL, 'COM3', ...)

sensor           = EthernetClientInterface("10.109.77.169", 8002)
tracking_camera  = vsca_camera.SerialOverEthernetClass("10.109.74.205", 1259, 'UDP')
```

### `variables.py`

定义所有硬件常量、信号名称映射以及串口命令字节串：

```python
# 矩阵信号名称
MATRIX_INPUT_BYOD    = 'BYOD'
MATRIX_INPUT_DOC     = 'DOC'
MATRIX_INPUT_CAMERA  = 'Camera'
MATRIX_INPUT_FLOOR   = 'Floor Socket'
MATRIX_INPUT_DESKTOP = 'Desktop'

MATRIX_OUTPUT_LED        = 'LED'
MATRIX_OUTPUT_RECORDER   = 'luobo'
MATRIX_OUTPUT_RETURN_TV  = 'Mirroring TV'
MATRIX_OUTPUT_LEFT_TV    = 'Left TV'
MATRIX_OUTPUT_RIGHT_TV   = 'Right TV'
MATRIX_OUTPUT_CAPTURE    = 'CAIji'

# 电源时序器命令
POWER_SEQUENCER_ON  = b'\x48\x1A\x00\x01\x02\x00\x00\x4D'
POWER_SEQUENCER_OFF = b'\x48\x1A\x00\x01\x01\x00\x00\x4D'

# 电视电源命令 (RS232)
TV_POWER_ON  = b'\x06\x01\x00\x18\x02\x1D'
TV_POWER_OFF = b'\x06\x01\x00\x18\x01\x1E'

# 环境传感器读取命令
ENVIRONMENTAL_SENSOR_READ = b'\x01\x03\x00\x00\x00\x08\x44\x0C'
```

### `control/av.py`

封装视频矩阵和音频处理器的操作：

```python
# 矩阵端口号映射
MATRIX_INPUT_NUMBERS = {
    'Camera': 7, 'Desktop': 9, 'DOC': 10, 'BYOD': 11, 'Floor Socket': 12
}
MATRIX_OUTPUT_NUMBERS = {
    'LED': 3, 'luobo': 4, 'Mirroring TV': 5,
    'Left TV': 6, 'Right TV': 7, 'CAIji': 8
}

class VideoMatrix:
    def route(self, input_name, output_name): ...  # 将输入切换到指定输出

class AudioProcessor:
    def set_volume(self, level): ...
    def set_mute(self, state): ...   # state: 'On' / 'Off' (字符串，非布尔值)
```

### `ui/tlp.py`

定义触摸屏上所有交互控件（Button、Slider、MESet），供 `system.py` 统一绑定事件处理。同时包含中英文按钮/MESet 双语映射字典（`BUTTON_ZH_TO_EN`、`BUTTON_EN_TO_ZH`、`MESET_ZH_TO_EN`、`MESET_EN_TO_ZH`），实现中英文界面按钮状态的自动同步。

---

## UI 界面说明

系统提供中英文双语界面。中文页面名称带 `_1` 后缀，英文版无后缀。

| 页面 | 截图 | 说明 |
|------|------|------|
| 启动页 | ![start](start_1.png) | 系统待机/欢迎页面 |
| 开机中 | ![Starting Up](Starting%20Up_1.png) | 开机时序执行中 |
| 确认开机 | ![Confirm Power On](Confirmation%20Power%20On_1.png) | 开机确认弹窗 |
| 主控页面 | ![Main](Main%20Multi-windows_1.png) | 多窗口主控界面 |
| 音频设置 | ![Audio](Audio%20Settings_1.png) | 音量/静音/输入选择 |
| 视频设置 | ![Video](Video%20Settings_1.png) | 矩阵切换/信号源选择 |
| 确认关机 | ![Confirm](Confirmation_1.png) | 关机确认弹窗 |
| 关机中 | ![Powering Down](Powering%20Down_1.png) | 关机时序执行中 |
| 帮助页面 | ![Help](Help_1.png) | 操作指南 |

---

## 通信协议

### 视频矩阵 (RS232)

- 接口：IPCP COM1, 9600 8N1
- 协议：私有串口协议，帧头 `0x7B 0x7B`，帧尾 `0x7D 0x7D`
- 功能：输入输出路由切换

### 音频处理器 TOT TIGER (RS232)

- 接口：IPL COM3, 9600 8N1
- 协议：TOT TIGER 私有串口协议，帧头 `0xA5 0xAB`
- 功能：音量控制、静音控制、输入选择

### 录播系统 SMP 351 (RS232)

- 接口：IPCP COM3, 9600 8N1
- 驱动：`extr_sm_SMP_300_Series_v1_19_20_0.py`
- 功能：录制启停、直播推流 (RTMP)

### 追踪摄像头 (UDP)

- 接口：以太网 UDP, 10.109.74.205:1259
- 协议：VISCA over Ethernet
- 驱动：`vsca_camera_Visca_v1_0_1_2.py`

### 环境传感器 (TCP)

- 接口：以太网 TCP, 10.109.77.169:8002
- 协议：Modbus-like, 请求帧 21 字节, 帧头 `0x01 0x03`
- 读取命令：`b'\x01\x03\x00\x00\x00\x08\x44\x0C'`
- 数据：温度、湿度、CO₂ 等环境参数

### 电视控制 (RS232)

- TV1: IPL COM1, TV2: IPL COM2, TV3: IPCP IRS2
- 开机：`b'\x06\x01\x00\x18\x02\x1D'`
- 关机：`b'\x06\x01\x00\x18\x01\x1E'`

---

## ThingsBoard 物联网集成

系统通过 HTTP REST API 将设备状态上报至 ThingsBoard 平台。

| 模块 | 文件 | 设备 Token | 上报内容 |
|------|------|-----------|---------|
| 电源状态 | `thingsboard_power.py` | `N61GJcet4ZAyOZ6BZheI` | 系统开关机状态 |
| 环境传感器 | `thingsboard_sensor.py` | hQdDFoalNZSwgj7lNrsT | 温度、湿度、CO₂ |
| LED 状态 | `thingsboard_LED.py` | 1PMwAXn0SgWPUhTxuDyz | LED 继电器状态 |
| 电视状态 | `thingsboard_TV.py` | IGeKi4fJVIuYaWbzlh2R | 电视电源状态 |
| 矩阵状态 | `martix.py` | `SlrUchlUCxC5qrq73FUj` | 当前信号路由 |

**服务器地址：**
- 内网域名：`things.intl.zju.edu.cn`
- 内网 IP：`10.105.5.170:8080`

**上报格式 (HTTP POST)：**
```http
POST /api/v1/{device_token}/telemetry
Content-Type: application/json
Authorization: Bearer {device_token}
{"key": "value"}
```

---

## 开关机时序

### 开机时序

1. 触摸屏显示"确认开机"弹窗
2. 用户确认后，进入"开机中"页面
3. 向 `power_sequencer` (COM2) 发送 `POWER_SEQUENCER_ON` 命令
4. 等待设备稳定
5. 初始化视频矩阵默认路由
6. 初始化音频处理器默认音量
7. 切换至主控界面
8. 通过 ThingsBoard 上报开机状态

### 关机时序

1. 触摸屏显示"确认关机"弹窗
2. 用户确认后，进入"关机中"页面
3. 停止录播系统（如正在录制）
4. 关闭所有电视
5. 向 `power_sequencer` (COM2) 发送 `POWER_SEQUENCER_OFF` 命令
6. 切换至待机页面
7. 通过 ThingsBoard 上报关机状态

---

## 视频矩阵信号路由

### 输入信号源

| 输入名称 | 矩阵端口 | 说明 |
|---------|---------|------|
| Camera | 7 | 追踪摄像头 |
| Desktop | 9 | 台式电脑 |
| DOC | 10 | 实物展台 |
| BYOD | 11 | 无线投屏 |
| Floor Socket | 12 | 地插 HDMI |

### 输出目标

| 输出名称 | 矩阵端口 | 说明 |
|---------|---------|------|
| LED | 3 | LED 大屏 |
| luobo | 4 | 录播主机 (SMP 351) 采集输入 |
| Mirroring TV | 5 | 返看电视 |
| Left TV | 6 | 左电视 |
| Right TV | 7 | 右电视 |
| CAIji | 8 | 采集卡 |

---

## 音频系统

音频处理器通过 IPL Pro S3 COM3 串口连接，使用 TOT TIGER 私有协议控制：

- **音量控制**：范围 0–100，对应 dB 值由处理器转换
- **静音控制**：通道级静音，调用时传字符串 `'On'` / `'Off'`
- **输入选择**：在不同音频源之间切换（麦克风、线路输入等）

---

## 环境传感器

传感器通过 TCP 连接，使用 Modbus-like 协议轮询数据：

```python
# 读取命令
READ_CMD = b'\x01\x03\x00\x00\x00\x08\x44\x0C'
# 返回 21 字节帧，包含：
# 温度 (°C)、相对湿度 (%)、CO₂ 浓度 (ppm) 等
```

采集到的数据周期性上报至 ThingsBoard 平台，可在仪表盘或监控界面查看。

![IOT](IOT.png)

---

## 部署与调试

### 环境要求

- Extron ControlScript (extronlib) 运行于 IPCP Pro 350
- Python 语法兼容 ControlScript 解释器 (Python=3.5)
- 设备需在同一局域网子网内 (10.109.74.x / 10.109.77.x)

### 部署步骤

1. 使用 `ControlScript Deployment Utility` 将 `src/` 目录下所有文件上传至 IPCP Pro 350
2. 将 `layout/XBGT.gdl` 上传至 TLP Pro 1025M
3. 确认串口波特率与 `devices.py` 中配置一致
4. 验证网络设备 IP 地址可达
5. 在 IPCP 控制台中运行 `main.py` 启动项目

### 常见问题排查

| 现象 | 可能原因 | 解决方案 |
|------|---------|---------|
| 音频静音命令无效 | `set_mute()` 传入了布尔值 | 改用字符串 `'On'` / `'Off'` |
| ThingsBoard 上报失败 | 网络不可达或 Token 错误 | 检查 `10.105.5.170:8080` 是否可达，Token 是否正确 |
| 音频初始化流程卡死 | `get_input_volume()` 调用过多导致命令拥塞 | 手动设置预设值，如 `SetFill(-10.2)` |
| 环境传感器无数据 | TCP 连接断开 | 检查 `10.109.77.169:8002` 连通性 |
