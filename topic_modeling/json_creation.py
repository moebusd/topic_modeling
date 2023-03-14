def json_creation(stoplist_path, working_folder, source, Save = False):
    import os
    import re
    import json
    from topic_modeling.topic_modeling import preprocess_outstr

    dic = {}

    for folder in source:
        for file in os.listdir(folder):
            print(file)
            try:
                text = open(folder + '\\' + file, 'r', encoding='UTF-8-sig').read()
            except UnicodeDecodeError:
                try:
                    text = open(folder + '\\' + file, 'r', encoding='UTF-8').read()
                except UnicodeDecodeError:
                    try:
                        text = open(folder + '\\' + file, 'r', encoding='UTF-16-le').read()
                    except UnicodeDecodeError:
                        try:
                            text = open(folder + '\\' + file, 'r', encoding='UTF-16-be').read()
                        except UnicodeDecodeError:
                            text = open(folder + '\\' + file, 'r', encoding='ANSI').read()
                            text = text.encode('UTF-8')
                            text = text.decode('UTF-8', 'ignore')

            # Dieser Teil ist für später irrelevant. Ist nur für meine eigene Textstruktur wichtig.
            text = re.sub(r"\*(.*?)\*[ ]", "", text)
            text = re.sub(r"\((.*?)\)[ ]", "", text)
            text = re.sub(r"\((.*?)\)", "", text)
            text = re.sub(r"(.*\n.*\n.*\n.*\n.*\n)(\+\+)", "", text)
            text = re.sub(r"^[ ]", "", text)

            text_unified = text.replace('!', '.').replace('?', '.').replace(';', '.').replace('...,', ',').replace(
                '..,', ',').replace('"', '').replace("'", '').replace("\n", ' ').replace(" - ", " ")
            text_split = text_unified.split('. ')

            id = file.split(".")[0]
            if file[:3] not in dic:
                dic[file[:3]] = {}
            dic[file[:3]][id] = {}
            dic[file[:3]][id]["sent"] = {}
            sent_number = 1
            for sent in text_split:
                dic[file[:3]][id]["sent"][sent_number] = {}
                dic[file[:3]][id]["sent"][sent_number]["raw"] = sent
                sent_number += 1

    # Die Einträge für jeden einzelnen Satz werden um weitere Einträge ergänzt.

    for archiv in dic:
        for id in dic[archiv]:
            for sent_number in dic[archiv][id]["sent"]:
                dic[archiv][id]["sent"][sent_number]["time"] = {}
                dic[archiv][id]["sent"][sent_number]["band"] = {}
                dic[archiv][id]["sent"][sent_number]["cleaned"] = {}
                dic[archiv][id]["sent"][sent_number]["speaker"] = {}
                dic[archiv][id]["sent"][sent_number]["chunk"] = {}

    stoplist = open(stoplist_path, encoding='UTF-16', mode='r').read().split()

    # Stopwords werden entfernt und unter "cleaned" im dic eingefügt.

    def remove_stopwords_by_list(data, stoplist):
        data_out = [[word for word in line if word not in stoplist] for line in data]
        return data_out

    for archiv in dic:
        for ID in dic[archiv]:
            for nr in dic[archiv][ID]["sent"]:
                text = dic[archiv][ID]["sent"][nr]["raw"]
                pre_line = preprocess_outstr(text)
                line = pre_line.split(" ")
                data_out = [word for word in line if word not in stoplist]
                data_out2 = [word for word in data_out if len(word) > 2]
                dic[archiv][ID]["sent"][nr]["cleaned"] = data_out2

    top_dic = {}

    top_dic["korpus"] = dic
    top_dic["weight"] = {}
    top_dic["words"] = {}
    top_dic["settings"] = {}


    top_dic = json.dumps(top_dic)

    return top_dic
