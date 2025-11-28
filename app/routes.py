from flask import Blueprint, jsonify
from app.models import db, User, Post
from datetime import datetime
from app.services.checkCtl import envCheck as check
from app.services.checkCtl import sqlCheck, sqlprase

# 创建蓝图
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# 错误处理
@main_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源未找到'}), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

# 主路由
@main_bp.route('/')
def index():
    return jsonify({
        'message': '欢迎使用Flask API',
        'endpoints': {
            '健康检查': '/health'
        }
    })

@main_bp.route('/env/check', endpoint='env_check_current')
def env_check_route():
    check()
    return jsonify({'message': 'success'})

@main_bp.route('/sqlprase')
def sqlprase_to_file():
    sqlprase()
    return jsonify({'message': 'success'})

@main_bp.route('/sqlcheck/<string:fileName>', methods=['GET'], endpoint='sqlcheck')
def sql_test(fileName):
    try:
        print(f"Processing file: {fileName} ====================")
        
        # 安全检查：验证文件名
        if not fileName.endswith('.json') or fileName.endswith('.yaml'):
            return jsonify({'error': 'Only JSON/YAML files are allowed'}), 400
        
        # 防止路径遍历攻击
        if '/' in fileName or '\\' in fileName or '..' in fileName:
            return jsonify({'error': 'Invalid file name'}), 400
        
        # 调用SQL检查函数
        sqlCheck(fileName)
        
        return jsonify({
            'message': 'success, please see the output folder',
            'file_processed': fileName
        })
        
    except FileNotFoundError:
        return jsonify({'error': f'File {fileName} not found in output folder'}), 404
    except Exception as e:
        print(f"Error processing file {fileName}: {str(e)}")
        return jsonify({'error': 'File processing failed'}), 500
    

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

