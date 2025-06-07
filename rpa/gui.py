import sys
import logging

def main():
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QPushButton,
        QTextEdit, QVBoxLayout, QFileDialog, QHBoxLayout,
        QToolBar, QStatusBar, QAction
    )

    logging.basicConfig(level=logging.INFO)
    from .__main__ import run_workflow

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("RPA Workflow Runner")
            self.resize(600, 400)
            self.workflow_file = "workflow.json"

            self.log_box = QTextEdit()
            self.log_box.setReadOnly(True)

            # Toolbar actions
            open_action = QAction("Open", self)
            run_action = QAction("Run", self)
            open_action.triggered.connect(self.open_file)
            run_action.triggered.connect(self.run)

            toolbar = QToolBar()
            toolbar.addAction(open_action)
            toolbar.addAction(run_action)
            self.addToolBar(toolbar)

            # Buttons in main area
            btn_open = QPushButton("Open Workflow")
            btn_run = QPushButton("Run")
            btn_open.clicked.connect(self.open_file)
            btn_run.clicked.connect(self.run)

            btn_row = QHBoxLayout()
            btn_row.addWidget(btn_open)
            btn_row.addWidget(btn_run)

            layout = QVBoxLayout()
            layout.addLayout(btn_row)
            layout.addWidget(self.log_box)
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

            self.setStatusBar(QStatusBar())

        def log(self, msg: str) -> None:
            self.log_box.append(msg)
            if self.statusBar():
                self.statusBar().showMessage(msg, 5000)

        def open_file(self):
            path, _ = QFileDialog.getOpenFileName(self, "Open Workflow", "", "JSON Files (*.json)")
            if path:
                self.workflow_file = path
                self.log(f"Loaded {path}")

        def run(self):
            try:
                self.log(f"Running {self.workflow_file}")
                run_workflow(self.workflow_file)
                self.log("Finished")
            except Exception as exc:
                self.log(f"Error: {exc}")

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
