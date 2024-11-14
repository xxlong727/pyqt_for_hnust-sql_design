import pymysql

# 配置数据库连接参数
db_config = {
    'host': 'localhost',       # 数据库主机地址
    'user': 'root',           # 数据库用户名
    'password': 'xxlong727',  # 数据库密码
    'database': 'xsgl',       # 数据库名
    'charset': 'utf8mb4',      # 字符编码
}

# 创建数据库连接
connection = pymysql.connect(**db_config)

try:
    # 创建cursor对象
    with connection.cursor() as cursor:
        # 定义创建表的SQL语句
        create_department_sql = """
        CREATE TABLE department (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            manager VARCHAR(255),
            intro TEXT
        );
        """
        create_edu_level_sql = """
        CREATE TABLE edu_level (
            code INT PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        );
        """
        create_job_sql = """
        CREATE TABLE job (
            code INT PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        );
        """
        create_personnel_change_sql = """
        CREATE TABLE personnel_change (
            code INT PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        );
        """
        create_person_sql = """
        CREATE TABLE person (
            id INT PRIMARY KEY AUTO_INCREMENT,
            passwd VARCHAR(255) NOT NULL,
            authority INT DEFAULT 0,
            name VARCHAR(255) NOT NULL,
            sex VARCHAR(10),
            birthday DATE,
            department_id INT,
            job INT,
            edu_level INT,
            spcialty VARCHAR(255),
            address VARCHAR(255),
            tel VARCHAR(20),
            email VARCHAR(255),
            state BOOLEAN DEFAULT TRUE,
            remark TEXT,
            FOREIGN KEY (department_id) REFERENCES department(id),
            FOREIGN KEY (edu_level) REFERENCES edu_level(code),
            FOREIGN KEY (job) REFERENCES job(code)
        );
        """
        create_personnel_sql = """
        CREATE TABLE personnel (
            id INT PRIMARY KEY AUTO_INCREMENT,
            person_id INT,
            chang INT,
            description TEXT,
            FOREIGN KEY (person_id) REFERENCES person(id),
            FOREIGN KEY (chang) REFERENCES personnel_change(code)
        );
        """

        # 执行SQL语句
      #  cursor.execute(create_department_sql)
       # cursor.execute(create_edu_level_sql)
      #  cursor.execute(create_job_sql)
      #  cursor.execute(create_personnel_change_sql)
      #  cursor.execute(create_person_sql)
        cursor.execute(create_personnel_sql)
        
    # 提交事务
    connection.commit()
    print("Tables created successfully.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    # 关闭数据库连接
    connection.close()