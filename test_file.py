import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
cache = {}

def sem_text_sim(t1, t2):
    """optimized function of bert_cosine. uses a cache to safe time when calculating duplicate similarities
    reason: for longer inputs bert can be very compute intensive. adding a cache can reduce minutes to seconds
    """

    sentences = [t1, t2]

    def encode(value):
        cache_hit = cache.get(value, None)
        if cache_hit is not None:
            return cache_hit
        else:
            embedding = model.encode(value, convert_to_tensor=True)
            cache[value] = embedding
            return embedding

    embedding_1 = encode(sentences[0])
    embedding_2 = encode(sentences[1])
    score = util.pytorch_cos_sim(embedding_1, embedding_2)
    score = score.tolist()
    return score[0][0]


#open json file with all working items
#TODO: to be replaced with the polarion get request!
# (a) get tokem
# (b) make a get request to ..{project_id}/working_items

with open('all_working_items.json', 'r') as file:
    data = json.load(file)
#    print(json.dumps(data['data'][0], indent=4))

wi_types = []

for d in data['data']:
    print("------------------: ", json.dumps(d, indent=4))
    wi_type = d['attributes']['type']
    if wi_type not in wi_types:
        wi_types.append(wi_type)
print(wi_types)



test_type = "stakeholder"



def my_filtering_function(wi,current_type):
    if wi['attributes']['type'] == current_type:
        return {'id':wi['attributes']['id'],'title':wi['attributes']['title']}
    else:
        False

filtered_wis = [my_filtering_function(wi,test_type) for wi in data['data'] if my_filtering_function(wi,test_type) is not None]
print(filtered_wis)

import itertools
for x,y in itertools.combinations(filtered_wis, 2):
    print(x,y)

# for fwi in filtered_wis:
#     title1 = fwi['title']
#     for afwi in filtered_wis:
#         title2 = afwi['title']
#         if title1 != title2:
#             score = sem_text_sim(title1,title2)
#             #print(score)
#             if score >= 0.7:
#                 print(score, title1, title2)
#
#

