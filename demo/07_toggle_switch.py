"""
Demo 7: QToggleSwitch - 现代开关控件

本 demo 展示 superqt 的 QToggleSwitch 控件：
- 现代化的开关控件，替代传统 QCheckBox
- 支持文本标签
- 应用场景：设置开关、功能启用/禁用

QToggleSwitch 提供类似手机上的开关控件，比传统的 QCheckBox 更现代美观。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QTextEdit,
)
from superqt import QToggleSwitch


class ToggleSwitchDemo(QWidget):
    """QToggleSwitch 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 7: QToggleSwitch")
        self.resize(450, 550)

        layout = QVBoxLayout(self)

        # 添加标题
        layout.addWidget(QLabel("<h2>QToggleSwitch - 现代开关控件</h2>"))

        # 1. 基本开关
        group1 = QGroupBox("1. 基本开关")
        layout1 = QVBoxLayout()
        self.switch1 = QToggleSwitch()
        self.switch1.toggled.connect(lambda checked: self.on_toggle("开关1", checked))
        layout1.addWidget(self.switch1)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 带文本标签的开关
        group2 = QGroupBox("2. 带文本标签")
        layout2 = QVBoxLayout()

        wifi_switch = QToggleSwitch(text="WiFi")
        wifi_switch.setChecked(True)
        layout2.addWidget(wifi_switch)

        bluetooth_switch = QToggleSwitch(text="蓝牙")
        layout2.addWidget(bluetooth_switch)

        location_switch = QToggleSwitch(text="定位服务")
        layout2.addWidget(location_switch)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 设置面板示例
        group3 = QGroupBox("3. 应用设置")
        layout3 = QVBoxLayout()

        dark_mode = QToggleSwitch(text="深色模式")
        dark_mode.toggled.connect(
            lambda checked: self.on_toggle("深色模式", checked)
        )
        layout3.addWidget(dark_mode)

        notifications = QToggleSwitch(text="通知推送")
        notifications.setChecked(True)
        notifications.toggled.connect(
            lambda checked: self.on_toggle("通知推送", checked)
        )
        layout3.addWidget(notifications)

        auto_update = QToggleSwitch(text="自动更新")
        auto_update.setChecked(True)
        auto_update.toggled.connect(
            lambda checked: self.on_toggle("自动更新", checked)
        )
        layout3.addWidget(auto_update)

        analytics = QToggleSwitch(text="使用统计收集")
        analytics.toggled.connect(
            lambda checked: self.on_toggle("使用统计", checked)
        )
        layout3.addWidget(analytics)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        layout.addWidget(QLabel("\n操作日志:"))
        layout.addWidget(self.status_text)

    def on_toggle(self, name, checked):
        """处理开关切换"""
        status = "开启" if checked else "关闭"
        msg = f"{name}: {status}"
        current = self.status_text.toPlainText()
        self.status_text.setText(current + msg + "\n")
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )


if __name__ == "__main__":
    app = QApplication([])
    window = ToggleSwitchDemo()
    window.show()
    app.exec()
