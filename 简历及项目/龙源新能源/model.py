import torch
import torch.nn as nn

input_size = 26  # 输入的26个特征值
hidden_size = 256
num_layers = 2
dropout = 0.5
output_size = 96  # 输出一天的值
learning_rate = 1e-3
require_imporve = 3000
last_improve = 0
flag = False  # 判断是否需要终止训练

'''
input_size=26 #输入的26个特征值
hidden_size=256
num_layers=2
dropout=0.5
output_size=96 #输出一天的值
learning_rate=1e-3
require_imporve=1000
last_improve=0
flag=False #判断是否需要终止训练
Epoch [90501/100000], train_Loss: 371662144.0,best_mse:16560.134765625
ckpt

lstm+attention 差不多有 
Epoch [13501/200000], train_Loss: 371707968.0,best_mse:16517.19921875 
'''
class trans_LSTMModel(nn.Module):
    # d_model : number of features
    def __init__(self, num_layers=3, nhead=4, dropout=0.2):
        super(trans_LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

        """
        `d_model`：模型的维度，也就是输入和输出的特征维度。
        `nhead`：注意力头数，控制多头注意力的并行度。
        """
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=nhead, dropout=dropout,
                                                        batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers,
                                                         mask_check=False)

        self.decoder = nn.Linear(hidden_size, output_size)  # feature_size是input的个数，1为output个数
        self.init_weights()

    # init_weight主要是用于设置decoder的参数
    def init_weights(self):
        initrange = 0.1
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

    def forward(self, x):
        output, (h0, c0) = self.lstm(x)

        mask = None
        output = self.transformer_encoder(output)
        # print(output.shape)
        output = self.decoder(output[:, -1, :])
        return output