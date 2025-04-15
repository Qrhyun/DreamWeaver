# import logging
# import pandas as pd
# from flask import  request, jsonify ,Blueprint
#
# from service.modelServer import modelPredictServer
# from util.webUtils import result
#
#
# model_bp = Blueprint('modeController', __name__)
# logger = logging.getLogger(__name__)
# @model_bp.route('/predicted', methods=['POST'])
# def predicted():
#     logger.info('Predicted mode')
#
#     # post请求需要以form-data的形式上传文件 且表单key=raw
#     if "raw" not in request.files:
#         logger.info('the key of file part in the request must contains raw')
#         return jsonify({'error': 'No file part in the request'}), 400
#
#     # post请求需要以form-data的形式上传文件 且表单key=raw
#     logger.info(f"the {request.files['raw'].filename}  file  upload was successful " )
#
#     df = pd.read_csv(request.files['raw'])
#     predicted = modelPredictServer(df)
#     if predicted == 'Wakefulness':
#         return result(predicted)
#     elif predicted == 'light_sleep':
#         return result(predicted)
#     elif predicted == 'deep_sleep':
#         return result(predicted)
#     else:
#         return result(predicted)


import logging
import pandas as pd
from flask import request, jsonify, Blueprint

from service.modelServer import modelPredictServer
from util.webUtils import result

model_bp = Blueprint('modeController', __name__)
logger = logging.getLogger(__name__)


@model_bp.route('/predicted', methods=['POST'])
def predicted():
    """
    睡眠分期预测接口
    接收CSV文件并返回预测结果
    """
    logger.info('接收预测请求')

    # 检查是否有文件上传
    if "raw" not in request.files:
        logger.info('请求中没有包含key=raw的文件')
        return jsonify({'error': '请求中没有文件部分'}), 400

    try:
        file = request.files['raw']
        logger.info(f"文件 {file.filename} 上传成功")

        # 读取CSV文件
        df = pd.read_csv(file)

        # 进行预测
        predicted = modelPredictServer(df)

        # 根据预测结果返回响应
        logger.info(f"预测结果: {predicted}")
        return result(predicted)

    except Exception as e:
        logger.error(f"预测过程中发生错误: {str(e)}")
        return jsonify({'error': f'预测失败: {str(e)}'}), 500