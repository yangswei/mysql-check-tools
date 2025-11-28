import yaml
import pymysql
from typing import Dict, Optional
import logging
import re
from datetime import datetime

class DatabaseConfig:
    """数据库配置类"""
    def __init__(self, config_file: str = "database_config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载YAML配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                logging.info(f"成功加载配置文件: {self.config_file}")
                return config
        except FileNotFoundError:
            logging.error(f"配置文件未找到: {self.config_file}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"YAML配置文件解析错误: {e}")
            return {}
        except Exception as e:
            logging.error(f"读取配置文件时出错: {e}")
            return {}
    
    def get_database_config(self, db_alias: str = "default") -> Optional[Dict]:
        """获取指定数据库的配置"""
        if not self.config or 'databases' not in self.config:
            logging.error("配置文件中未找到databases配置节")
            return None
        
        databases = self.config['databases']
        
        if db_alias not in databases:
            logging.error(f"数据库别名 '{db_alias}' 在配置文件中未找到")
            available_aliases = list(databases.keys())
            logging.info(f"可用的数据库别名: {available_aliases}")
            return None
        
        db_config = databases[db_alias]
        
        # 设置默认值
        default_config = {
            'host': 'localhost',
            'port': 3306,
            'username': 'root',
            'password': '',
            'charset': 'utf8mb4'
        }
        
        # 合并配置
        for key, value in default_config.items():
            if key not in db_config:
                db_config[key] = value
        
        return db_config
    
    def list_databases(self) -> list:
        """列出所有可用的数据库配置"""
        if not self.config or 'databases' not in self.config:
            return []
        return list(self.config['databases'].keys())

class DatabaseValidator:
    def __init__(self, host: str = None, username: str = None, password: str = None, 
                 port: int = 3306, config_file: str = None, db_alias: str = "default"):
        """支持多种初始化方式：直接参数或配置文件"""
        if host and username and password:
            # 使用直接参数
            self.host = host
            self.username = username
            self.password = password
            self.port = port
            self.config_loader = None
        else:
            # 使用配置文件
            if not config_file:
                config_file = "app/config/database_config.yaml"
            self.config_loader = DatabaseConfig(config_file)
            self.db_config = self.config_loader.get_database_config(db_alias)
            if self.db_config:
                self.host = self.db_config['host']
                self.username = self.db_config['username']
                self.password = self.db_config['password']
                self.port = self.db_config['port']
            else:
                raise ValueError("无法获取数据库配置")
        
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logging.info(f"数据库连接成功: {self.host}:{self.port}")
            return True
        except Exception as e:
            logging.error(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logging.info("数据库连接已关闭")
    
    def validate_schema(self, schema_dict: Dict, output_file: str = "database_validation.md"):
        """
        校验数据库结构并生成MD报告
        
        Args:
            schema_dict: 预期的数据库结构字典 {database: {table: {column: type}}}
            output_file: 输出的MD文件名
        """
        if not self.connect():
            logging.error("无法连接数据库，校验终止")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8') as md_file:
                # 写入MD文件标题
                md_file.write("# 数据库结构校验报告\n\n")
                md_file.write(f"**校验时间**: {self._get_current_time()}\n")
                md_file.write(f"**数据库地址**: {self.host}:{self.port}\n")
                md_file.write(f"**用户名**: {self.username}\n\n")
                
                # 遍历预期的数据库结构
                for db_name, tables in schema_dict.items():
                    self._validate_database(md_file, db_name, tables)
                
                md_file.write("\n---\n*报告生成完成*")
            
            logging.info(f"校验报告已生成: {output_file}")
            
        except Exception as e:
            logging.error(f"生成校验报告时出错: {e}")
        finally:
            self.disconnect()
    
    def _validate_database(self, md_file, db_name: str, tables: Dict):
        """校验单个数据库"""
        try:
            # 检查数据库是否存在
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = [db['Database'] for db in cursor.fetchall()]
                
                if db_name not in databases:
                    md_file.write(f"## 数据库: {db_name} ❌\n\n")
                    md_file.write("*数据库不存在*\n\n")
                    return
                
                md_file.write(f"## 数据库: {db_name} ✅\n\n")
                
                # 切换到该数据库
                cursor.execute(f"USE `{db_name}`")
                
                # 获取当前数据库的所有表
                cursor.execute("SHOW TABLES")
                existing_tables = [list(table.values())[0] for table in cursor.fetchall()]
                
                # 校验表结构
                for table_name, columns in tables.items():
                    self._validate_table(md_file, db_name, table_name, columns, existing_tables)
                    
        except Exception as e:
            logging.error(f"校验数据库 {db_name} 时出错: {e}")
            md_file.write(f"## 数据库: {db_name} ❌\n\n")
            md_file.write(f"*校验过程中出错: {e}*\n\n")
    
    def _validate_table(self, md_file, db_name: str, table_name: str, columns: Dict, existing_tables: list):
        """校验单个表"""
        try:
            if table_name not in existing_tables:
                md_file.write(f"### 表: {table_name} ❌\n\n")
                md_file.write("| 字段名 | 预期类型 | 状态 |\n")
                md_file.write("|-------|---------|------|\n")
                for column_name, expected_type in columns.items():
                    md_file.write(f"| `{column_name}` | `{expected_type}` | ❌ 表不存在 |\n")
                md_file.write("\n")
                return
            
            md_file.write(f"### 表: {table_name} ✅\n\n")
            md_file.write("| 字段名 | 预期类型 | 实际类型 | 状态 |\n")
            md_file.write("|-------|---------|---------|------|\n")
            
            # 获取表的实际结构
            with self.connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE `{table_name}`")
                actual_columns = {col['Field']: col['Type'] for col in cursor.fetchall()}
                
                # 校验每个字段
                for column_name, expected_type in columns.items():
                    self._validate_column(md_file, column_name, expected_type, actual_columns)
            
            md_file.write("\n")
            
        except Exception as e:
            logging.error(f"校验表 {db_name}.{table_name} 时出错: {e}")
            md_file.write(f"### 表: {table_name} ❌\n\n")
            md_file.write(f"*校验过程中出错: {e}*\n\n")
    
    def _validate_column(self, md_file, column_name: str, expected_type: str, actual_columns: Dict):
        """校验单个字段"""
        if column_name not in actual_columns:
            # 字段不存在
            md_file.write(f"| `{column_name}` | `{expected_type}` | - | ❌ 字段不存在 |\n")
        else:
            actual_type = actual_columns[column_name]
            # 简化类型比较（忽略大小写和空格差异）
            expected_simple = self._simplify_type(expected_type)
            actual_simple = self._simplify_type(actual_type)
            
            if expected_simple == actual_simple:
                md_file.write(f"| `{column_name}` | `{expected_type}` | `{actual_type}` | ✅ |\n")
            else:
                md_file.write(f"| `{column_name}` | `{expected_type}` | `{actual_type}` | ⚠️ 类型不匹配 |\n")
    
    def _simplify_type(self, data_type: str) -> str:
        """简化数据类型以便比较"""
        if not data_type:
            return ""
        
        # 转换为小写，移除空格和括号内的空格
        simplified = data_type.lower().strip()
        # 移除多余的空格
        simplified = re.sub(r'\s+', ' ', simplified)
        # 统一处理括号内的空格
        simplified = re.sub(r'\(\s+', '(', simplified)
        simplified = re.sub(r'\s+\)', ')', simplified)
        simplified = re.sub(r',\s+', ',', simplified)
        
        return simplified
    
    def _get_current_time(self):
        """获取当前时间字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")