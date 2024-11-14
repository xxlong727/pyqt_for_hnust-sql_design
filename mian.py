import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QStackedWidget
from PyQt5.QtWidgets import QLineEdit,QTextEdit,QToolTip,QRadioButton
from PyQt5.QtWidgets import QTableWidget,QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QTableWidgetItem,QWhatsThis,QMessageBox
from PyQt5.QtCore import Qt,QEvent

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("人事管理")
        self.resize(500,700)
        layout = QVBoxLayout()

        title_mian = QTextEdit("人事管理系统")
        title_mian.setReadOnly(True)
        title_mian.setFixedHeight(200)
        title_mian.setStyleSheet("QTextEdit { font-size: 48px; }")

        btn_worker = QPushButton("员工登录")
        btn_worker.setFixedHeight(100)

        btn_worker.clicked.connect(self.build_worker)#窗口的构建

        btn_boss = QPushButton("人事登录")
        btn_boss.setFixedHeight(100)
        btn_boss.clicked.connect(self.build_boss)#窗口的构建


        layout.addWidget(title_mian)
        layout.addWidget(btn_worker)
        layout.addWidget(btn_boss)

        self.setLayout(layout)

   

    def build_worker(self):
        self.hide()
        from views.login_action import LoginDialog_worker
        win_login = LoginDialog_worker()  # 创建登录对话框实例

        if not win_login.exec_() : # 显示模态对话框，阻塞直到对话框关闭
            self.show() 
    
    def build_boss(self):
        self.hide()
        from  views.login_action import LoginDialog_boss
        win_login = LoginDialog_boss()  # 创建登录对话框实例
        if not win_login.exec_() : # 显示模态对话框，阻塞直到对话框关闭
            self.show()
            
 
def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()