import json
import logging
from typing import Dict, Any, List, Optional

from PySide6 import QtWidgets, QtCore

from rpa import Step, Workflow


class QTextEditLogger(logging.Handler):
    """Logging handler that writes to a QTextEdit widget."""

    def __init__(self, widget: QtWidgets.QTextEdit):
        super().__init__()
        self.widget = widget
        self.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.widget.append(msg)


class StepDialog(QtWidgets.QDialog):
    """Dialog to create or edit a step."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Add Step")
        self.layout = QtWidgets.QFormLayout(self)

        self.action_combo = QtWidgets.QComboBox()
        self.action_combo.addItems(
            [
                "click",
                "input",
                "screenshot",
                "file_copy",
                "excel_write",
                "if",
                "for",
                "notify",
            ]
        )
        self.layout.addRow("Action", self.action_combo)
        self.param_edits: Dict[str, QtWidgets.QLineEdit] = {}

        self.action_combo.currentTextChanged.connect(self._build_fields)
        self._build_fields(self.action_combo.currentText())

        btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        self.layout.addRow(btn_box)

    def _clear_fields(self) -> None:
        for widget in self.param_edits.values():
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.param_edits.clear()

    def _build_fields(self, action: str) -> None:
        self._clear_fields()
        if action == "click":
            self.param_edits["x"] = QtWidgets.QLineEdit()
            self.param_edits["y"] = QtWidgets.QLineEdit()
        elif action == "input":
            self.param_edits["text"] = QtWidgets.QLineEdit()
        elif action == "screenshot":
            self.param_edits["path"] = QtWidgets.QLineEdit("screenshot.png")
        elif action == "file_copy":
            self.param_edits["src"] = QtWidgets.QLineEdit()
            self.param_edits["dst"] = QtWidgets.QLineEdit()
        elif action == "excel_write":
            self.param_edits["path"] = QtWidgets.QLineEdit()
            self.param_edits["cell"] = QtWidgets.QLineEdit()
            self.param_edits["value"] = QtWidgets.QLineEdit()
        elif action == "if":
            self.param_edits["condition"] = QtWidgets.QLineEdit()
        elif action == "for":
            self.param_edits["count"] = QtWidgets.QLineEdit("1")
        elif action == "notify":
            self.param_edits["message"] = QtWidgets.QLineEdit()
            self.param_edits["email"] = QtWidgets.QLineEdit()

        for name, widget in self.param_edits.items():
            self.layout.insertRow(self.layout.rowCount() - 1, name, widget)

    def get_step(self) -> Dict[str, Any]:
        params = {k: w.text() for k, w in self.param_edits.items() if w.text()}
        return {"action": self.action_combo.currentText(), "params": params}


class MainWindow(QtWidgets.QWidget):
    """Main application window with step management."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA GUI")
        layout = QtWidgets.QVBoxLayout(self)

        self.step_list = QtWidgets.QListWidget()
        self.step_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.step_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        layout.addWidget(self.step_list)

        btn_layout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add")
        self.remove_btn = QtWidgets.QPushButton("Remove")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        layout.addLayout(btn_layout)

        file_layout = QtWidgets.QHBoxLayout()
        self.load_btn = QtWidgets.QPushButton("Load")
        self.save_btn = QtWidgets.QPushButton("Save")
        self.run_btn = QtWidgets.QPushButton("Run")
        file_layout.addWidget(self.load_btn)
        file_layout.addWidget(self.save_btn)
        file_layout.addWidget(self.run_btn)
        layout.addLayout(file_layout)

        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.add_btn.clicked.connect(self.add_step)
        self.remove_btn.clicked.connect(self.remove_step)
        self.load_btn.clicked.connect(self.load_workflow)
        self.save_btn.clicked.connect(self.save_workflow)
        self.run_btn.clicked.connect(self.run_workflow)

        self.logger = logging.getLogger("rpa_gui")
        self.logger.setLevel(logging.INFO)
        handler = QTextEditLogger(self.log_text)
        self.logger.addHandler(handler)

    def add_step(self) -> None:
        dialog = StepDialog(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            step = dialog.get_step()
            self.step_list.addItem(json.dumps(step, ensure_ascii=False))

    def remove_step(self) -> None:
        row = self.step_list.currentRow()
        if row >= 0:
            self.step_list.takeItem(row)

    def load_workflow(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load Workflow", "", "JSON (*.json)"
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            steps = json.load(f)
        self.step_list.clear()
        for step in steps:
            self.step_list.addItem(json.dumps(step, ensure_ascii=False))

    def save_workflow(self) -> None:
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Workflow", "workflow.json", "JSON (*.json)"
        )
        if not path:
            return
        steps = [
            json.loads(self.step_list.item(i).text())
            for i in range(self.step_list.count())
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(steps, f, ensure_ascii=False, indent=2)

    def run_workflow(self) -> None:
        steps = [
            json.loads(self.step_list.item(i).text())
            for i in range(self.step_list.count())
        ]
        workflow_steps = [Step(s["action"], s.get("params", {})) for s in steps]
        workflow = Workflow(workflow_steps)
        try:
            workflow.run()
            self.logger.info("Workflow completed")
        except Exception as exc:  # pragma: no cover - GUI runtime
            self.logger.error("Execution failed: %s", exc)
            QtWidgets.QMessageBox.critical(self, "Error", str(exc))


def main() -> None:  # pragma: no cover - manual launch
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.resize(600, 400)
    win.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover
    main()
