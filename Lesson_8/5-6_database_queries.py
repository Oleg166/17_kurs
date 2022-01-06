from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['instagram']

question = 'd_k_solution'
# подписчики пользователя
print(f'Подписчики пользователя {question}:')
# items = db.d_k_solution
items = db.d_k_solution
for j in items.find({'usertype': 'follower'}):
    print(j['username'])

print('**************************************************************************************************************')
# на кого подписан пользователь
print(f'На кого подписан пользователь {question}:')
items_2 = db.d_k_solution
for g in items.find({'usertype': 'following'}):
    print(g['username'])

# Вывод данных:
"""
Подписчики пользователя d_k_solution:
masih2873
mr_deepxkkk
nutritionistdrdeepti
neuranewss
**************************************************************************************************************
На кого подписан пользователь d_k_solution:
ai_machine_learning
netajihotel
python.learning
cyber_ev0lution
i.m.pratikdabhi
codingambitions
avixdan
linux.teach
thehardsecurity
programmerplus
hacker__hub
hoshangmotwani
hoshangmotwani
thecybersapiens
programmer.skills
coders.eduyear
the_geekies
niteshsinghhacker
finxterdotcom
logobrainy
python.hunt
webapp_creator
thecodergeek
advancechestclinics
advancechestclinics
itchallenges
digitalsthan
wordpressdotcom
thecodecrumbs
nutritionistdrdeepti
inside.code
thetechunique
h_o_u_s_e_y
i_know_python
icssindia.in
kali_linux_tricks_youtube
thecodingroom
datascienceinfo
philipplackner_official
inside.code
programminghub_app_official
0day_crew
the.website
androidevelopment
learn.machinelearning
neuralnine
theprogrammingexpert
code.know
ml.india
mythbustersworld
__shruti_.singh_
codinganddecoding
brcarcareraipur
"""

