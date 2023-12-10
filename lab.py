import sqlite3
import tokenize_uk
import collections
import pymorphy2
import pymorphy2_dicts_uk
with open("земля.txt", encoding = "utf-8") as data_1:
    lines = data_1.readlines()
modified_lines = []
current_line = ""
for line in lines:
    line = line.rstrip('\n')  
    if line.endswith('-'):
        current_line += line.rstrip('-')
    else:
        current_line += line
        modified_lines.append(current_line)
        current_line = ""
        
text_1 = ' '.join([str(line.rstrip('-\n')) for line in modified_lines])        
splitted_1 = tokenize_uk.tokenize_uk.tokenize_words(text_1)

#функція окириличення
def is_cyrillic(char):
    return 0x0400 <= ord(char) <= 0x04FF

for i in range (1, len(splitted_1)-1):
    #слова через дефіс
    if splitted_1[i] == '-':
        splitted_1[i-1] = splitted_1[i-1]+'-'+splitted_1[i+1] 
        splitted_1[i+1]='0' 
    #скорочення!!!
    if splitted_1[i] == '.' and splitted_1[i+1][0].islower()==True:
        splitted_1[i-1] = splitted_1[i-1]+'.'
    if (splitted_1[i] == '.' 
            and splitted_1[i+1][0].isupper()==True
            and splitted_1[i-1][0].isupper()==True 
            and len(splitted_1[i-1])==1):
        splitted_1[i-1] = splitted_1[i-1]+'.'
splitted_2 = []
for token in splitted_1:
    #фільтр: слова кирилицею, без скорочень
    if (token[0].isalpha()==True and
    is_cyrillic(token[0])==True and
        token[-1].isalpha()==True):
        splitted_2.append(token)
for j in range (len(splitted_2)):
    splitted_2[j]=splitted_2[j].lower()
print(splitted_2)

#ЧАСТИНА 2
dict_of_lists = {}
sample_number = 1
volume = 0
while sample_number < 21:
    dict_of_lists["sample_{0}_list".format(sample_number)] =\
    splitted_2[volume:(volume+1000)]
    volume += 1000
    sample_number +=1

freq_dict={}
def freq(sample_number):
    for i in dict_of_lists.keys():
        if str(sample_number) in i:
            words = dict_of_lists[i]
    counter = collections.Counter(words)
    samp_freq = dict(counter)
    for word_form in samp_freq.keys():
        if word_form not in freq_dict.keys():
            freq_dict[word_form]=[word_form]
            iterator = 1
            while iterator < sample_number:
                freq_dict[word_form].append(0)
                iterator+=1
        freq_dict[word_form].append(samp_freq[word_form])
    for key in freq_dict.keys():
        if key not in words:
            freq_dict[key].append(0)
for i in range (1,21):
    freq(i)
for key in freq_dict.keys():
    freq_dict[key].insert(1, sum(freq_dict[key][1:]))
values_freq = list(freq_dict.values())
values_freq_ordered = sorted(values_freq, key=lambda x: x[1], reverse=True)
print(values_freq_ordered) 

#частини мови
morph = pymorphy2.MorphAnalyzer(lang='uk')
pos_dict={}
for key, value in freq_dict.items():
    tag = morph.parse(key)[0].tag.POS
    if tag == None:
       tag  = 'NOTDEF'
    if tag in pos_dict.keys():
        pos_dict[tag] += [value[1:]]
    else:
        pos_dict[tag] = [value[1:]]
for key, value in pos_dict.items():
    pos_dict[key]=list(map(sum, zip(*value)))
    pos_dict[key].insert(0, key)
values_pos = list(pos_dict.values())
values_pos_ordered = sorted(values_pos, key=lambda x: x[1], reverse=True)
print(values_pos_ordered) 

#леми
lemmas_dict={}
for key, value in freq_dict.items():
    lemma = morph.parse(key)[0].normal_form
    if lemma in lemmas_dict.keys():
        lemmas_dict[lemma] += [value[1:]]
    else:
        lemmas_dict[lemma] = [value[1:]]
for key, value in lemmas_dict.items():
    lemmas_dict[key]=list(map(sum, zip(*value)))
    lemmas_dict[key].insert(0, key)
values_lemmas = list(lemmas_dict.values())
values_lemmas_ordered = sorted(values_lemmas, key=lambda x: x[1], reverse=True)
print(values_lemmas_ordered) 

conn = sqlite3.connect('chesllab100.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS wordforms_freq_zem100
                  (word_form VARCHAR,
                  gen_freq INTEGER, 
                  sample_1 INTEGER, 
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')
c.execute('''CREATE TABLE IF NOT EXISTS pos_freq_zem100
                  (pos VARCHAR,
                  gen_freq INTEGER, 
                  sample_1 INTEGER, 
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')
c.execute('''CREATE TABLE IF NOT EXISTS lemmas_freq_zem100
                  (lemma VARCHAR,
                  gen_freq INTEGER, 
                  sample_1 INTEGER, 
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')
for i in values_freq_ordered:
   c.execute("""INSERT OR IGNORE INTO wordforms_freq_zem100
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

for i in values_pos_ordered:
   c.execute("""INSERT OR IGNORE INTO pos_freq_zem100
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

for i in values_lemmas_ordered:
   c.execute("""INSERT OR IGNORE INTO lemmas_freq_zem100
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()
conn.close()

