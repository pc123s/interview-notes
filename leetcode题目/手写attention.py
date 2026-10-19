import numpy as np
'''
参考
https://zhuanlan.zhihu.com/p/655425442

'''
class attention_np:
    def softmax(self,x):
        e_x=np.exp(x)
        result=e_x/np.sum(x,axis=-1,keepdims=True)
        return result
    def self_attention(self,x,hidden_dim):
        n,d=x.shape
        print(n,d)
        wq=np.random.rand(d,hidden_dim)
        wk=np.random.rand(d,hidden_dim)
        wv=np.random.rand(d,hidden_dim)
        #print(wq,wk,wv)
        # @代表矩阵相乘
        q=x@wq
        k=x@wk
        v=x@wv
        A=q@k.T
        print(q.shape,k.shape,v.shape,A.shape)
        A=A/np.sqrt(d)
        A_hat=self.softmax(A)
        output=A_hat@v
        print(output.shape)
        return output
    def multi_head_attention(x,hidden_dim,head_n=4):
        '''
        :param x: 输入的embedding以后的向量
        :param hidden_dim:
        :param head_n:
        :return:
        '''
        n,d=x.shape
        # 一定要确保 隐层是头数量的整数倍
        assert hidden_dim%head_n==0
        wq=np.random.rand(d,hidden_dim)
        wk=np.random.rand(d,hidden_dim)
        wv=np.random.rand(d,hidden_dim)
        q=x@wq
        k=x@wk
        v=x@wv
        hidden_dim_=hidden_dim//head_n
        # 按照头数将hidden_dim切分为 head_n份
        q=np.reshape(q,(n,head_n,hidden_dim_)) # n,head_n,hidden_dim
        k=np.reshape(k,(n,head_n,hidden_dim_))
        v=np.reshape(v,(n,head_n,hidden_dim_))
        q=np.transpose(q,(1,0,2)) # head_n,n,hidden_dim_
        k=np.transpose(k,(1,0,2)) # head_n,n,hidden_dim_
        v=np.transpose(v,(1,0,2)) # head_n,n,hidden_dim_
        A=q@np.transpose(k,(0,2,1))              #head_n,n,hidden_dim_ head_n,hidden_dim_,n
        A=A/np.sqrt(hidden_dim_)
        A_hat=self.softmax(A)  #head_n,n,n
        output=A_hat@v  # head_n,n,hidden_dim_
        output=np.transpose(output,(1,0,2)) # n,head_n,hidden_dim_
        output=np.reshape(output,(n,hidden_dim))
        print(output.shape)
        return output

####### 利用torch重新写一个######
'''
https://zhuanlan.zhihu.com/p/688109742
'''
import torch
import math
from torch import nn as nn
class self_attention_torch(nn.Module):
    def __init__(self,input_dim,hidden_dim):
        super().__init__()
        self.d=hidden_dim
        self.n=input_dim
        self.scale=1/math.sqrt(hidden_dim)
        self.linear_q = nn.Linear(input_dim, hidden_dim)
        self.linear_k = nn.Linear(input_dim, hidden_dim)
        self.linear_v = nn.Linear(input_dim, hidden_dim)

    def forward(self, x):
        batch_size, seq_len, input_dim = x.shape
        assert input_dim == self.n
        q = self.linear_q(x)
        k = self.linear_k(x)
        v = self.linear_v(x)
        # q n*d × d*n=n*n
        atten = torch.matmul(q, k.transpose(1, 2)) * self.scale
        atten = torch.softmax(atten, dim=-1)
        x = torch.matmul(atten, v)
        return x,atten
class multiHead_selfattention(nn.Module):
    def __init__(self,input_dim,num_heads,hidden_dim):
        super().__init__()
        assert hidden_dim%num_heads==0
        hidden_dim_=hidden_dim//num_heads
        self.n_head=num_heads
        self.n=input_dim
        self.d1=hidden_dim_
        self.d=hidden_dim
        self.q=nn.Linear(input_dim,hidden_dim)
        self.k=nn.Linear(input_dim,hidden_dim)
        self.v=nn.Linear(input_dim,hidden_dim)
        self.output_liner=nn.Linear(input_dim,hidden_dim)
        self.scale=1/math.sqrt(hidden_dim_)
    def forward(self,x):
        batch_size,seq_len,input_dim=x.size()
        assert input_dim== self.n
        # batch,seq_len,num_head,d1->batch,num_head,seq_len,d1
        q = self.q(x).reshape(batch_size, seq_len, self.n_head, self.d1).transpose(1, 2)
        k = self.q(x).reshape(batch_size, seq_len, self.n_head, self.d1).transpose(1, 2)
        v = self.q(x).reshape(batch_size, seq_len, self.n_head, self.d1).transpose(1, 2)
        #print(q.size())
        # q batch,num_head,seq_len,d1  batch,num_head,d1,seq_len-> batch,num_head,seq_len,seq_len
        atten = torch.matmul(q, k.transpose(2, 3)) * self.scale
        atten = torch.softmax(atten, dim=-1)
        # batch,num_head,seq_len,seq_len × batch,num_head,seq_len,d1=batch,num_head,seq_len,d1
        x = torch.matmul(atten, v)
        # 将其变为 batch,seq_len,num_head,d1-> batch,seq_len,
        x = x.transpose(1, 2).reshape(batch_size, seq_len, self.d)
        return x, atten
if __name__=="__main__":
    solution1=attention_np()
    if False:
        # 测试softmax
        x=np.array([1,2,3,4])
        x_=solution1.softmax(x)
        print(x_)
    if False:
        # 测试多头注意力机制
        m=16  #句子的长度
        n=64  # 词向量的维度
        hidden_dim=128 #self-attention的隐层的维度
        input_x=np.random.rand(m,n)
        # 输入为16*64，经过self-attention变为16*128
        # wq,wk,wv分别为64*128 # attention的隐层的维度
        # 最后得到的 k q v以及输出值均为 16*128的句子
        solution1.self_attention(input_x,hidden_dim)
    if False:
        m=16
        n=64
        hidden_dim=128
        x=np.random.rand(m,n)
        res=solution1.multi_head_attention(x,hidden_dim)
    if True:

        x = torch.rand(16, 100, 64) # batch,seq_len,hidden_dim
        n=64
        d=128
        self_attention = self_attention_torch(64,128)
        x, atten = self_attention(x)
        print("x.shape:", x.shape)
        print("atten.shape:", atten.shape)
    if True:
        x = torch.rand(16, 100, 64)  # batch,seq_len,hidden_dim
        n = 64
        d = 128
        multi_attention=multiHead_selfattention(64,4,128)
        x,atten=multi_attention(x)
        print("x.shape:", x.shape)
        print("atten.shape:", atten.shape)