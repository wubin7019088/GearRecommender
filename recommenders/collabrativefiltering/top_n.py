#-*- coding: UTF-8 -*-
import pickle
import numpy as np
import logging
import logging.handlers
from evaluation.evaluation import *


class TopN():
    def __init__(self, path, parameters):
        self.user_index_dict = pickle.load(open(path[:-1] + 'uiDict', 'rb'))
        self.item_index_dict = pickle.load(open(path[:-1] + 'iiDict', 'rb'))
        self.train_data = pd.read_csv(path + 'eccTrainData')
        self.user_purchased_item_dict = pickle.load(open(path + 'upiTrainDict', 'rb'))
        self.item_purchased_user_dict = pickle.load(open(path + 'ipuTrainDict', 'rb'))

        self.true_rating_dict = pickle.load(open(path + 'uiraTestDict', 'rb'))
        self.true_purchased_dict = pickle.load(open(path + 'upiTestDict', 'rb'))

        self.user_count = len(self.user_index_dict.keys())
        self.item_count = len(self.item_index_dict.keys())


        self.n = parameters['n']
        self.recommend_new = parameters['recommend_new']

        logging.config.fileConfig('log_conf')
        self.topn_logger = logging.getLogger('topn')
        self.topn_logger.info(''.join((' TopN:', str(self.n))))

    def fit(self):
        vs = [len(i) for i in self.item_purchased_user_dict.values()]
        ks = self.item_purchased_user_dict.keys()
        index = np.argsort(np.array(vs))[-1:-self.n-1:-1]
        self.popItems = np.array(ks)[index]

    def save(self):
        t = pd.DataFrame(self.user_recommend)
        t.to_csv('../results/top_n_user_recommend')


    def predict(self, u, item):
        if item in self.popItems:
            return 5
        else:
            return 1

    def recommend(self, u):
        if self.recommend_new == 0:
            candidate = np.array([self.predict(u, i) for i in range(self.item_count)])
        else:
            candidate = np.array([self.predict(u, i) for i in range(self.item_count) if i not in self.user_purchased_item_dict[u]])

        result = np.argsort(candidate)[-1:-self.n-1:-1]
        return result

    def score(self, log):
        e = Eval()
        predict_rating_list = []
        true_rating_list = []
        predict_top_n = []
        true_purchased = []
        self.user_recommend = []

        for (ui, rating) in self.true_rating_dict.items():
            user = int(ui.split('##')[0])
            item = int(ui.split('##')[1])
            predict_rating_list.append(self.predict(user, item))
            true_rating_list.append(rating)

        for (u, items) in self.true_purchased_dict.items():
            recommended_item = self.recommend(u)
            predict_top_n.append(recommended_item)
            self.user_recommend.append([u, recommended_item])
            true_purchased.append(items)


        rmse = e.RMSE(predict_rating_list, true_rating_list)
        f1, hit, ndcg, p, r, f = e.evalAll(predict_top_n, true_purchased)
        self.topn_logger.info(''.join((str(f1), str(hit), str(ndcg), str(p), str(r), str(f))))
        return [rmse, f1, ndcg, p, r, f]








