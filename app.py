# import logging
# import sys
# from flask import Flask
#
# from controller.modeController import model_bp
# from logger import setup_logging, logFilePath
#
# app = Flask(__name__)
# logger = logging.getLogger(__name__)
#
#
# if __name__ == '__main__':
#     # 从环境变量中读取端口号
#     port = int(sys.argv[1] if len(sys.argv)>=2 else 5000)
#     # 从命令行参数中读取debug模式
#     debug= bool(int(sys.argv[2] if len(sys.argv)>=3 else 1))
#     #logfile路径
#     logfile=logFilePath(sys.argv[3] if len(sys.argv) >= 4 else 'logs')
#
#     setup_logging(logfile)
#
#     # 注册蓝图
#     app.register_blueprint(model_bp)
#     logging.info(f"Starting Flask app on port {port} in debug={debug} mode")
#     # 启动Flask应用
#     app.run(port=port, debug=debug)


import logging
import sys
import os
from flask import Flask, jsonify

from controller.modeController import model_bp
from logger import setup_logging, logFilePath

# 创建Flask应用
app = Flask(__name__)
logger = logging.getLogger(__name__)


# 添加错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '未找到请求的资源'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


# 添加健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200


# 主程序入口
if __name__ == '__main__':
    # 从环境变量或命令行参数中读取配置
    port = int(sys.argv[1] if len(sys.argv) >= 2 else os.environ.get('PORT', 5000))
    debug = bool(int(sys.argv[2] if len(sys.argv) >= 3 else os.environ.get('DEBUG', 1)))
    log_dir = sys.argv[3] if len(sys.argv) >= 4 else os.environ.get('LOG_DIR', 'logs')

    # 配置日志
    logfile = logFilePath(log_dir)
    setup_logging(logfile)

    # 注册蓝图
    app.register_blueprint(model_bp)

    # 启动应用
    logger.info(f"启动Flask应用，端口:{port}，调试模式:{debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)