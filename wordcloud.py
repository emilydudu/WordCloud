# coding=utf-8

import json
import itertools
from collections import Counter
import math

theses = json.load(open('nthu_thesis20170330.json'))


def keyword_search(keyword):
    return [thesis[0] for thesis in enumerate(theses[1:], 1)
                      if keyword in ' '.join(thesis[1])]


def get_keywords(thesis):
    attrs = dict([p[::-1] for p in enumerate(theses[0])])
    return thesis[attrs[u'系所名稱']].split('\n') + \
           thesis[attrs[u'作者']].split('\n') + \
           thesis[attrs[u'指導教授']].split('\n') + \
           thesis[attrs[u'口試委員']].split('\n') + \
           thesis[attrs[u'中文關鍵詞']].split('\n') + \
           thesis[attrs[u'外文關鍵詞']].split('\n')

            
def word_could(keyword):
    ourput_N = 1000 # output number of top counted keywords
    log_base = 5    # log scale for count scores
 
    doc_idx = keyword_search(keyword)
    relatives = [get_keywords(theses[idx]) for idx in doc_idx]
    relatives = list(itertools.chain.from_iterable(relatives))
    
    counter = Counter()
    counter.update(relatives)
    d = dict([ele for ele in counter.most_common(ourput_N)])
    d.pop(u'', 0)
    d.update({keyword: len(doc_idx)})
    li = [list(ele) for ele in d.iteritems()]
    li = sorted(li, key=lambda x: x[1], reverse=True)
    li = [[ele[0], math.log(ele[1], log_base)]for ele in li]

    return li


def wrapper(keyword):
    result = word_could(keyword)
    result = [[ele[0].encode("utf-8"), ele[1]] for ele in result]
    
    with open('json', 'w') as stream:
        json.dump(result, stream, ensure_ascii=False, encoding="utf-8")
        
    with open('text', 'w') as f:
        for ele in result:
            f.write('{} {}\n'.format(ele[1], ele[0]))

            

if __name__ == '__main__':
    result = word_could(u'石墨')
    result = [[ele[0].encode("utf-8"), ele[1]] for ele in result]
    
    with open('json', 'w') as stream:
        json.dump(result, stream, ensure_ascii=False, encoding="utf-8")
        
    with open('text', 'w') as f:
        for ele in result:
            f.write('{} {}\n'.format(ele[1], ele[0]))
