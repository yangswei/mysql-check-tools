import re
import logging
from typing import Dict, List, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MySQLSchemaParser:
    def __init__(self):
        self.current_database = None
        self.schema_dict = {}
        
    def parse_sql_file(self, file_path: str) -> Dict:
        """
        解析SQL文件，返回数据库结构字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # 预处理：移除注释和多余的空格
            cleaned_sql = self._preprocess_sql(sql_content)
            
            # 分割SQL语句
            statements = self._split_sql_statements(cleaned_sql)
            
            # 解析每个语句
            for statement in statements:
                self._parse_statement(statement.strip())
            
            return self.schema_dict
            
        except FileNotFoundError:
            logger.error(f"文件未找到: {file_path}")
            return {}
        except Exception as e:
            logger.error(f"解析SQL文件时出错: {e}")
            return {}
    
    def _preprocess_sql(self, sql_content: str) -> str:
        """
        预处理SQL内容，移除注释和多余空格
        """
        # 移除单行注释
        sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)
        # 移除多行注释
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        # 移除多余的空格和换行
        sql_content = re.sub(r'\s+', ' ', sql_content)
        return sql_content
    
    def _split_sql_statements(self, sql_content: str) -> List[str]:
        """
        分割SQL语句，以分号作为分隔符
        """
        # 使用分号分割，但要注意避免分割字符串中的分号
        statements = []
        current_statement = ""
        in_string = False
        string_char = None
        
        for char in sql_content:
            if char in ['"', "'", '`']:
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
            
            current_statement += char
            
            if char == ';' and not in_string:
                statements.append(current_statement.strip())
                current_statement = ""
        
        # 添加最后一个语句（如果没有分号结尾）
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        return statements
    
    def _parse_statement(self, statement: str):
        """
        解析单个SQL语句
        """
        statement_upper = statement.upper()
        
        # 解析 USE 语句
        if statement_upper.startswith('USE '):
            self._parse_use_statement(statement)
        
        # 解析 CREATE TABLE 语句
        elif statement_upper.startswith('CREATE TABLE'):
            self._parse_create_table(statement)
        
        # 其他语句（如数据初始化）可以在这里添加处理逻辑
        # 但根据要求，我们只关注建库建表语句
    
    def _parse_use_statement(self, statement: str):
        """
        解析 USE database 语句
        """
        match = re.match(r'USE\s+([`"]?)(\w+)\1', statement, re.IGNORECASE)
        if match:
            self.current_database = match.group(2)
            logger.info(f"切换到数据库: {self.current_database}")
            
            # 初始化数据库结构
            if self.current_database not in self.schema_dict:
                self.schema_dict[self.current_database] = {}
        else:
            logger.warning(f"无法解析 USE 语句: {statement}")
    
    def _parse_create_table(self, statement: str):
        """
        解析 CREATE TABLE 语句
        """
        if not self.current_database:
            logger.warning("发现 CREATE TABLE 语句但未指定数据库，跳过处理")
            return
        
        # 提取表名
        table_match = re.search(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"]?)(\w+)\1',
            statement, 
            re.IGNORECASE
        )
        
        if not table_match:
            logger.warning(f"无法解析表名: {statement[:100]}...")
            return
        
        table_name = table_match.group(2)
        
        # 初始化表结构
        if table_name not in self.schema_dict[self.current_database]:
            self.schema_dict[self.current_database][table_name] = {}
        
        # 提取字段定义部分
        column_section_match = re.search(
            r'\((.*)\)',
            statement, 
            re.IGNORECASE | re.DOTALL
        )
        
        if not column_section_match:
            logger.warning(f"无法找到字段定义部分: {table_name}")
            return
        
        column_section = column_section_match.group(1)
        
        # 解析字段
        self._parse_columns(column_section, table_name)
        
        logger.info(f"解析表 {self.current_database}.{table_name} 完成")
    
    def _parse_columns(self, column_section: str, table_name: str):
        """
        解析字段定义
        """
        # 分割字段定义，考虑嵌套括号（如约束等）
        column_definitions = self._split_column_definitions(column_section)
        
        for col_def in column_definitions:
            col_def = col_def.strip()
            if not col_def or col_def.upper().startswith(('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY', 'INDEX', 'KEY', 'CONSTRAINT')):
                continue
            
            # 解析字段名和类型
            column_match = re.match(
                r'([`"]?)(\w+)\1\s+([^(]+?(?:\([^)]+\))?[^,]*)(?:,|$)',
                col_def, 
                re.IGNORECASE
            )
            
            if column_match:
                column_name = column_match.group(2)
                column_type = column_match.group(3).split(' ')[0].strip()
                
                # 清理类型定义中的额外空格
                column_type = re.sub(r'\s+', ' ', column_type)
                
                self.schema_dict[self.current_database][table_name][column_name] = column_type
            else:
                logger.warning(f"无法解析字段定义: {col_def[:50]}...")
    
    def _split_column_definitions(self, column_section: str) -> List[str]:
        """
        分割字段定义，处理嵌套括号
        """
        definitions = []
        current_def = ""
        paren_count = 0
        
        for char in column_section:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                definitions.append(current_def.strip())
                current_def = ""
                continue
            
            current_def += char
        
        # 添加最后一个定义
        if current_def.strip():
            definitions.append(current_def.strip())
        
        return definitions

def parse_mysql_schema(sql_file_path: str) -> Dict:
    """
    主函数：解析MySQL SQL文件并返回数据库结构
    
    Args:
        sql_file_path: SQL文件路径
        
    Returns:
        Dict: 数据库结构字典，格式为 {database: {table: {column: type}}}
    """
    parser = MySQLSchemaParser()
    return parser.parse_sql_file(sql_file_path)

def print_schema(schema_dict: Dict, indent: int = 0):
    """
    美化打印数据库结构
    """
    if not schema_dict:
        print("没有解析到数据库结构")
        return
    
    for db_name, tables in schema_dict.items():
        print(" " * indent + f"数据库: {db_name}")
        for table_name, columns in tables.items():
            print(" " * (indent + 2) + f"表名: {table_name}")
            for column_name, column_type in columns.items():
                print(" " * (indent + 4) + f"字段: {column_name} -> {column_type}")