from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QTextEdit,QHBoxLayout
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QTableWidgetItem, QScrollArea
from PyQt5.QtWidgets import QFormLayout,QLabel,QComboBox
list_width = [70,70,70,85,70,75,70,70,90,70,100,150,150,75,60]

person_list = ["员工号","密码","用户权限-int","姓名","性别","生日","所在部门-int","职务-int",
           "受教育程度-int","专业技能","家庭住址","联系电话","电子邮箱","当前状态","变更"
           ]

class win_boss(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("人员管理")
        self.resize(1400,500)
        layout = QVBoxLayout()#主布局

        title_mian = QTextEdit("人事管理系统-BOSS")
        title_mian.setReadOnly(True)
        title_mian.setFixedHeight(100)
        title_mian.setStyleSheet("QTextEdit { font-size: 40px; }")

        area_get_layout = QHBoxLayout()#次布局
        #搜索栏
        area_get_worker = QTextEdit()
        area_get_worker.setPlaceholderText("输入")
        area_get_worker.setFixedHeight(40)
        #win_work(

        btn_get_worker = QPushButton("确认")
        btn_get_worker.setFixedHeight(40)
        btn_get_worker.clicked.connect(lambda:self.get_work(area_get_worker.toPlainText()))#窗口的构建

        area_get_layout.addStretch()
        area_get_layout.addWidget(area_get_worker)
        area_get_layout.addWidget(btn_get_worker)

        area_table = QVBoxLayout()#table布局
        table = QTableWidget(10,15)
        for i,width in enumerate(list_width):
            table.setColumnWidth(i,width)
       # table_widget.setFixedHeight(650)
        table.setHorizontalHeaderLabels(person_list)
        #添加下拉菜单
      #  self.set_table(table)

        #加载数据
        self.up_data(table)
       
        btn_done = QPushButton("确认-添加")
        btn_done.clicked.connect(lambda:self.data_sql(table))

        area_table.addWidget(table)
        area_table.addWidget(btn_done)

        btn_back = QPushButton("返回登录")
        btn_back.clicked.connect(lambda: self.close())

        layout.addWidget(title_mian)
        layout.addLayout(area_get_layout)
        layout.addLayout(area_table)
        layout.addWidget(btn_back)

        self.setLayout(layout)
   #加载数据

    def get_work(self,name):
        self.hide()

        win = win_change(name,self)
        win.show()
        if not win.exec_(): 
            self.show()
        #self.close()
     


    def up_data(self,table):
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='xxlong727',  # 替换为你的数据库密码
            database='xsgl',  # 替换为你的数据库名
            charset='utf8mb4'
        )
        try:
            with connection.cursor() as cursor:
                # 查询 person 表中的所有数据
                cursor.execute("SELECT * FROM person")
                data = cursor.fetchall()
                
                # 设置 QTableWidget 的行数
               # table.setRowCount(len(data))
                
                # 填充数据到 QTableWidget
                for row_idx, row_data in enumerate(data):
                    for col_idx, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value))  # 将值转换为字符串
                        table.setItem(row_idx, col_idx, item)
                        
        except pymysql.MySQLError as e:
            print(f"Error fetching data: {e}")
        finally:
            connection.close()

        pass     
  #获取数据并保存
    def data_sql(self, table):
        all_data = []
        for row in range(0,table.rowCount()):#
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                   
                    row_data.append(None)  # 如果单元格为空，添加None或默认值
            all_data.append(row_data)
        
        # 连接数据库
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='xxlong727',  # 替换为你的数据库密码
            database='xsgl',  # 替换为你的数据库名
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # 插入数据到数据库
        try:

            sql = "DELETE FROM `person`"
            
            cursor.execute(sql)
            conn.commit()

            sql = "ALTER TABLE person AUTO_INCREMENT = 0;"
            
            cursor.execute(sql)
            conn.commit()

            # 构建INSERT语句，不包括id字段
            sql = """
            INSERT INTO person 
            (passwd, authority, name, sex, birthday, department_id, job, edu_level, spcialty, address, tel, email, state, remark) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for row_data in all_data:
                # 确保row_data长度与字段数量匹配
                row_data = row_data[1:]

                department_id = row_data[5]# 假设这是我们要插入的 department_id
               
                cursor.execute("SELECT * FROM department WHERE id = %s", (department_id,))
                if cursor.fetchone() is None:
                    # 如果 department_id 不存在，则插入新的部门
                    cursor.execute("INSERT INTO department (id, name) VALUES (%s, %s)", (department_id, 'Department Name'))
                    conn.commit()
                
                # 检查 edu_level 是否存在
                edu_level = row_data[7]# 假设这是我们要插入的 edu_level
                
                cursor.execute("SELECT * FROM edu_level WHERE code = %s", (edu_level,))
                if cursor.fetchone() is None:
                    # 如果 edu_level 不存在，则插入新的教育程度
                    cursor.execute("INSERT INTO edu_level (code, description) VALUES (%s, %s)", (edu_level, 'Education Description'))
                    conn.commit()
                
                # 检查 job 是否存在
                job = row_data[6]  # 假设这是我们要插入的 job
                
                cursor.execute("SELECT * FROM job WHERE code = %s", (job,))
                if cursor.fetchone() is None:
                    # 如果 job 不存在，则插入新的职位
                    cursor.execute("INSERT INTO job (code, description) VALUES (%s, %s)", (job, 'Job Description'))
                    conn.commit()
                
                if len(row_data) == 14:  # 根据实际字段数量调整
                    
                    cursor.execute(sql, tuple(row_data))  # 将列表转换为元组
            conn.commit()
            print("All data saved to database successfully.")
        except pymysql.Error as e:
            print(f"Error saving data: {e}")
        finally:
            cursor.close()
            conn.close()

  
  #设置下拉菜单方法
    def set_table(self, table):
        # 假设表格已经存在并且有足够的行
        for idx in range(0, 10):  # 假设至少有10行

            c_box_6 = QComboBox()  # 为每一行创建一个新的 QComboBox 实例
            c_box_6.addItems([ 0 ,1 , 2 ])
            table.setCellWidget(idx, 6, c_box_6)  # 将 QComboBox 设置到第6列

            c_box_7 = QComboBox()  # 为每一行创建一个新的 QComboBox 实例
            c_box_7.addItems([0 , 1 , 2 , 3])
            table.setCellWidget(idx, 7, c_box_7)  # 将 QComboBox 设置到第6列

            # c_box_8 = QComboBox()  # 为每一行创建一个新的 QComboBox 实例
            # c_box_8.addItems(["无" , "研发" , "销售" , "管理"])
            # table.setCellWidget(idx, 8, c_box_8)  # 将 QComboBox 设置到第6列


#修改界面  
class win_change(QDialog):
    def __init__(self, name,boss):
        super().__init__()
        self.name = name
        self.boss = boss
        super().__init__()
        self.setWindowTitle("员工信息")
        self.resize(850,500)

        ##从数据库中调出用户数据 实现打包为 
        layout = QVBoxLayout()#主布局

        title_mian = QTextEdit("人事管理系统-Worker-Change")
        title_mian.setReadOnly(True)
        title_mian.setFixedHeight(100)
        title_mian.setStyleSheet("QTextEdit { font-size: 40px; }")

        btn_change = QPushButton("修改-确认")#创建另一个窗口进行修改，并在确认后返回登录
        btn_change.setFixedHeight(50)
        btn_change.clicked.connect(lambda:self.change_data(line_list))
        #获得数据
        data_work = self.get_data(name)

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
        layout.addWidget(roll_area)
        
       # roll_area.setLayout(data_layout)#记得加入主布局
        self.setLayout(layout)


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
              #  self.boss.show()
                connection.close()
