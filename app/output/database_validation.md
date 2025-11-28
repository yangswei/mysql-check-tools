# 数据库结构校验报告

**校验时间**: 2025-11-27 15:14:48
**数据库地址**: localhost:3306
**用户名**: root

## 数据库: ecommerce_db ✅

### 表: users ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `user_id` | `INT` | `int` | ✅ |
| `username` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `email` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `password_hash` | `VARCHAR(255)` | `varchar(255)` | ✅ |
| `full_name` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `created_at` | `TIMESTAMP` | `timestamp` | ✅ |
| `updated_at` | `TIMESTAMP` | `timestamp` | ✅ |
| `status` | `ENUM('active'` | `enum('active','inactive','suspended')` | ⚠️ 类型不匹配 |

### 表: products ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `product_id` | `INT` | `int` | ✅ |
| `product_name` | `VARCHAR(200)` | `varchar(200)` | ✅ |
| `description` | `TEXT` | `text` | ✅ |
| `price` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `stock_quantity` | `INT` | `int` | ✅ |
| `category_id` | `INT` | `int` | ✅ |
| `brand` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `image_url` | `VARCHAR(500)` | `varchar(500)` | ✅ |
| `created_at` | `TIMESTAMP` | `timestamp` | ✅ |
| `is_available` | `BOOLEAN` | `tinyint(1)` | ⚠️ 类型不匹配 |

### 表: orders ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `order_id` | `INT` | `int` | ✅ |
| `user_id` | `INT` | `int` | ✅ |
| `order_date` | `TIMESTAMP` | `timestamp` | ✅ |
| `total_amount` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `shipping_address` | `TEXT` | `text` | ✅ |
| `order_status` | `ENUM('pending'` | `enum('pending','confirmed','shipped','delivered','cancelled')` | ⚠️ 类型不匹配 |
| `payment_method` | `ENUM('credit_card'` | `enum('credit_card','paypal','bank_transfer','cash_on_delivery')` | ⚠️ 类型不匹配 |
| `tracking_number` | `VARCHAR(100)` | `varchar(100)` | ✅ |

## 数据库: school_management ✅

### 表: students ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `student_id` | `INT` | `int` | ✅ |
| `student_code` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `first_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `last_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `date_of_birth` | `DATE` | `date` | ✅ |
| `gender` | `ENUM('Male'` | `enum('Male','Female','Other')` | ⚠️ 类型不匹配 |
| `email` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `address` | `TEXT` | `text` | ✅ |
| `enrollment_date` | `DATE` | `date` | ✅ |
| `class_id` | `INT` | `int` | ✅ |
| `guardian_name` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `guardian_phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |

### 表: teachers ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `teacher_id` | `INT` | `int` | ✅ |
| `teacher_code` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `first_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `last_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `email` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `department` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `hire_date` | `DATE` | `date` | ✅ |
| `salary` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `specialization` | `VARCHAR(200)` | `varchar(200)` | ✅ |
| `office_room` | `VARCHAR(20)` | `varchar(20)` | ✅ |

### 表: courses ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `course_id` | `INT` | `int` | ✅ |
| `course_code` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `course_name` | `VARCHAR(200)` | `varchar(200)` | ✅ |
| `credits` | `INT` | `int` | ✅ |
| `description` | `TEXT` | `text` | ✅ |
| `teacher_id` | `INT` | `int` | ✅ |
| `semester` | `ENUM('Spring'` | `enum('Spring','Summer','Fall','Winter')` | ⚠️ 类型不匹配 |
| `academic_year` | `YEAR` | `year` | ✅ |
| `max_students` | `INT` | `int` | ✅ |

## 数据库: hr_system ✅

### 表: departments ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `department_id` | `INT` | `int` | ✅ |
| `department_name` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `manager_id` | `INT` | `int` | ✅ |
| `location` | `VARCHAR(200)` | `varchar(200)` | ✅ |
| `budget` | `DECIMAL(15` | `decimal(15,2)` | ⚠️ 类型不匹配 |
| `established_date` | `DATE` | `date` | ✅ |
| `description` | `TEXT` | `text` | ✅ |

### 表: employees ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `employee_id` | `INT` | `int` | ✅ |
| `employee_code` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `first_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `last_name` | `VARCHAR(50)` | `varchar(50)` | ✅ |
| `email` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `hire_date` | `DATE` | `date` | ✅ |
| `job_title` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `department_id` | `INT` | `int` | ✅ |
| `salary` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `date_of_birth` | `DATE` | `date` | ✅ |
| `gender` | `ENUM('Male'` | `enum('Male','Female','Other')` | ⚠️ 类型不匹配 |
| `emergency_contact` | `VARCHAR(100)` | `varchar(100)` | ✅ |
| `emergency_phone` | `VARCHAR(20)` | `varchar(20)` | ✅ |
| `employment_status` | `ENUM('Full-time'` | `enum('Full-time','Part-time','Contract','Intern')` | ⚠️ 类型不匹配 |

### 表: attendance ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `attendance_id` | `INT` | `int` | ✅ |
| `employee_id` | `INT` | `int` | ✅ |
| `attendance_date` | `DATE` | `date` | ✅ |
| `check_in_time` | `TIME` | `time` | ✅ |
| `check_out_time` | `TIME` | `time` | ✅ |
| `work_hours` | `DECIMAL(4` | `decimal(4,2)` | ⚠️ 类型不匹配 |
| `status` | `ENUM('Present'` | `enum('Present','Absent','Late','Early Leave','Vacation','Sick Leave')` | ⚠️ 类型不匹配 |
| `notes` | `TEXT` | `text` | ✅ |

### 表: payroll ✅

| 字段名 | 预期类型 | 实际类型 | 状态 |
|-------|---------|---------|------|
| `payroll_id` | `INT` | `int` | ✅ |
| `employee_id` | `INT` | `int` | ✅ |
| `pay_period_start` | `DATE` | `date` | ✅ |
| `pay_period_end` | `DATE` | `date` | ✅ |
| `basic_salary` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `overtime_pay` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `bonus` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `deductions` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `net_salary` | `DECIMAL(10` | `decimal(10,2)` | ⚠️ 类型不匹配 |
| `payment_date` | `DATE` | `date` | ✅ |
| `payment_method` | `ENUM('Bank` | `enum('Bank Transfer','Cash','Check')` | ⚠️ 类型不匹配 |
| `remarks` | `TEXT` | `text` | ✅ |


---
*报告生成完成*