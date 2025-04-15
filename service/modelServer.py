# import torch
#
# from model.CNN import CNN
# from util.webUtils import jsonToTensor
#
#
# # 模型预测
# def modelPredictServer(segmentData):
#     # json转tensor
#     segment_tensor=jsonToTensor(segmentData)
#
#     model = CNN(segment_tensor.shape, 6)
#     model.load_state_dict(torch.load('saved/trained_model.pth'))
#     sleep_stages = ['wakefulness', 'light_sleep', 'deep_sleep', 'deep_sleep', 'REM']
#     model.eval()
#     with torch.no_grad():
#         outputs = model(segment_tensor)
#         _, predicted_class = torch.max(outputs, 1)
#         predicted_stage = sleep_stages[predicted_class.item() - 1]
#         print("Predicted sleep stage for the segment:", predicted_stage)
#     return predicted_stage
#
#  # def _valid_epoch(self, epoch):
#  #        """
#  #        Validate after training an epoch
#  #
#  #        :param epoch: Integer, current training epoch.
#  #        :return: A log that contains information about validation
#  #        """
#  #        self.model.eval()
#  #        self.valid_metrics.reset()
#  #        with torch.no_grad():
#  #            outs = np.array([])
#  #            trgs = np.array([])
#  #            for batch_idx, (data, target) in enumerate(self.valid_data_loader):
#  #                data, target = data.to(self.device), target.to(self.device)
#  #                output = self.model(data)
#  #                loss = self.criterion(output, target, self.class_weights, self.device)
#  #
#  #                self.valid_metrics.update('loss', loss.item())
#  #                for met in self.metric_ftns:
#  #                    self.valid_metrics.update(met.__name__, met(output, target))
#  #
#  #                preds_ = output.data.max(1, keepdim=True)[1].cpu()
#  #
#  #                outs = np.append(outs, preds_.cpu().numpy())
#  #                trgs = np.append(trgs, target.data.cpu().numpy())
#  #
#  #
#  #        return self.valid_metrics.result(), outs, trgs
#  #

import torch
import logging
from model.AttnSleepModel import AttnSleep
from util.webUtils import jsonToTensor

logger = logging.getLogger(__name__)


# 模型预测
def modelPredictServer(segmentData):
    try:
        # json转tensor
        segment_tensor = jsonToTensor(segmentData)

        # 创建AttnSleep模型实例（替换原有CNN模型）
        model = AttnSleep()

        # 加载预训练模型参数
        model.load_state_dict(torch.load('saved/trained_model.pth', map_location=torch.device('cpu')))

        # 设置为评估模式
        model.eval()

        # 定义睡眠阶段映射
        sleep_stages = ['wakefulness', 'light_sleep', 'deep_sleep', 'deep_sleep', 'REM']

        # 进行预测
        with torch.no_grad():
            outputs = model(segment_tensor)
            _, predicted_class = torch.max(outputs, 1)
            predicted_stage = sleep_stages[predicted_class.item() - 1]
            logger.info(f"Predicted sleep stage for the segment: {predicted_stage}")

        return predicted_stage

    except Exception as e:
        logger.error(f"Error in model prediction: {str(e)}")
        # 出错时返回一个默认值
        return "unknown"