"""
Demo 1: Hello World - 第一个 PySide6 + superqt 程序

本 demo 展示了：
- PySide6 的基本窗口创建流程
- 使用 superqt 的 QElidingLabel 显示文本
- 信号与槽的基本连接

学习目标：
- 理解 QApplication, QWidget 的基本概念
- 掌握窗口创建的最小代码模板
"""

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from superqt import QElidingLabel

class HelloWorldWindow(QWidget):
    """一个简单的问候窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 1: Hello World")
        self.resize(400, 200)

        # 创建布局
        layout = QVBoxLayout(self)

        # 使用 superqt 的 QElidingLabel（支持文本截断省略号）
        self.label = QElidingLabel("点击按钮查看问候语")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # 创建按钮
        self.button = QPushButton("点击我")
        self.button.clicked.connect(self.say_hello)
        layout.addWidget(self.button)

        self.click_count = 0

    def say_hello(self):
        """按钮点击时的处理函数"""
        self.click_count += 1
        messages = [
            "Hello, World! 👋",
            "你好，世界！🌍",
            "こんにちは世界！🇯🇵",
            "Bonjour le monde! 🇫🇷",
            "Hola Mundo! 🇪🇸",
        ]
        msg = messages[self.click_count % len(messages)]
        self.label.setText(f"第 {self.click_count} 次点击: {msg}")


if __name__ == "__main__":
    app = QApplication([])
    window = HelloWorldWindow()
    window.show()
    app.exec()
