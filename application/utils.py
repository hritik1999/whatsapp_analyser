import json
import os
import re
from datetime import datetime
from collections import defaultdict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv , find_dotenv

_ = load_dotenv(find_dotenv())
os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

def text_chunking(file):
    android_date_pattern = re.compile(r'^\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} - ')
    ios_date_pattern = re.compile(r'^\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}\u202f[APM]{2}\]')

    # with open(file, 'r') as f:
    #     file_content = f.read()

    user_messages = defaultdict(list)
    software_type = ""
    texts = file.split('\n')


    for line in texts:
        if android_date_pattern.match(line):
            software_type = "android"
            break
        elif ios_date_pattern.match(line):
            software_type = "ios"
            break


    if software_type == "android":
        for line in texts:
            try:
                if android_date_pattern.match(line):
                    date = line.split(' - ', 1)[0].strip()
                    user_message = line.split(' - ', 1)[1].strip()
                    user = user_message.split(': ', 1)[0].strip()
                    text = user_message.split(': ', 1)[1].strip() if ': ' in user_message else ""

                    if len(text.split()) > 3 and len(text.split()) < 120:
                        date_obj = datetime.strptime(date, '%m/%d/%y, %H:%M')
                        user_messages[user].append((date_obj, text))
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Exception: {e}")

    elif software_type == "ios":
        for line in texts:
            try:
                if ios_date_pattern.match(line):
                    date_part = line.split(']')[0].strip('[').strip()
                    user_message = line.split(']')[1].strip()
                    user = user_message.split(':', 1)[0].strip('~').strip()
                    text = user_message.split(':', 1)[1].strip() if ':' in user_message else ""

                    if len(text.split()) > 3 and len(text.split()) < 120:
                        date_obj = datetime.strptime(date_part, '%d/%m/%y, %I:%M:%S\u202f%p')
                        user_messages[user].append((date_obj, text))
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Exception: {e}")


    def split_into_chunks(messages, chunk_size=6000):
        words = ' '.join(messages).split()
        for i in range(0, len(words), chunk_size):
            yield ' '.join(words[i:i + chunk_size])


    user_chunks = {}
    month_chunks = {}
    for user, messages in user_messages.items():
        messages.sort()
        texts = [text for date, text in messages]
        word_count = sum(len(text.split()) for text in texts)

        if word_count > 10000:
            month_messages = defaultdict(list)
            for date, text in messages:
                month_key = date.strftime('%Y-%m')
                month_messages[month_key].append(text)
            month_chunks[user] = {month: list(split_into_chunks(texts)) for month, texts in month_messages.items()}
        else:
            chunks = list(split_into_chunks(texts))
            if sum(len(chunk.split()) for chunk in chunks) >= 500:
                user_chunks[user] = chunks

    result = {"user_chunks": user_chunks}
    if month_chunks:
        result["month_chunks"] = month_chunks

    return json.dumps(result, indent=4)

def personality_analyser(text_chunks):
  
  text_chunks = json.loads(text_chunks)
  llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
  user_summary_analysis = {}
  user_analysis = {}

  if 'user_chunks' in text_chunks.keys():

    analysis_template = ChatPromptTemplate.from_messages(
    [
        ('system',"You are a highly skilled personality analyst AI, trained to interpret text in multiple languages, including English, Hindi, and others, to deduce personality traits. You will receive WhatsApp group chat messages of a user, and your task is to analyze these messages to provide a comprehensive overview of the user's personality,interest,dislikes,quirks or any traits that you can discern from the give messages."),
       ('user', "Here are the WhatsApp group chat messages of a user: {messages}")
    ]
    )
    analyst_chain = ({"messages": RunnablePassthrough()} |analysis_template | llm)

    for user,text in text_chunks['user_chunks'].items():
      analysis = analyst_chain.invoke(text).content
      user_analysis[user] = analysis
  
  if 'month_chunks' in text_chunks.keys():

    summarization_template = ChatPromptTemplate.from_messages(
    [
        ('system', "You are a highly skilled summarizer AI, trained to condense large volumes of text data into concise summaries. You will receive WhatsApp group chat messages from a user, and your task is to provide a monthly summary of these messages. The summaries should capture the main topics, events, and any notable interactions, with a focus on aspects that reveal the user's personality, interests, dislikes, and quirks."),
        ('user', "Here are the WhatsApp group chat messages for the month: {messages}")
    ]
    )
    summarization_chain = ({"messages": RunnablePassthrough()} |summarization_template | llm)

    analysis_template = ChatPromptTemplate.from_messages(
    [
        ('system', "You are a highly skilled personality analyst AI, trained to interpret text data to deduce personality traits. You will receive monthly summaries of WhatsApp group chat messages of a user, and your task is to analyze these summaries to provide a comprehensive overview of the user's personality, interests, dislikes, quirks, or any traits that you can discern from the given summaries."),
        ('user', "Here are the monthly summaries of the WhatsApp group chat messages: {summaries}")
    ]
    )
    analyst_chain = ({"summaries": RunnablePassthrough()} |analysis_template | llm)

    user_summary = {}

    for user,text in text_chunks['month_chunks'].items():
      if user not in user_summary:
        user_summary[user] = {}
      for month,chat in text.items():
        summary = summarization_chain.invoke(chat).content
        user_summary[user][month] = summary

    for user,text in user_summary.items():
      analysis = analyst_chain.invoke(text).content
      user_summary_analysis[user] = analysis

  result = {'user_analysis':user_analysis}
  if user_summary_analysis:
    result['user_summary_analysis'] = user_summary_analysis
  return json.dumps(result,indent=4)
    