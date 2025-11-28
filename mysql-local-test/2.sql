-- 创建三个数据库
CREATE DATABASE IF NOT EXISTS `ecommerce_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `school_management` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `hr_system` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用电商数据库
USE `ecommerce_db`;

-- 创建用户表
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(100),
    `phone` VARCHAR(20),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `status` ENUM('active', 'inactive', 'suspended') DEFAULT 'active'
);

-- 创建商品表
CREATE TABLE IF NOT EXISTS `products` (
    `product_id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_name` VARCHAR(200) NOT NULL,
    `description` TEXT,
    `price` DECIMAL(10, 2) NOT NULL,
    `stock_quantity` INT NOT NULL DEFAULT 0,
    `category_id` INT,
    `brand` VARCHAR(100),
    `image_url` VARCHAR(500),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `is_available` BOOLEAN DEFAULT TRUE
);

-- 创建订单表
CREATE TABLE IF NOT EXISTS `orders` (
    `order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `order_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `total_amount` DECIMAL(10, 2) NOT NULL,
    `shipping_address` TEXT NOT NULL,
    `order_status` ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    `payment_method` ENUM('credit_card', 'paypal', 'bank_transfer', 'cash_on_delivery'),
    `tracking_number` VARCHAR(100),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
);

-- 使用学校管理系统数据库
USE `school_management`;

-- 创建学生表
CREATE TABLE IF NOT EXISTS `students` (
    `student_id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_code` VARCHAR(20) NOT NULL UNIQUE,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `gender` ENUM('Male', 'Female', 'Other'),
    `email` VARCHAR(100),
    `phone` VARCHAR(20),
    `address` TEXT,
    `enrollment_date` DATE NOT NULL,
    `class_id` INT,
    `guardian_name` VARCHAR(100),
    `guardian_phone` VARCHAR(20)
);

-- 创建教师表
CREATE TABLE IF NOT EXISTS `teachers` (
    `teacher_id` INT AUTO_INCREMENT PRIMARY KEY,
    `teacher_code` VARCHAR(20) NOT NULL UNIQUE,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `phone` VARCHAR(20),
    `department` VARCHAR(100),
    `hire_date` DATE NOT NULL,
    `salary` DECIMAL(10, 2),
    `specialization` VARCHAR(200),
    `office_room` VARCHAR(20)
);

-- 创建课程表
CREATE TABLE IF NOT EXISTS `courses` (
    `course_id` INT AUTO_INCREMENT PRIMARY KEY,
    `course_code` VARCHAR(20) NOT NULL UNIQUE,
    `course_name` VARCHAR(200) NOT NULL,
    `credits` INT NOT NULL,
    `description` TEXT,
    `teacher_id` INT,
    `semester` ENUM('Spring', 'Summer', 'Fall', 'Winter'),
    `academic_year` YEAR,
    `max_students` INT DEFAULT 30,
    FOREIGN KEY (`teacher_id`) REFERENCES `teachers`(`teacher_id`) ON DELETE SET NULL
);

-- 使用人力资源系统数据库
USE `hr_system`;

-- 创建部门表（先创建不带外键约束的版本）
CREATE TABLE IF NOT EXISTS `departments` (
    `department_id` INT AUTO_INCREMENT PRIMARY KEY,
    `department_name` VARCHAR(100) NOT NULL UNIQUE,
    `manager_id` INT,
    `location` VARCHAR(200),
    `budget` DECIMAL(15, 2),
    `established_date` DATE,
    `description` TEXT
);

-- 创建员工表
CREATE TABLE IF NOT EXISTS `employees` (
    `employee_id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_code` VARCHAR(20) NOT NULL UNIQUE,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `phone` VARCHAR(20),
    `hire_date` DATE NOT NULL,
    `job_title` VARCHAR(100) NOT NULL,
    `department_id` INT,
    `salary` DECIMAL(10, 2) NOT NULL,
    `date_of_birth` DATE,
    `gender` ENUM('Male', 'Female', 'Other'),
    `emergency_contact` VARCHAR(100),
    `emergency_phone` VARCHAR(20),
    `employment_status` ENUM('Full-time', 'Part-time', 'Contract', 'Intern') DEFAULT 'Full-time',
    FOREIGN KEY (`department_id`) REFERENCES `departments`(`department_id`) ON DELETE SET NULL
);

-- 创建考勤表
CREATE TABLE IF NOT EXISTS `attendance` (
    `attendance_id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `attendance_date` DATE NOT NULL,
    `check_in_time` TIME,
    `check_out_time` TIME,
    `work_hours` DECIMAL(4, 2),
    `status` ENUM('Present', 'Absent', 'Late', 'Early Leave', 'Vacation', 'Sick Leave') DEFAULT 'Present',
    `notes` TEXT,
    FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_attendance` (`employee_id`, `attendance_date`)
);

-- 创建薪资表
CREATE TABLE IF NOT EXISTS `payroll` (
    `payroll_id` INT AUTO_INCREMENT PRIMARY KEY,
    `employee_id` INT NOT NULL,
    `pay_period_start` DATE NOT NULL,
    `pay_period_end` DATE NOT NULL,
    `basic_salary` DECIMAL(10, 2) NOT NULL,
    `overtime_pay` DECIMAL(10, 2) DEFAULT 0,
    `bonus` DECIMAL(10, 2) DEFAULT 0,
    `deductions` DECIMAL(10, 2) DEFAULT 0,
    `net_salary` DECIMAL(10, 2) NOT NULL,
    `payment_date` DATE,
    `payment_method` ENUM('Bank Transfer', 'Cash', 'Check'),
    `remarks` TEXT,
    FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`) ON DELETE CASCADE
);

-- 现在为部门表添加外键约束（在员工表创建后）
ALTER TABLE `departments` 
ADD CONSTRAINT `fk_department_manager` 
FOREIGN KEY (`manager_id`) REFERENCES `employees`(`employee_id`) ON DELETE SET NULL;

-- 显示创建的数据库（修正语法）
SHOW DATABASES WHERE `Database` IN ('ecommerce_db', 'school_management', 'hr_system');

-- 显示所有表
SELECT 
    TABLE_SCHEMA as 'Database',
    TABLE_NAME as 'Table'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA IN ('ecommerce_db', 'school_management', 'hr_system')
ORDER BY TABLE_SCHEMA, TABLE_NAME;