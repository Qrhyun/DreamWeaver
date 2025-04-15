# import torch
# from flask import jsonify
#
#
# def jsonToTensor(data):
#     """将json数据转换为tensor"""
#     segment_data = data.to_numpy().reshape(1, 7, 3000)
#     segment_tensor = torch.tensor(
#         segment_data, dtype=torch.float32)
#     return segment_tensor
#
# def result(predicted):
#     '''根据预测结果返回对应的报告'''
#     REPORT = {'wakefulness': 1, 'light_sleep': 2, 'deep_sleep': 3, 'REM': 4, }
#
#     json_data = {"type": predicted, "report": str(REPORT.get(predicted))}
#     return jsonify(json_data)


import torch
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def jsonToTensor(data):
    """
    将json数据转换为tensor
    对于AttnSleep模型，需要确保输入形状符合要求
    """
    try:
        # 将数据转换为numpy数组并重塑为(batch_size, channels, sequence_length)的形式
        segment_data = data.to_numpy().reshape(1, 1, 3000)  # AttnSleep模型需要通道维度为1

        # 转换为tensor
        segment_tensor = torch.tensor(segment_data, dtype=torch.float32)

        logger.debug(f"转换后的tensor形状: {segment_tensor.shape}")
        return segment_tensor
    except Exception as e:
        logger.error(f"转换数据为tensor时出错: {str(e)}")
        raise e


def result(predicted):
    '''根据预测结果返回对应的报告'''
    REPORT = {'wakefulness': 1, 'light_sleep': 2, 'deep_sleep': 3, 'REM': 4, 'unknown': 5}

    json_data = {"type": predicted, "report": str(REPORT.get(predicted, 0))}
    return jsonify(json_data)