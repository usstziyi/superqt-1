"""
Demo 9: QDoubleSlider & QLabeledDoubleSlider - 浮点数滑块

本 demo 展示 superqt 的浮点数滑块控件：
- QDoubleSlider: 支持浮点数的滑块
- QLabeledDoubleSlider: 带标签的浮点数滑块
- 应用场景：音量控制、透明度调节、科学计算参数

PySide6 原生 QSlider 只支持整数，superqt 提供了浮点数滑块来满足精度需求。
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
)
from PySide6.QtCore import Qt
from superqt import QDoubleSlider, QLabeledDoubleSlider


class DoubleSliderDemo(QWidget):
    """浮点数滑块演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 9: QDoubleSlider")
        self.resize(500, 500)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(
            QLabel(
                "<h2>QDoubleSlider - 浮点数滑块</h2>"
                "<p>支持小数精度的滑块控件</p>"
            )
        )

        # 1. 基本浮点滑块
        group1 = QGroupBox("1. 基本浮点滑块 (0.0 - 10.0)")
        layout1 = QVBoxLayout()
        self.double_slider = QDoubleSlider(Qt.Orientation.Horizontal)
        self.double_slider.setRange(0.0, 10.0)
        self.double_slider.setValue(5.5)
        self.double_slider.valueChanged.connect(
            lambda v: self.on_value("滑块", v)
        )
        layout1.addWidget(self.double_slider)
        self.value_label1 = QLabel("当前值: 5.5")
        layout1.addWidget(self.value_label1)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # 2. 带标签的浮点滑块
        group2 = QGroupBox("2. 带标签的浮点滑块")
        layout2 = QVBoxLayout()
        self.labeled_double = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self.labeled_double.setRange(0.0, 1.0)
        self.labeled_double.setValue(0.5)
        layout2.addWidget(self.labeled_double)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # 3. 透明度控制 (0.0 - 1.0)
        group3 = QGroupBox("3. 透明度控制")
        layout3 = QVBoxLayout()
        self.opacity_slider = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0.0, 1.0)
        self.opacity_slider.setValue(1.0)
        self.opacity_slider.setSingleStep(0.05)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        layout3.addWidget(self.opacity_slider)

        # 演示用的颜色方块
        self.color_box = QLabel()
        self.color_box.setFixedHeight(50)
        self.color_box.setStyleSheet("background-color: rgb(65, 105, 225);")
        layout3.addWidget(self.color_box)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 4. 高精度科学参数
        group4 = QGroupBox("4. 科学计算参数 (高精度)")
        layout4 = QVBoxLayout()
        self.precision_slider = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self.precision_slider.setRange(0.000, 1.000)
        self.precision_slider.setValue(0.314)
        self.precision_slider.setSingleStep(0.001)
        self.precision_slider.setDecimals(3)
        layout4.addWidget(self.precision_slider)
        group4.setLayout(layout4)
        layout.addWidget(group4)

        layout.addStretch()

    def on_value(self, name, value):
        """处理数值变化"""
        self.value_label1.setText(f"当前值: {value:.2f}")

    def on_opacity_changed(self, value):
        """处理透明度变化"""
        self.color_box.setStyleSheet(
            f"background-color: rgba(65, 105, 225, {value:.2f});"
        )


if __name__ == "__main__":
    app = QApplication([])
    window = DoubleSliderDemo()
    window.show()
    app.exec()
