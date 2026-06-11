"""
Demo 13: @ensure_main_thread - 确保在主线程执行

本 demo 展示 superqt 的 ensure_main_thread 装饰器：
- 确保被装饰的函数在 Qt 主线程执行
- 通常与 @thread_worker 配合使用
- 应用场景：后台任务完成后更新 UI

在 Qt 中，所有 UI 操作必须在主线程执行。
@ensure_main_thread 让你可以在后台线程中安全地调用 UI 更新方法。
"""

import time
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QProgressBar,
)
from superqt.utils import thread_worker, ensure_main_thread


class EnsureMainThreadDemo(QWidget):
    """@ensure_main_thread 演示"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo 13: @ensure_main_thread")
        self.resize(500, 450)

        layout = QVBoxLayout(self)

        # 说明
        layout.addWidget(
            QLabel(
                "<h2>@ensure_main_thread - 确保主线程执行</h2>"
                "<p>对比：直接在后台线程更新 UI vs 使用装饰器切换回主线程</p>"
            )
        )

        # 进度条
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        # 结果标签（UI 组件）
        self.result_label = QLabel("等待结果...")
        layout.addWidget(self.result_label)

        # 按钮
        btn_layout = QHBoxLayout()

        self.correct_btn = QPushButton("正确方式 (ensure_main_thread)")
        self.correct_btn.clicked.connect(self.run_correct)
        btn_layout.addWidget(self.correct_btn)

        self.wrong_btn = QPushButton("错误方式 (直接更新 UI)")
        self.wrong_btn.clicked.connect(self.run_wrong)
        btn_layout.addWidget(self.wrong_btn)

        layout.addLayout(btn_layout)

        # 日志
        layout.addWidget(QLabel("日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        layout.addWidget(self.log_text)

    # @ensure_main_thread
    def log(self, message):
        """添加日志"""
        import threading
        thread_name = threading.current_thread().name
        self.log_text.append(f"[{thread_name}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    # ===== 关键：这个方法被 ensure_main_thread 装饰 =====
    # 即使在后台线程调用它，也会自动切换到主线程执行
    @ensure_main_thread
    def update_result_ui(self, value):
        """更新结果标签的 UI 方法"""
        self.result_label.setText(f"处理中... {value}%")
        self.progress.setValue(value)
        self.log(f"UI 已更新: {value}")

    @thread_worker
    def background_task_correct(self):
        """正确的后台任务 - 使用 @ensure_main_thread 更新 UI"""
        self.log("开始后台任务（正确方式）...")
        for i in range(1, 6):
            time.sleep(0.5)
            # 在后台线程调用 self.update_result_ui
            # @ensure_main_thread 会自动将其切换到主线程执行
            self.update_result_ui(i * 20)
        return "成功"

    @thread_worker
    def background_task_wrong(self):
        """错误的后台任务 - 直接在后台线程更新 UI"""
        self.log("开始后台任务（错误方式）...")
        for i in range(1, 6):
            time.sleep(0.5)
            # 直接在后台线程更新 UI - 这是不安全的！
            self.update_progress.emit(i * 20)

        return "完成（但 UI 更新不安全）"

    def run_correct(self):
        """运行正确的后台任务"""
        self.status_label.setText("正在执行...")
        self.result_label.setText("处理中...")
        self.progress.setValue(0)
        self.log("========== 正确方式 ==========")

        worker = self.background_task_correct()
        worker.returned.connect(self.on_task_done)
        worker.start()

    def run_wrong(self):
        """运行错误的后台任务"""
        self.status_label.setText("正在执行...")
        self.result_label.setText("处理中...")
        self.progress.setValue(0)
        self.log("========== 错误方式 ==========")

        worker = self.background_task_wrong()
        worker.returned.connect(self.on_task_done)
        worker.start()

    def on_task_done(self, result):
        """任务完成"""
        self.status_label.setText(f"完成: {result}")
        self.progress.setValue(100)
        if result == "成功":
            self.log("✅ 所有 UI 更新都在主线程完成")
        else:
            # 手动更新结果（因为后台任务没做）
            self.result_label.setText("处理完成（UI 更新可能不安全）⚠️")
            self.log("⚠️ UI 更新可能在后台线程执行，不安全")


if __name__ == "__main__":
    app = QApplication([])
    window = EnsureMainThreadDemo()
    window.show()
    app.exec()
