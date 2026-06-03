# PySide6 + superqt 学习教程

> 由浅入深学习 PySide6 控件与 superqt 扩展组件的使用

---

## 目录

- [简介](#简介)
- [环境配置](#环境配置)
- [教程目录](#教程目录)
- [基础篇](#基础篇)
- [控件篇](#控件篇)
- [进阶篇](#进阶篇)
- [综合篇](#综合篇)
- [参考资料](#参考资料)

---

## 简介

**PySide6** 是 Qt 官方的 Python 绑定，提供了完整的 Qt6 框架访问能力。

**superqt** 是一个社区驱动的 PySide/PyQt 扩展库，提供了 Qt 原生模块中"缺失"的高质量控件和工具组件。

本教程通过 14 个由浅入深的 demo，帮助你快速掌握 PySide6 基础以及 superqt 的核心控件。

---

## 环境配置

本项目使用 `uv` 管理 Python 环境。

```bash
# 安装依赖
uv sync

# 或直接使用
uv run python demo/01_hello_world.py
```

---

## 教程目录

| 序号 | Demo | 文件 | 知识点 |
|------|------|------|--------|
| 1 | Hello World | `demo/01_hello_world.py` | PySide6 基础，QElidingLabel |
| 2 | QLabeledSlider | `demo/02_labeled_slider.py` | 带标签的滑块 |
| 3 | QRangeSlider | `demo/03_range_slider.py` | 范围滑块，双滑块选择 |
| 4 | QEnumComboBox | `demo/04_enum_combo_box.py` | 枚举下拉框，类型安全 |
| 5 | QCollapsible | `demo/05_collapsible.py` | 可折叠面板，动画效果 |
| 6 | QElidingLabel | `demo/06_eliding_label.py` | 省略号标签，文本截断 |
| 7 | QToggleSwitch | `demo/07_toggle_switch.py` | 现代开关控件 |
| 8 | QSearchableComboBox | `demo/08_searchable_combo_box.py` | 可搜索下拉框 |
| 9 | QDoubleSlider | `demo/09_double_slider.py` | 浮点数滑块 |
| 10 | Thread Worker | `demo/10_threading.py` | 线程装饰器，后台任务 |
| 11 | Searchable List | `demo/11_searchable_list.py` | 可搜索列表和树形控件 |
| 12 | 综合示例 | `demo/12_comprehensive_demo.py` | 多控件组合实战 |
| 13 | Ensure Main Thread | `demo/13_ensure_main_thread.py` | 确保主线程更新 UI |
| 14 | Signals Blocked | `demo/14_signals_blocked.py` | 防止信号级联触发，状态同步 |

---

## 基础篇

### Demo 1: Hello World

第一个 PySide6 程序，展示了：
- 创建 QApplication 和 QWidget
- 使用 QVBoxLayout 布局
- 信号与槽的连接
- superqt 的 QElidingLabel 基本用法

```python
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from superqt import QElidingLabel

app = QApplication([])
window = QWidget()
layout = QVBoxLayout(window)

label = QElidingLabel("Hello, superqt!")
layout.addWidget(label)

window.show()
app.exec()
```

---

## 控件篇

### Demo 2: QLabeledSlider

`QLabeledSlider` 是 `QSlider` 的增强版，在滑块旁边显示可编辑的数值标签。

**核心特性：**
- 拖动滑块或直接在 SpinBox 中输入数值
- 支持 `EdgeLabelMode` 控制标签位置
- 支持水平和垂直方向

```python
from superqt import QLabeledSlider

slider = QLabeledSlider(Qt.Orientation.Horizontal)
slider.setRange(0, 100)
slider.setValue(50)
```

### Demo 3: QRangeSlider

`QRangeSlider` 允许用户选择一个数值范围，有两个滑块手柄。

**应用场景：**
- 价格区间筛选
- 时间范围选择
- 图表缩放

```python
from superqt import QRangeSlider

slider = QRangeSlider(Qt.Orientation.Horizontal)
slider.setRange(0, 100)
slider.setValue((10, 90))  # (最小值, 最大值)
slider.valueChanged.connect(lambda v: print(f"范围: {v[0]} - {v[1]}"))
```

### Demo 4: QEnumComboBox

`QEnumComboBox` 基于 Python Enum 自动填充下拉选项。

**核心特性：**
- 类型安全的选择
- 自动从 Enum 填充选项
- `currentEnumChanged` 信号返回具体的 Enum 成员

```python
from enum import Enum
from superqt import QEnumComboBox

class Theme(Enum):
    Light = "浅色"
    Dark = "深色"

combo = QEnumComboBox()
combo.setEnumClass(Theme)
combo.currentEnumChanged.connect(lambda t: print(f"选择了: {t.name}"))
```

### Demo 5: QCollapsible

`QCollapsible` 是可折叠/展开的面板控件。

**核心特性：**
- 平滑的折叠动画
- 可以设置默认展开/折叠状态
- 通过 `setContent(widget)` 设置内容

```python
from superqt import QCollapsible

panel = QCollapsible("标题")
content = QWidget()
layout = QVBoxLayout(content)
layout.addWidget(QLabel("这是内容"))
panel.setContent(content)
panel.setCollapsed(True)  # 默认折叠
```

### Demo 6: QElidingLabel

`QElidingLabel` 是 `QLabel` 的增强版，文本过长时自动截断并显示省略号。

**省略模式：**
- `ElideRight`: 右侧省略（默认）
- `ElideMiddle`: 中间省略
- `ElideLeft`: 左侧省略

```python
from superqt import QElidingLabel

label = QElidingLabel("/very/long/path/to/file.py")
label.setElideMode(Qt.TextElideMode.ElideMiddle)  # 中间省略
```

### Demo 7: QToggleSwitch

`QToggleSwitch` 提供类似手机的开关控件。

```python
from superqt import QToggleSwitch

switch = QToggleSwitch(text="WiFi")
switch.setChecked(True)
switch.toggled.connect(lambda checked: print(f"Wifi: {'开' if checked else '关'}"))
```

### Demo 8: QSearchableComboBox

`QSearchableComboBox` 是可搜索的下拉框。

```python
from superqt import QSearchableComboBox

combo = QSearchableComboBox()
combo.addItems(["北京", "上海", "广州", "深圳"])
# 用户可以在输入框中打字搜索
```

### Demo 9: QDoubleSlider

`QDoubleSlider` 和 `QLabeledDoubleSlider` 支持浮点数精度。

```python
from superqt import QDoubleSlider, QLabeledDoubleSlider

slider = QDoubleSlider(Qt.Orientation.Horizontal)
slider.setRange(0.0, 1.0)
slider.setSingleStep(0.01)  # 步长 0.01
```

---

## 进阶篇

### Demo 10: Thread Worker

`@thread_worker` 装饰器让函数在后台线程执行，避免阻塞 GUI。

```python
from superqt.utils import thread_worker

@thread_worker
def long_running_task():
    for i in range(100):
        time.sleep(0.1)
    return "完成"

worker = long_running_task()
worker.returned.connect(on_finished)
```

### Demo 11: Searchable List & Tree

`QSearchableListWidget` 和 `QSearchableTreeWidget` 提供了带搜索框的列表和树形控件。

### Demo 13: @ensure_main_thread

`@ensure_main_thread` 装饰器确保被装饰的方法在 Qt 主线程执行，通常与 `@thread_worker` 配合使用。

**为什么需要它？**

Qt 规定所有 UI 操作必须在主线程执行。`@thread_worker` 让函数在后台线程运行，但如果需要在后台线程中更新 UI（比如显示进度、更新标签），就必须用 `@ensure_main_thread` 自动切换回主线程。

```python
from superqt.utils import thread_worker, ensure_main_thread

class MyWidget(QWidget):
    @ensure_main_thread
    def update_ui(self, text):
        """这个方法无论在哪个线程调用，都会在主线程执行"""
        self.label.setText(text)

    @thread_worker
    def background_task(self):
        """在后台线程运行"""
        for i in range(10):
            time.sleep(0.5)
            # 在后台线程调用 self.update_ui
            # @ensure_main_thread 自动将其切换到主线程
            self.update_ui(f"处理中... {i * 10}%")
        self.update_ui("完成!")

    def start(self):
        worker = self.background_task()
        worker.returned.connect(self.on_done)
```

**参数说明：**
- `await_return=False`: 是否等待结果返回再执行下一行
- `timeout=1000`: 等待结果的超时时间（毫秒）

### Demo 14: signals_blocked

`signals_blocked` 是信号工具，通过上下文管理器临时阻断对象发出的信号，解决多控件状态同步时的级联触发问题。

**典型问题：**
```python
# 问题：滑块和SpinBox双向绑定，导致无限循环
slider.valueChanged.connect(lambda v: spinbox.setValue(v))
spinbox.valueChanged.connect(lambda v: slider.setValue(v))  # 互相触发！
```

**使用 signals_blocked 解决：**
```python
from superqt.utils import signals_blocked

# 方法1：单个控件
slider.valueChanged.connect(lambda v: 
    spinbox.blockSignals(True) or spinbox.setValue(v) or spinbox.blockSignals(False)
)

# 方法2：优雅的方式
slider.valueChanged.connect(lambda v: _sync_spin(v))

def _sync_spin(v):
    with signals_blocked(spinbox):
        spinbox.setValue(v)

# 方法3：同时阻断多个控件
with signals_blocked(slider), signals_blocked(spinbox):
    slider.setValue(50)
    spinbox.setValue(50)
```

---

## 综合篇

### Demo 12: 综合控制面板

结合多个 superqt 控件，构建一个完整的参数控制面板：
- `QCollapsible` 分组
- `QEnumComboBox` 模式选择
- `QLabeledSlider` 参数调节
- `QRangeSlider` 范围设置
- `QToggleSwitch` 功能开关
- `QSearchableComboBox` 格式选择

---

## 参考资料

- [PySide6 官方文档](https://doc.qt.io/qtforpython-6/)
- [superqt 官方文档](https://pyapp-kit.github.io/superqt/)
- [superqt GitHub](https://github.com/pyapp-kit/superqt)
- [Qt 官方文档](https://doc.qt.io/)

---

> *Made with ❤️ by SOLO*
