
def chunking(top_dic, chunk_setting = 50, ):
    import json
    with open(top_dic) as f:
        top_dic = json.load(f)

    for archiv in top_dic["korpus"]:
        for ID in top_dic["korpus"][archiv]:
            chunk_count = 1
            chunk_data = []
            for nr in range(1, (len(top_dic["korpus"][archiv][ID]["sent"]) + 1)):
                chunk_data += top_dic["korpus"][archiv][ID]["sent"][str(nr)]["cleaned"]
                top_dic["korpus"][archiv][ID]["sent"][str(nr)]["chunk"] = chunk_count
                if len(chunk_data) > chunk_setting:
                    chunk_count += 1
                    chunk_data = []

    top_dic["settings"].update({"chunks": chunk_setting})