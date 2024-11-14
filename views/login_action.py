from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QApplication
import pymysql
#员工登录
class LoginDialog_worker(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('员工登录')
        self.resize(300, 200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.usernameLabel = QLabel('用户名:')
        layout.addWidget(self.usernameLabel)
        self.usernameEdit = QLineEdit()
        layout.addWidget(self.usernameEdit)
        
        self.passwordLabel = QLabel('密码:')
        layout.addWidget(self.passwordLabel)
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordEdit)
        
        self.loginButton = QPushButton('登录')
        self.loginButton.clicked.connect(self.login)
        layout.addWidget(self.loginButton)


    
    def login(self):
        from views.work_action import win_work#导入类

        username = self.usernameEdit.text()
        password = self.passwordEdit.text()

        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='xxlong727',  # 替换为您的数据库密码
            database='xsgl',  # 替换为您的数据库名
            charset='utf8mb4'
        )

        try:
            with connection.cursor() as cursor:
                # 查询用户名和密码
                sql = "SELECT * FROM person WHERE name = %s AND passwd = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.hide()  # 登录成功，关闭对话框
                    from views.work_action import win_work  # 导入类
                    boss_win = win_work(username)  # 传入 username
                    boss_win.show()
                    if not boss_win.exec_():
                        self.show()
                    self.close()    
                else:
                    QMessageBox.warning(self, '登录失败', '用户名或密码错误')
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            QMessageBox.warning(self, '数据库错误', '无法连接到数据库')
        finally:
            connection.close()
            
            
#boss登录

class LoginDialog_boss(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('管理员登录')
        self.resize(300, 200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.usernameLabel = QLabel('用户名:')
        layout.addWidget(self.usernameLabel)
        self.usernameEdit = QLineEdit()
        layout.addWidget(self.usernameEdit)
        
        self.passwordLabel = QLabel('密码:')
        layout.addWidget(self.passwordLabel)
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordEdit)
        
        self.loginButton = QPushButton('登录')
        self.loginButton.clicked.connect(self.login)
        layout.addWidget(self.loginButton)


    #boss登录
    def login(self):
        from views.boss_action import win_boss
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        if username == "admin" and password == "admin":  # 假设这是正确的用户名和密码
           # print(1243)
            self.hide() # 登录成功，关闭对话框
            boss_win = win_boss()
            boss_win.show()
           
            if not boss_win.exec_():#不知道什么问题，会一直误判，加双重判断可解决
                 #self.show()
                if not boss_win.exec_():
                    self.close()
            

          #  
        else:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误')


