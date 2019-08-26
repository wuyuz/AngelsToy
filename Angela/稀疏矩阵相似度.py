import jieba
import gensim  # 机器学习综合库 - NLP 语言模型 相似度算法
from gensim import corpora
from gensim import models
from gensim import similarities

from Config import MongoDB

l1 = list(MongoDB.Content.find({}))
all_doc_list = []  # 问题库的分词列表
for doc in l1:
    doc_list = list(jieba.cut_for_search(doc.get("title")))  # ["你","的","名字","是","什么","是什么"]
    all_doc_list.append(doc_list)
dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
lsi = models.LsiModel(corpus)  # 数据量小时相对精确 大了就非常的不精确 500万内
index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))


def my_gensim_nlp(a):
    doc_test_list = list(jieba.cut_for_search(a))  # ["今年","多","大","了"]
    doc_test_vec = dictionary.doc2bow(doc_test_list)  # 用户输入转换为 corpus 通过 dictionary 转换
    sim = index[lsi[doc_test_vec]]
    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    if cc[0][0] >= 0.55 :
        text = l1[cc[0][0]]
        return text

