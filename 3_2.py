import psutil
# subprocess.Popen([r"C:\Program Files\Notepad++\Notepad++.exe"])

# print(psutil.process_iter(['pid', 'name']))

# for proc in psutil.process_iter(['pid', 'name']):
#     try:
#         print(proc.info)
#     except (psutil.NoSuchProcess, psutil.AccessDenied):
#         print("Error!!Q")

# for process in psutil.process_iter(['pid', 'name']):
#     if process.info['name'] == 'cmd.exe':
#         process.kill()


import sys
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView
)
from PyQt6.QtCore import QTimer, Qt

class ProcessManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.resize(700,500)


        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Որոնել պրոցես ըստ անվան․․․")
        self.search_input.textChanged.connect(self.filter_processes)
        top_layout.addWidget(self.search_input)

        self.refresh_button = QPushButton("Թարմացնել")
        self.refresh_button.clicked.connect(self.load_processes)
        top_layout.addWidget(self.refresh_button)

        layout.addLayout(top_layout)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['PID', 'Անուն', 'CPU %', 'Հիշողություն MB'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.table)  


        bottom_layout = QHBoxLayout()

        self.status_label = QLabel("Պրոցեսներ ")

        bottom_layout.addWidget(self.status_label)

        self.kill_button = QPushButton("Ընդհատել")
        self.kill_button.clicked.connect(self.process_kill) 
        bottom_layout.addWidget(self.kill_button) 

        layout.addLayout(bottom_layout)


        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.load_processes)
        self.timer.start()

        self.load_processes()


    def load_processes(self):
        selected_pid = self.get_selected_pid()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        process_list = []

        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                info = process.info_policy if hasattr(process, 'info_policy') else process.info
                pid = info['pid']
                name = info['name']
                cpu = info['cpu_percent'] or 0.0
                mem = info['memory_info'].rss / (1024 * 1024) if info['memory_info'] else 0.0
                
                
                process_list.append((pid, name, cpu, mem))
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        self.table.setRowCount(len(process_list))
        row_to_select = -1
        for row, (pid, name, cpu, mem) in enumerate(process_list):
            pid_item = QTableWidgetItem()
            pid_item.setData(Qt.ItemDataRole.DisplayRole, pid)
            name_item = QTableWidgetItem(name)
            cpu_item = QTableWidgetItem()
            cpu_item.setData(Qt.ItemDataRole.DisplayRole, round(cpu, 1))
            mem_item = QTableWidgetItem()
            mem_item.setData(Qt.ItemDataRole.DisplayRole, round(mem, 1))

            self.table.setItem(row, 0, pid_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, cpu_item)
            self.table.setItem(row, 3, mem_item)

            if pid == selected_pid:
                row_to_select = row

        self.table.setSortingEnabled(True)

        if row_to_select != -1:
            self.table.selectRow(row_to_select)

        self.filter_processes()
        self.status_label.setText(f"Պրոցեսներ՝ {len(process_list)}")
    
    def process_kill(self):
        pid = self.get_selected_pid()
        if pid is None:
            QMessageBox.warning(self, "Զգուշացում", "Խնդրում ենք ընտրել որևէ պրոցես")
            return

        selected_rows = self.table.selectionModel().selectedRows()
        row = selected_rows[0].row()
        proc_name = self.table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Հաստատում",
            f"Վստա՞հ եք որ ուզում եք ընդհատել {proc_name} պրոցեսը",
            QMessageBox.standardButton.Yes | QMessageBox.standardButton.No, QMessageBox.StandardButton.No
            )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                p = psutil.Process(pid)
                p.terminate()
                QMessageBox.information(self, "Հաջողված է", "Պրոցեսն ընդհատվեց")
                self.load_processes()
            except psutil.NoSuchProcess:
                QMessageBox.critical(self, "Սխալ", "Պրոցեսը գույություն չունի")
            except psutil.AccessDenied:
                QMessageBox.critical(self, "Սխալ", "Դուք իրավունք չունեք պրոցես ջնջելու")
            except Exception as e:
                QMessageBox.critical(self, "Սխալ", f"Չհաջողվեց ավարտել պրոցեսը {str(e)}")
                


    def filter_processes(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            if name_item:
                matches = search_text in name_item.text().lower()
                self.table.setRowHidden(row, not matches)

    def get_selected_pid(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            pid_item = self.table.item(row, 0)
            if pid_item:
                return pid_item.data(Qt.ItemDataRole.DisplayRole)

        return None 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessManager()
    window.show()
    sys.argv[0]
    sys.exit(app.exec())
