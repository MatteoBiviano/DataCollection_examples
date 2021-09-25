from stackapi import StackAPI

SITE = StackAPI('stackoverflow',   key = "xxxxxxxx" , impose_throttling = True)
#pagination
SITE.page_size = 100
SITE.max_pages = 500
#Crawl question from 01/01/2020 to 01/01/2021
questions = SITE.fetch("questions", filter = '!)rTkr_OQd(vR1j2O5o_q', fromdate =  1577836800, todate = 1609459200, sort = 'votes')
#store
tags_dict = {}
for i in questions["items"]:
    tags = i["tags"]
    for tg in tags:
        if tg not in tags_dict:
            tags_dict[tg] = []
            tags_dict[tg].append(i["question_id"])
        else:
            tags_dict[tg].append(i["question_id"])
info_quest = []
for i in questions["items"]:
    # question tags
    tags = i["tags"] 
    is_answered = i["is_answered"]
    # User name
    display_name = i["owner"]["display_name"]
    # Questions view count
    view_count = i["view_count"]
    # Question down vote
    down_vote_count = i["down_vote_count"]
    # Question up vote
    up_vote_count = i["up_vote_count"]
    # Question answer's count
    answer_count = i["answer_count"]
    # Question score
    score = i["score"]
    # Creation date
    creation_date = i["creation_date"]
    # Question id
    question_id = i["question_id"]
    # Question link
    q_link = i["link"]
    # Question title
    title = i["title"]
    info_quest.append((
            tags,
            display_name,
            title,
            view_count,
            down_vote_count,
            up_vote_count,
            answer_count,
            score,
            creation_date,
            question_id,
            q_link,
            is_answered))
 tags = []
display_name = []
title = []
view_count = []
down_vote_count = []
up_vote_count = []
answer_count = []
score = []
creation_date = []
question_id = []
q_link = []
is_answered = []
for i in info_quest:
    s = ""
    for tt in i[0]:
        s = s + tt + "|-|"
    tags.append(s)
    display_name.append(i[1])
    title.append(i[2])
    view_count.append(i[3])
    down_vote_count.append(i[4])
    up_vote_count.append(i[5])
    answer_count.append(i[6])
    score.append(i[7])
    creation_date.append(i[7])
    question_id.append(i[8])
    q_link.append(i[9])
    is_answered.append(i[10])
df = pd.DataFrame({"Tags": tags,
                   "User_Name": display_name, "Title": title,
                   "View_count": view_count, "Down_vote_count": down_vote_count, "Up_vote_count": up_vote_count,
                   "Answer_count": answer_count, "Score": score, "Creation_date": creation_date, 
                   "Question_id": question_id, "Question_link": q_link, "Is_Answered":is_answered})
df.to_csv("questions_2020_2021.csv", index=False)
