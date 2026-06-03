"""
Demo 6: QElidingLabel - 省略号标签

本 demo 展示 superqt 的 QElidingLabel 控件：
- 文本过长时自动截断并显示省略号
- 支持不同的省略模式（左、中、右）
- 应用场景：文件路径显示、长标题展示、列表项

QElidingLabel 是 QLabel 的增强版，当文本超出控件宽度时，
会自动在适当位置添加省略号 (...)。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QHBoxLayout,
)
from superqt import QElidingLabel


class ElidingLabelDemo(QWidget):
    """QElidingLabel 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 6: QElidingLabel")
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(
            QLabel(
                "<h2>QElidingLabel - 自动省略长文本</h2>"
                "<p>尝试调整窗口大小，观察文本截断效果</p>"
            )
        )

        long_text = "/Users/user/Documents/Projects/superqt-tutorial/examples/demo_files/very_long_filename.py"
        long_sentence = (
            "这是一段很长的中文句子，用于演示当文本超出控件宽度时，"
            "QElidingLabel 会自动截断并添加省略号来保持界面美观。"
        )

        # 1. 右侧省略（默认）
        group1 = QGroupBox("1. 右侧省略 (ElideRight) - 默认模式")
        layout1 = QVBoxLayout()
        label1 = QElidingLabel(long_text)
        layout1.addWidget(label1)

        label1b = QElidingLabel(long_sentence)
        label1b.setWordWrap(False)  # 不换行才能看到省略效果
        layout1.addWidget(label1b)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 中间省略
        group2 = QGroupBox("2. 中间省略 (ElideMiddle)")
        layout2 = QVBoxLayout()
        label2 = QElidingLabel(long_text)
        label2.setElideMode(Qt.TextElideMode.ElideMiddle)
        layout2.addWidget(label2)

        label2b = QElidingLabel(long_sentence)
        label2b.setElideMode(Qt.TextElideMode.ElideMiddle)
        label2b.setWordWrap(False)
        layout2.addWidget(label2b)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 左侧省略
        group3 = QGroupBox("3. 左侧省略 (ElideLeft)")
        layout3 = QVBoxLayout()
        label3 = QElidingLabel(long_text)
        label3.setElideMode(Qt.TextElideMode.ElideLeft)
        layout3.addWidget(label3)

        label3b = QElidingLabel(long_sentence)
        label3b.setElideMode(Qt.TextElideMode.ElideLeft)
        label3b.setWordWrap(False)
        layout3.addWidget(label3b)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 4. 对比普通 QLabel
        group4 = QGroupBox("4. 普通 QLabel (对比)")
        layout4 = QVBoxLayout()
        normal_label = QLabel(long_text)
        layout4.addWidget(normal_label)
        group4.setLayout(layout4)
        layout.addWidget(group4)

        layout.addStretch()


if __name__ == "__main__":
    app = QApplication([])
    window = ElidingLabelDemo()
    window.show()
    app.exec()
