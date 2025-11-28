import json
import yaml
import os
from typing import Dict, Any, Optional

class DictFileConverter:
    """
    字典与文件转换工具类
    支持 JSON 和 YAML 格式
    converter.dict_to_file(sample_data, "output/data.yaml", "yaml")
    converter.dict_to_file(sample_data, "output/data.json", "json")
    """
    
    @staticmethod
    def dict_to_file(
        data: Dict[str, Any], 
        file_path: str, 
        file_type: str = 'json'
    ) -> bool:
        """
        将字典对象保存为文件
        
        Args:
            data: 要保存的字典数据
            file_path: 文件路径
            file_type: 文件类型，支持 'json', 'yaml'
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            file_type = file_type.lower()
            
            if file_type == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
            elif file_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                    
            else:
                raise ValueError(f"不支持的文件类型: {file_type}，支持 'json', 'yaml'")
                
            return True
            
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False
    
    @staticmethod
    def file_to_dict(file_path: str) -> Optional[Dict[str, Any]]:
        """
        从文件解析为字典对象（自动根据文件后缀判断类型）
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict or None: 解析后的字典数据，失败返回None
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 根据文件后缀判断类型
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            if ext in ['.json']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
            elif ext in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
                    
            else:
                raise ValueError(f"不支持的文件格式: {ext}，支持 .json, .yaml, .yml")
                
        except Exception as e:
            print(f"解析文件失败: {e}")
            return None
    
    @staticmethod
    def get_supported_types() -> list:
        """
        获取支持的文件类型列表
        
        Returns:
            list: 支持的文件类型
        """
        return ['json', 'yaml']