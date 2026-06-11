"""
Demo 14: signals_blocked - 按钮状态同步

本 demo 展示 superqt 的 signals_blocked 工具：
- 临时阻断信号，防止程序化更新触发不必要的回调
- 同时阻断多个对象的信号
- 解决多控件状态同步时的级联触发问题

典型场景：
- 多个控件联动时，一个控件变化触发另一个，另一个又触发回来（无限循环）
- 程序化设置值时不希望触发信号
- 批量更新多个控件时，只希望触发一次最终事件
"""

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QTextEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from superqt.utils import signals_blocked


class SignalBlockedDemo(QWidget):
    """signals_blocked 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 14: signals_blocked - 按钮状态同步")
        self.resize(600, 650)

        layout = QVBoxLayout(self)

        # 添加说明
        layout.addWidget(
            QLabel(
                "<h2>signals_blocked - 状态同步利器</h2>"
                "<p>使用 superqt 的 signals_blocked 防止程序化更新触发级联信号</p>"
            )
        )

        # ===== 场景 1: 滑块与数字输入框同步 =====
        group1 = QGroupBox("1. 滑块与数字输入框同步")
        layout1 = QVBoxLayout()
        layout1.addWidget(
            QLabel("问题：滑块变化 → 更新SpinBox → 触发SpinBox变化 → 又更新滑块...")
        )

        self.slider_1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_1.setRange(0, 100)
        self.slider_1.setValue(50)
        layout1.addWidget(self.slider_1)

        self.spin_1 = QSpinBox()
        self.spin_1.setRange(0, 100)
        self.spin_1.setValue(50)
        layout1.addWidget(self.spin_1)

        self.slider_1.valueChanged.connect(self._on_slider_changed)
        self.spin_1.valueChanged.connect(self._on_spin_changed)
        group1.setLayout(layout1)
        layout.addWidget(group1)

        # ===== 场景 2: 多个控件联动同步 =====
        group2 = QGroupBox("2. 多控件状态同步")
        layout2 = QVBoxLayout()
        layout2.addWidget(
            QLabel("点击按钮同时更新滑块、Spin、CheckBox，但不触发级联信号")
        )

        self.sync_slider = QSlider(Qt.Orientation.Horizontal)
        self.sync_slider.setRange(0, 100)
        self.sync_slider.setValue(50)
        layout2.addWidget(self.sync_slider)

        self.sync_spin = QSpinBox()
        self.sync_spin.setRange(0, 100)
        self.sync_spin.setValue(50)
        layout2.addWidget(self.sync_spin)

        self.sync_check = QCheckBox("启用 (值 > 50 时自动勾选)")
        layout2.addWidget(self.sync_check)

        # 控件之间的联动
        self.sync_slider.valueChanged.connect(self._on_sync_slider)
        self.sync_spin.valueChanged.connect(self._on_sync_spin)

        # 同步按钮
        btn_layout = QHBoxLayout()
        btn_25 = QPushButton("设为 25")
        btn_25.clicked.connect(lambda: self.sync_set_value(25))
        btn_layout.addWidget(btn_25)

        btn_50 = QPushButton("设为 50")
        btn_50.clicked.connect(lambda: self.sync_set_value(50))
        btn_layout.addWidget(btn_50)

        btn_75 = QPushButton("设为 75")
        btn_75.clicked.connect(lambda: self.sync_set_value(75))
        btn_layout.addWidget(btn_75)

        btn_100 = QPushButton("设为 100")
        btn_100.clicked.connect(lambda: self.sync_set_value(100))
        btn_layout.addWidget(btn_100)
        layout2.addLayout(btn_layout)
        group2.setLayout(layout2)
        layout.addWidget(group2)

        # ===== 场景 3: 批量更新 vs 逐个更新 =====
        group3 = QGroupBox("3. 批量更新对比")
        layout3 = QVBoxLayout()
        layout3.addWidget(
            QLabel("对比使用 signals_blocked 批量更新与逐个更新的信号触发次数")
        )

        self.combo1 = QComboBox()
        self.combo1.addItems(["选项A", "选项B", "选项C", "选项D", "选项E"])
        layout3.addWidget(QLabel("下拉框1:"))
        layout3.addWidget(self.combo1)

        self.combo2 = QComboBox()
        self.combo2.addItems(["选项A", "选项B", "选项C", "选项D", "选项E"])
        layout3.addWidget(QLabel("下拉框2:"))
        layout3.addWidget(self.combo2)

        self.combo3 = QComboBox()
        self.combo3.addItems(["选项A", "选项B", "选项C", "选项D", "选项E"])
        layout3.addWidget(QLabel("下拉框3:"))
        layout3.addWidget(self.combo3)

        btn_layout2 = QHBoxLayout()
        btn_batch = QPushButton("批量更新 (使用 signals_blocked)")
        btn_batch.clicked.connect(self.batch_update)
        btn_layout2.addWidget(btn_batch)

        btn_normal = QPushButton("逐个更新 (不使用 signals_blocked)")
        btn_normal.clicked.connect(self.normal_update)
        btn_layout2.addWidget(btn_normal)
        layout3.addLayout(btn_layout2)
        group3.setLayout(layout3)
        layout.addWidget(group3)

        # 日志
        layout.addWidget(QLabel("信号触发日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        layout.addWidget(self.log_text)

        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(self.clear_btn)

    def log(self, message):
        """添加日志"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    # ===== 场景 1: 双向同步 =====

    def _on_slider_changed(self, value):
        """滑块变化时，同步到 SpinBox"""
        # 使用 signals_blocked 防止 SpinBox 变化信号又触发回来
        with signals_blocked(self.spin_1):
            self.spin_1.setValue(value)
        self.log(f"[场景1] 滑块 → {value}")

    def _on_spin_changed(self, value):
        """SpinBox 变化时，同步到滑块"""
        with signals_blocked(self.slider_1):
            self.slider_1.setValue(value)
        self.log(f"[场景1] SpinBox → {value}")

    # ===== 场景 2: 多控件同步 =====

    def _on_sync_slider(self, value):
        """同步滑块变化"""
        with signals_blocked(self.sync_spin):
            self.sync_spin.setValue(value)
        self.sync_check.setChecked(value > 50)
        self.log(f"[场景2] 滑块同步 → {value}")

    def _on_sync_spin(self, value):
        """同步 SpinBox 变化"""
        with signals_blocked(self.sync_slider):
            self.sync_slider.setValue(value)
        self.sync_check.setChecked(value > 50)
        self.log(f"[场景2] SpinBox同步 → {value}")

    def sync_set_value(self, value):
        """同步设置所有控件的值"""
        # 同时阻断所有控件的信号，一次性更新
        with signals_blocked(self.sync_slider), signals_blocked(self.sync_spin), signals_blocked(self.sync_check):
            self.sync_slider.setValue(value)
            self.sync_spin.setValue(value)
            self.sync_check.setChecked(value > 50)
        self.log(f"[场景2] 批量设为 {value}（无级联触发）")

    # ===== 场景 3: 批量更新对比 =====

    def batch_update(self):
        """使用 signals_blocked 批量更新（只触发一次事件）"""
        with signals_blocked(self.combo1), signals_blocked(self.combo2), signals_blocked(self.combo3):
            self.combo1.setCurrentIndex(2)
            self.combo2.setCurrentIndex(2)
            self.combo3.setCurrentIndex(2)
        self.log("[场景3] 批量更新: 3个控件同时设为索引2 (0次信号触发)")

    def normal_update(self):
        """逐个更新（会触发多次事件）"""
        self.combo1.setCurrentIndex(2)
        self.combo2.setCurrentIndex(2)
        self.combo3.setCurrentIndex(2)
        self.log("[场景3] 逐个更新: 3个控件依次设为索引2 (3次信号触发)")


if __name__ == "__main__":
    app = QApplication([])
    window = SignalBlockedDemo()
    window.show()
    app.exec()
