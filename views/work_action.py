from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QTextEdit,QHBoxLayout
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QTableWidgetItem, QScrollArea
from PyQt5.QtWidgets import QFormLayout,QLabel,QComboBox

person_list = ["员工号","密码","用户权限-int","姓名","性别","生日","所在部门-int","职务-int",
           "受教育程度-int","专业技能","家庭住址","联系电话","电子邮箱","当前状态","变更"
           ]



class win_work(QDialog):
    def __init__(self,name):
        self.name = name
        super().__init__()
        self.setWindowTitle("员工信息")
        self.resize(850,500)

        ##从数据库中调出用户数据 实现打包为 

        layout = QVBoxLayout()#主布局

        title_mian = QTextEdit("人事管理系统-Worker")
        title_mian.setReadOnly(True)
        title_mian.setFixedHeight(100)
        title_mian.setStyleSheet("QTextEdit { font-size: 40px; }")

        btn_change = QPushButton("修改-确认")#创建另一个窗口进行修改，并在确认后返回登录
        btn_change.setFixedHeight(50)
        btn_change.clicked.connect(lambda:self.change_data(line_list))

        data_work = self.get_data(name)#获得数据

        btn_back = QPushButton("返回登录")
        btn_back.setFixedHeight(50)
        btn_back.clicked.connect(lambda: self.close())

        roll_area = QScrollArea()
       
        widget_data = QWidget()#创建信息容器
        widget_data.resize(900,1000)

        data_layout = QFormLayout() 

        line_list = []

        for data_p,data_w in zip(person_list,data_work):#仅作为数据展示，修改界面重新创建
            text_area = QLineEdit()
            text_area.setFixedHeight(50)
            text_area.setText(str(data_w))#后续修改为自己的数据
            line_list.append(text_area)#将每个文本栏存入列表
            data_layout.addRow(QLabel(data_p),text_area)
        line_list[0].setReadOnly(True)

        widget_data.setLayout(data_layout)
        roll_area.setWidget(widget_data)

        layout.addWidget(title_mian)
        layout.addWidget(btn_change)
        layout.addWidget(btn_back)
        layout.addWidget(roll_area)
        
       # roll_area.setLayout(data_layout)#记得加入主布局
        self.setLayout(layout)
    #获得当前数据

    def change_data(self,change_list):
        data = [line_edit.text() for line_edit in change_list]
      
        connection = pymysql.connect(
        host='localhost',
        user='root',
        password='xxlong727',  # 替换为您的数据库密码
        database='xsgl',  # 替换为您的数据库名
        charset='utf8mb4'
    )
    
        try:
            with connection.cursor() as cursor:
                # 开启事务
                connection.begin()
                
                # 遍历 change_list 中的数据
                
                id = data[0]  # 假设列表的第一个元素是 id
                passwd = data[1]
                authority = data[2]
                name = data[3]
                sex = data[4]
                birthday = data[5]
                department_id = data[6]
                job = data[7]
                edu_level = data[8]
                spcialty = data[9]
                address = data[10]
                tel = data[11]
                email = data[12]
                state = data[13]
                remark = data[14]
                
                # 构建 UPDATE 语句
                update_sql = """
                UPDATE person
                SET passwd=%s, authority=%s, name=%s, sex=%s, birthday=%s, department_id=%s, job=%s, edu_level=%s, spcialty=%s, address=%s, tel=%s, email=%s, state=%s, remark=%s
                WHERE id=%s;
                """
                
                # 执行 SQL 语句
                cursor.execute(update_sql, (passwd, authority, name, sex, birthday, department_id, job, edu_level, spcialty, address, tel, email, state, remark, id))
            
            # 提交事务
            connection.commit()
          #  QMessageBox.warning(self, "Data updated successfully.")
           
        except pymysql.MySQLError as e:
            print(f"Error updating data: {e}")
            connection.rollback()  # 发生错误时回滚事务
        finally:
            self.close()
            connection.close()

        

    def get_data(self,name):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='xxlong727',  # 替换为你的数据库密码
            database='xsgl',  # 替换为你的数据库名
            charset='utf8mb4'
        )
        try:
            with connection.cursor() as cursor:
                # 查询 person 表中的特定数据
                sql = "SELECT * FROM person WHERE name = %s"
                cursor.execute(sql, str(name))
                data = cursor.fetchone()  # 获取单个结果
                
                
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
        finally:
            connection.close()
            return data