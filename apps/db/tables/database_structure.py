import pyodbc
conn_str = ("Driver={SQL Server};"
               "Server=localhost;"
               "Database=StoreManagement;"
               "UID=Reece;"
               "PWD=Madness9900;"
               "Trusted_Connection=yes;")
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def create_first_table():
    cursor.execute("CREATE TABLE auth_user "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "username NVARCHAR(150) NOT NULL UNIQUE, "
                   "email NVARCHAR(254) NOT NULL, "
                   "first_name NVARCHAR(150) NOT NULL, "
                   "last_name NVARCHAR(150) NOT NULL, "
                   "is_active BIT DEFAULT 1, "
                   "is_staff BIT DEFAULT 0, "
                   "is_superuser BIT DEFAULT 0, "
                   "date_joined DATETIME2 DEFAULT GETDATE(), "
                   "last_login DATETIME2 NULL, "
                   "password NVARCHAR(128) NOT NULL)")
    cursor.commit()
# create_first_table()
def create_second_table():
    cursor.execute("CREATE TABLE Regions "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "region_name NVARCHAR(100) NOT NULL UNIQUE, "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_Regions_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_Regions_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id))")
    cursor.commit()
create_second_table()
def create_third_table():
    cursor.execute("CREATE TABLE Stores "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "store_id NVARCHAR(10) NOT NULL UNIQUE, "
                   "store_name NVARCHAR(30) NOT NULL, "
                   "region_id INT NULL, "
                   "is_head_office BIT DEFAULT 0, "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_Stores_Region FOREIGN KEY (region_id) REFERENCES Regions(id), "
                   "CONSTRAINT FK_Stores_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_Stores_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT CK_StoreID_Format CHECK (store_id LIKE '[A-Z][A-Z][A-Z][0-9]%' AND LEN(store_id) BETWEEN 4 AND 8))")
    cursor.commit()
create_third_table()
def create_fourth_table():
    cursor.execute("CREATE TABLE RegionalCoaches "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "first_name NVARCHAR(50) NOT NULL, "
                   "last_name NVARCHAR(50) NOT NULL, "
                   "cell_phone NVARCHAR(15), "
                   "email_address NVARCHAR(100), "
                   "employee_code NVARCHAR(20) NOT NULL UNIQUE, "
                   "is_active BIT DEFAULT 1, "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_RegionalCoaches_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_RegionalCoaches_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id))")
    cursor.commit()
create_fourth_table()

def create_fifth_table():
    cursor.execute("CREATE TABLE AreaCoaches "
                  "(id INT IDENTITY(1,1) PRIMARY KEY, "
                  "first_name NVARCHAR(50) NOT NULL, "
                  "last_name NVARCHAR(50) NOT NULL, "
                  "cell_phone NVARCHAR(15), "
                  "email_address NVARCHAR(100), "
                  "employee_code NVARCHAR(20) NOT NULL UNIQUE, "
                  "is_active BIT DEFAULT 1, "
                  "created_at DATETIME2 DEFAULT GETDATE(), "
                  "updated_at DATETIME2 DEFAULT GETDATE(), "
                  "created_by_id INT NOT NULL, "
                  "updated_by_id INT NOT NULL, "
                  "CONSTRAINT FK_AreaCoaches_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                  "CONSTRAINT FK_AreaCoaches_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id))")
    cursor.commit()
create_fifth_table()
def create_sixth_table():
    cursor.execute("CREATE TABLE BusinessPartners "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "first_name NVARCHAR(50) NOT NULL, "
                   "last_name NVARCHAR(50) NOT NULL, "
                   "cell_phone NVARCHAR(15), "
                   "email_address NVARCHAR(100), "
                   "employee_code NVARCHAR(20) NOT NULL UNIQUE, "
                   "is_active BIT DEFAULT 1, "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_BusinessPartners_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_BusinessPartners_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id))")
    cursor.commit()
create_sixth_table()
def create_seventh_table():
    cursor.execute(" CREATE TABLE Employees "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "first_name NVARCHAR(50) NOT NULL, "
                   "last_name NVARCHAR(50) NOT NULL, "
                   "cell_phone NVARCHAR(15), "
                   "email_address NVARCHAR(100), "
                   "employee_code NVARCHAR(20) NOT NULL UNIQUE, "
                   "store_id INT NOT NULL, "
                   "employee_type NVARCHAR(20) DEFAULT 'EMPLOYEE', "
                   "is_active BIT DEFAULT 1, "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_Employees_Store FOREIGN KEY (store_id) REFERENCES Stores(id), "
                   "CONSTRAINT FK_Employees_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_Employees_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT CK_EmployeeType CHECK (employee_type IN ('EMPLOYEE', 'REGIONAL_COACH', 'AREA_COACH', 'BUSINESS_PARTNER')))")
    cursor.commit()
create_seventh_table()
def create_eighth_table():
    cursor.execute("CREATE TABLE RegionalCoachAssignments "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "regional_coach_id INT NOT NULL, "
                   "store_id INT NOT NULL, "
                   "start_date DATE NOT NULL, "
                   "end_date DATE NULL,  "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_RCA_RegionalCoach FOREIGN KEY (regional_coach_id) REFERENCES RegionalCoaches(id), "
                   "CONSTRAINT FK_RCA_Store FOREIGN KEY (store_id) REFERENCES Stores(id), "
                   "CONSTRAINT FK_RCA_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_RCA_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT CK_RCA_DateRange CHECK (end_date IS NULL OR end_date >= start_date), "
                   "CONSTRAINT UQ_RCA_Current UNIQUE (regional_coach_id, store_id, start_date))")
    cursor.commit()
create_eighth_table()

def create_ninth_table():
    cursor.execute("CREATE TABLE AreaCoachAssignments "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "area_coach_id INT NOT NULL, "
                   "regional_coach_id INT NOT NULL, "
                   "start_date DATE NOT NULL, "
                   "end_date DATE NULL,  "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_ACA_AreaCoach FOREIGN KEY (area_coach_id) REFERENCES AreaCoaches(id), "
                   "CONSTRAINT FK_ACA_RegionalCoach FOREIGN KEY (regional_coach_id) REFERENCES RegionalCoaches(id), "
                   "CONSTRAINT FK_ACA_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_ACA_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT CK_ACA_DateRange CHECK (end_date IS NULL OR end_date >= start_date), "
                   "CONSTRAINT UQ_ACA_Current UNIQUE (area_coach_id, regional_coach_id, start_date))")
    cursor.commit()
create_ninth_table()
def create_tenth_table():
    cursor.execute("CREATE TABLE BusinessPartnerAssignments "
                   "(id INT IDENTITY(1,1) PRIMARY KEY, "
                   "business_partner_id INT NOT NULL, "
                   "area_coach_id INT NOT NULL, "
                   "start_date DATE NOT NULL, "
                   "end_date DATE NULL,  "
                   "created_at DATETIME2 DEFAULT GETDATE(), "
                   "updated_at DATETIME2 DEFAULT GETDATE(), "
                   "created_by_id INT NOT NULL, "
                   "updated_by_id INT NOT NULL, "
                   "CONSTRAINT FK_BPA_BusinessPartner FOREIGN KEY (business_partner_id) REFERENCES BusinessPartners(id), "
                   "CONSTRAINT FK_BPA_AreaCoach FOREIGN KEY (area_coach_id) REFERENCES AreaCoaches(id), "
                   "CONSTRAINT FK_BPA_CreatedBy FOREIGN KEY (created_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT FK_BPA_UpdatedBy FOREIGN KEY (updated_by_id) REFERENCES auth_user(id), "
                   "CONSTRAINT CK_BPA_DateRange CHECK (end_date IS NULL OR end_date >= start_date), "
                   "CONSTRAINT UQ_BPA_Current UNIQUE (business_partner_id, area_coach_id, start_date))")
    cursor.commit()
create_tenth_table()
def create_index_performance():
    cursor.execute("CREATE INDEX IX_Stores_StoreID ON Stores(store_id); "
                   "CREATE INDEX IX_Stores_Region ON Stores(region_id); "
                   "CREATE INDEX IX_Employees_Store ON Employees(store_id);"
                   "CREATE INDEX IX_Employees_EmployeeCode ON Employees(employee_code);")
    cursor.commit()
create_index_performance()

def create_index_analytics():
    cursor.execute("CREATE INDEX IX_Stores_Region_Created ON Stores(region_id, created_at); "
                   "CREATE INDEX IX_Employees_Type_Store ON Employees(employee_type, store_id)")
    cursor.commit()
create_index_analytics()

def create_index_lookup():
    cursor.execute("CREATE INDEX IX_RCA_RegionalCoach_Current ON RegionalCoachAssignments(regional_coach_id, end_date); "
                   "CREATE INDEX IX_RCA_Store_Current ON RegionalCoachAssignments(store_id, end_date); "
                   "CREATE INDEX IX_RCA_Dates ON RegionalCoachAssignments(start_date, end_date); "
                   "CREATE INDEX IX_ACA_AreaCoach_Current ON AreaCoachAssignments(area_coach_id, end_date); "
                   "CREATE INDEX IX_ACA_RegionalCoach_Current ON AreaCoachAssignments(regional_coach_id, end_date); "
                   "CREATE INDEX IX_ACA_Dates ON AreaCoachAssignments(start_date, end_date); "
                   "CREATE INDEX IX_BPA_BusinessPartner_Current ON BusinessPartnerAssignments(business_partner_id, end_date); "
                   "CREATE INDEX IX_BPA_AreaCoach_Current ON BusinessPartnerAssignments(area_coach_id, end_date); "
                   "CREATE INDEX IX_BPA_Dates ON BusinessPartnerAssignments(start_date, end_date)")
    cursor.commit()
create_index_lookup()
def create_index_code():
    cursor.execute("CREATE INDEX IX_RegionalCoaches_EmployeeCode ON RegionalCoaches(employee_code);"
                   "CREATE INDEX IX_AreaCoaches_EmployeeCode ON AreaCoaches(employee_code);"
                   "CREATE INDEX IX_BusinessPartners_EmployeeCode ON BusinessPartners(employee_code)")
    cursor.commit()
create_index_code()

# def insert_one_sample():
#     cursor.execute("INSERT INTO auth_user (username, email, first_name, last_name, is_staff, is_superuser, password)"
#                    "VALUES ('admin', 'admin@company.com', 'Admin', 'User', 1, 1, 'pbkdf2_sha256$placeholder')")
#     cursor.commit()
