"""
Demo 5: QCollapsible - 可折叠面板

本 demo 展示 superqt 的 QCollapsible 控件：
- 可折叠/展开的面板
- 动画效果
- 应用场景：设置面板、手风琴式布局、FAQ 展示

QCollapsible 是一个可以折叠和展开的容器，点击标题栏即可切换显示状态。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QComboBox,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import Qt
from superqt import QCollapsible


class CollapsibleDemo(QWidget):
    """QCollapsible 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 5: QCollapsible")
        self.resize(500, 600)

        layout = QVBoxLayout(self)

        # 添加标题
        layout.addWidget(
            QLabel("<h2>可折叠面板示例</h2><p>点击标题栏展开/折叠内容</p>")
        )

        # 1. 外观设置
        self.appearance = QCollapsible("🎨 外观设置")
        appearance_layout = QVBoxLayout()
        appearance_layout.addWidget(QLabel("主题颜色:"))
        color_combo = QComboBox()
        color_combo.addItems(["蓝色", "绿色", "紫色", "橙色"])
        appearance_layout.addWidget(color_combo)

        appearance_layout.addWidget(QLabel("字体大小:"))
        font_slider = QSlider(Qt.Orientation.Horizontal)
        font_slider.setRange(10, 30)
        font_slider.setValue(14)
        appearance_layout.addWidget(font_slider)
        appearance_widget = QWidget()
        appearance_widget.setLayout(appearance_layout)
        self.appearance.setContent(appearance_widget)
        layout.addWidget(self.appearance)

        # 2. 通知设置
        self.notification = QCollapsible("🔔 通知设置")
        notification_layout = QVBoxLayout()
        email_check = QCheckBox("接收邮件通知")
        email_check.setChecked(True)
        notification_layout.addWidget(email_check)

        push_check = QCheckBox("接收推送通知")
        push_check.setChecked(True)
        notification_layout.addWidget(push_check)

        sms_check = QCheckBox("接收短信通知")
        notification_layout.addWidget(sms_check)
        notification_widget = QWidget()
        notification_widget.setLayout(notification_layout)
        self.notification.setContent(notification_widget)
        layout.addWidget(self.notification)

        # 3. 高级设置（默认折叠）
        self.advanced = QCollapsible("⚙️ 高级设置")
        self.advanced.setCollapsed(True)  # 默认折叠
        advanced_layout = QVBoxLayout()
        advanced_layout.addWidget(QLabel("API 密钥:"))
        advanced_layout.addWidget(QLabel("此处为敏感配置项..."))

        debug_btn = QPushButton("调试模式")
        debug_btn.setCheckable(True)
        advanced_layout.addWidget(debug_btn)
        advanced_widget = QWidget()
        advanced_widget.setLayout(advanced_layout)
        self.advanced.setContent(advanced_widget)
        layout.addWidget(self.advanced)

        # 4. 关于信息
        self.about = QCollapsible("ℹ️ 关于")
        about_layout = QVBoxLayout()
        about_layout.addWidget(
            QLabel(
                "本示例展示了 QCollapsible 的基本用法。\n"
                "它非常适合用于设置面板、帮助文档等需要折叠展示的场景。"
            )
        )
        about_widget = QWidget()
        about_widget.setLayout(about_layout)
        self.about.setContent(about_widget)
        layout.addWidget(self.about)

        layout.addStretch()


if __name__ == "__main__":
    app = QApplication([])
    window = CollapsibleDemo()
    window.show()
    app.exec()
