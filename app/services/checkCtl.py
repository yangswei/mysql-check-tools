import os
from app.services.dopEnvcheck import dopEnvcheck
from app.services.mysqlParser import MySQLSchemaParser
from app.services.mysqlCheck import DatabaseValidator
from typing import Dict, Any
from app.services.sqldictTofile import DictFileConverter
from pathlib import Path

def envCheck():
    checker = dopEnvcheck()
    system_info = checker.get_system_info()
    print(f"   系统类型: {system_info.get('system', 'Unknown')}")
    print(f"   系统版本: {system_info.get('version', 'Unknown')}")
    print(f"   系统架构: {system_info.get('architecture', 'Unknown')}")
    disk_info = checker.get_disk_mount_info()
    if 'error' in disk_info:
        print(f"   {disk_info['error']}")

    memory_info = checker.get_memory_info()
    if 'error' in memory_info:
        print(f"   {memory_info['error']}")
    else:
        print(f"   总内存: {memory_info.get('total', 'Unknown')}")
        print(f"   可用内存: {memory_info.get('available', memory_info.get('free', 'Unknown'))}")
        if 'usage_percent' in memory_info:
            print(f"   内存使用率: {memory_info['usage_percent']}")

    cpu_info = checker.get_cpu_info()
    if 'error' in cpu_info:
        print(f"   {cpu_info['error']}")
    else:
        print(f"   逻辑核心数: {cpu_info.get('logical_cores', 'Unknown')}")
        print(f"   支持AVX2: {'是' if cpu_info.get('avx2') else '否'}")
        print(f"   支持BMI2: {'是' if cpu_info.get('bmi2') else '否'}")
    kernel_version = checker.get_kernel_version()
    print(f"   {kernel_version}")
    gpu_info = checker.get_gpu_info()
    if 'error' in gpu_info:
        print(f"   {gpu_info['error']}")
    else:
        print(f"   NVIDIA GPU: {gpu_info.get('nvidia', ['无'])[0]}")
        print(f"   Other GPU: {gpu_info.get('other', ['无'])[0]}")
        print(f"   Apple GPU: {gpu_info.get('apple', ['无'])[0]}")

def validate_database_from_schema(schema_dict: Dict, output_file: str = "database_validation.md", 
                                 config_file: str = "database_config.yaml", db_alias: str = "default"):
    """
    基于schema字典校验数据库并生成MD报告
    
    Args:
        schema_dict: 预期的数据库结构
        output_file: 输出文件名
        config_file: 配置文件路径
        db_alias: 数据库配置别名
    """
    validator = DatabaseValidator(config_file=config_file, db_alias=db_alias)
    validator.validate_schema(schema_dict, output_file)

def validate_database_direct(schema_dict: Dict, host: str, username: str, password: str, 
                            output_file: str = "database_validation.md", port: int = 3306):
    """
    直接使用连接参数校验数据库
    
    Args:
        schema_dict: 预期的数据库结构
        host: 数据库主机
        username: 用户名
        password: 密码
        output_file: 输出文件名
        port: 数据库端口
    """
    validator = DatabaseValidator(host=host, username=username, password=password, port=port)
    validator.validate_schema(schema_dict, output_file)

def sqlCheckDemo():
    '''
    这里是完整sql处理,将sql放到sql目录,循环文件夹下的sql文件,通过sqlChecker中的parse_sql_file方法解析为字典,然后通过DictFileConverter中的dict_to_file方法保存为json文件
    在做最终数据校验前,将指定目录的json(或者yaml)解析为dict对象,最后调用mysqlCheck中的sqlCheck,在目标库进行数据校验
    '''
    sqlChecker = MySQLSchemaParser()
    sqlPath = 'app/sql'
    all_items = os.listdir(sqlPath)
    sql_files = [f for f in all_items if f.endswith('.sql')]
    for sql_file in sql_files:
        file_path = os.path.join(sqlPath, sql_file)
        sqlDict = sqlChecker.parse_sql_file(file_path)
        DictFileConverter.dict_to_file(
            data=sqlDict, 
            file_path=f"app/output/{sql_file[:-4]}.json",
            file_type='json'
        )
        sqlDicte = DictFileConverter.file_to_dict("app/output/1.json")
        print(sqlDicte)


def sqlprase():
    sqlChecker = MySQLSchemaParser()
    file_path = 'app/sql/2.sql'
    sqlDict = sqlChecker.parse_sql_file(file_path)
    DictFileConverter.dict_to_file(data=sqlDict, file_path="app/output/2.json", file_type='json')

def sqlCheck(file_name: str = "2.json"):
    """
    这里简单，直接从已经转换的json中获取dict数据进行校验
    """
    try:
        # 使用 pathlib 更安全的路径处理
        output_dir = Path("app/output")
        file_path = output_dir / file_name
        outputfile = output_dir / "database_validation.md"
        
        # 安全检查
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        
        # 防止路径遍历攻击
        if not file_path.resolve().parent.samefile(output_dir.resolve()):
            raise ValueError("Invalid file path")
        
        sql_dict = DictFileConverter.file_to_dict(str(file_path))
        
        validator = DatabaseValidator()
        result = validator.validate_schema(sql_dict, str(outputfile))
        
        return result
        
    except Exception as e:
        raise Exception(f"SQL check failed: {str(e)}")