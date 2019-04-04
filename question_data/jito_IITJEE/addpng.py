import pandas as pd


df = pd.read_csv('physics_class_12_1.csv')

link = df['QuestionLink']
usedFor = df['usedFor']
sectionType = df['sectionType']
lang = df['lang']
optionA = df['optionA']
optionB = df['optionB']
optionC = df['optionC']
optionD = df['optionD']
source = df['source']
correct = df['correct']
new_links = []
for i in link:
    new_link = link+'.png'
    new_links.append(new_link)


new_sheet = {'QuestionLink':new_links,
             'usedFor':usedFor,
             'sectionType':sectionType,
             'lang':lang,
             'optionA':optionA,
             'optionB':optionA,
             'optionC':optionC,
             'optionD':optionD,
             'correct':correct,
             'source':source}
                


gf = pd.DataFrame(new_sheet)
gf.to_csv('physics_class12.csv')
