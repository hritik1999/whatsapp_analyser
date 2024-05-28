import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urlextract import URLExtract
import re
from collections import Counter
from wordcloud import WordCloud
import io
import base64

def  data_organize_android(data):
  pattern = re.compile(r'\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2}[AP]M\]')
  messages = re.split(pattern, data)[1:]


  #extract all dates
  dates = re.findall(pattern, data)

  #create dataframe
  df = pd.DataFrame({'user_message': messages, 'message_date': dates}).reset_index()
  # convert message_date type
  df['message_date'] = pd.to_datetime(dates, format="[%d/%m/%y, %I:%M:%S%p]")
  df.rename(columns={'message_date': 'date'}, inplace=True)
  df.head(10)
  df=df[~(df['user_message'].astype(str).str.contains("Messages and calls are end-to-end encrypted.|created this group|pinned a message| changed the group name|changed the group description|joined using this group's"))]
  df['User']=[(x.split(":")[0]) for x in df['user_message']]
  pattern = r'\b\w +added \w*\b'
  df = df[~(df['user_message'].astype(str).str.contains(pattern,case=False, regex=True))]
  df['message']=[(x.split(":")[1]).strip() for x in df['user_message']]



  return df

def  data_organize_ios(data):
  pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s')
  messages = re.split(pattern, data)[1:]


  #extract all dates
  dates = re.findall(pattern, data)

  #create dataframe
  df = pd.DataFrame({'user_message': messages, 'message_date': dates}).reset_index()
  # convert message_date type
  df['message_date'] = pd.to_datetime(dates, format='%m/%d/%y, %H:%M - ')
  df.rename(columns={'message_date': 'date'}, inplace=True)
  df.head(10)
  df=df[~(df['user_message'].astype(str).str.contains("Messages and calls are end-to-end encrypted.|created group|pinned a message| changed group name|changed the group description|joined using this group's"))]
  df['User']=[(x.split(":")[0]) for x in df['user_message']]
  pattern = r'\b\w +added \w*\b'
  df = df[~(df['user_message'].astype(str).str.contains(pattern,case=False, regex=True))]
  df['message']=[(x.split(":")[1]).strip() for x in df['user_message']]



  return df

def last_days(df):
  df['Day'] = df['date'].dt.date
  df['Week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)


  # Most active days
  most_active_days = pd.DataFrame(df['Day'].value_counts()[:30]).reset_index()
  most_active_days=most_active_days.sort_values(by='Day', ascending=True)
  print("Most Active Days:")

  plt.figure(figsize=(12, 6))
  plt.plot(most_active_days['Day'],most_active_days['count'])
  plt.xlabel('Day')
  plt.ylabel('Number of Messages')
  plt.xticks(rotation=90)

  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

    # Convert buffer to base64 string
  img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
  buffer.close()
  return {'last_days':img_base64}

def NO_OF_MSG(df):
    no_of_msg=[]
    user_message_counts = df['User'].value_counts().reset_index()
    user_message_counts.columns = ['User', 'message_count']
    user_message_counts = user_message_counts.sort_values(by='message_count', ascending=False)
    top_20_users = user_message_counts.head(20)

# Get the list of top 20 users
    top_20_user_list = top_20_users['User'].tolist()

    # Step 4: Filter the original DataFrame to get the data for the top 20 users
    top_20_users_data = df[df['User'].isin(top_20_user_list)]
    for u in top_20_users_data.User.unique():
        df1=df[df['User']==u]
        no_of_msg.append(len(df1['message']))
    # plt.bar(top_20_users_data.User.unique(),no_of_msg)
    plt.figure(figsize=(12, 6))
    sns.barplot( x=list(no_of_msg),y=list(top_20_users_data.User.unique()),  color='deeppink')
    plt.ylabel('user')
    plt.xlabel('Number of Messages')
    plt.xticks(rotation=90)
    plt.title("No of messages of the most active users")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert buffer to base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return {'no_of_msg':img_base64}

def NO_OF_words(df):
    no_of_words=[]

    user_message_counts = df['User'].value_counts().reset_index()
    user_message_counts.columns = ['User', 'message_count']
    user_message_counts = user_message_counts.sort_values(by='message_count', ascending=False)
    top_20_users = user_message_counts.head(20)

# Get the list of top 20 users
    top_20_user_list = top_20_users['User'].tolist()

    # Step 4: Filter the original DataFrame to get the data for the top 20 users
    top_20_users_data = df[df['User'].isin(top_20_user_list)]
    for u in top_20_users_data.User.unique():
        df1= top_20_users_data[ top_20_users_data['User']==u]
        text=''
        for x in df1['message']:
            text+=x
        no_of_words.append(len(text.split()))
    plt.figure(figsize=(12, 6))
    sns.barplot( x=list(no_of_words),y=list(top_20_users_data.User.unique()),  color='red')
    plt.ylabel('user')
    plt.xlabel('Number of Words')
    plt.xticks(rotation=90)
    plt.title("No of words of the most active users")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert buffer to base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return {'no_of_words':img_base64}

def links(df):


    extract = URLExtract()
    df2=pd.DataFrame({'User':df.User.unique(),'count':  None})


    for i,u in enumerate(df2.User):
        links = []
        df1= df[ df['User']==u]
        text=''
        for message in df1['user_message']:
          links.extend(extract.find_urls(message))
        df2['count'][i]=(len(links))

    df2=df2.sort_values(by='count', ascending=False)
    plt.figure(figsize=(12, 6))
    plt.bar(df2.User[:20],df2['count'][:20],  color='darkturquoise')
    plt.ylabel('user')
    plt.xlabel('Number of Links')
    plt.xticks(rotation=90)
    plt.title("No of links sent by the users")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert buffer to base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return {'no_of_links':img_base64}

def busy_day(df):

    df['day_of_week'] =[x.strftime('%A') for  x in df['date']]

    # Calculate the count of occurrences of each day
    busy_day = (pd.DataFrame(df['day_of_week'].value_counts().reset_index()))
    # Define the order of days of the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Convert 'index' to categorical with the desired order
    plt.figure(figsize=(12, 6))
    plt.bar(busy_day['day_of_week'], busy_day['count'], color='purple')
    plt.title("Distribution of messages in a week")
    plt.xticks(rotation='vertical')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert buffer to base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return {'busy_day':img_base64}

def busy_month(df):

    df['month'] =[x.strftime('%B') for  x in df['date']]

    busy_month = (pd.DataFrame(df['month'].value_counts().reset_index()))
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    busy_month.columns = ['month', 'count']

# Sort the DataFrame by month names
    # busy_month = busy_month.sort_values(by='month', key=lambda x: pd.Categorical(x['month'], categories=month_order, ordered=True))

    plt.figure(figsize=(12, 6))
    plt.bar(busy_month['month'], busy_month['count'], color='purple')
    plt.title("Distribution of messages in a yr")
    plt.xticks(rotation='vertical')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert buffer to base64 string
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return {'busy_month':img_base64}

def word_cloud(df):
  user_message_counts = df['User'].value_counts().reset_index()
  user_message_counts.columns = ['User', 'message_count']
  user_message_counts = user_message_counts.sort_values(by='message_count', ascending=False)
  top_20_users = user_message_counts.head(20)
  top_20_user_list = top_20_users['User'].tolist()
  top_20_users_data = df[df['User'].isin(top_20_user_list)]
  combined_messages = ' '.join(top_20_users_data['message'])
  words = re.findall(r'\w+', combined_messages.lower())
  word_counts = Counter(words)
  top_words = word_counts.most_common(20)

  # Display the top words

  # Step 2: Generate the Word Cloud
  wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_messages)

  # Display the Word Cloud
  buffer = io.BytesIO()
  plt.figure(figsize=(10, 5))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')


  plt.savefig(buffer, format='png')
  buffer.seek(0)

    # Convert buffer to base64 string
  img_base642 = base64.b64encode(buffer.read()).decode('utf-8')
  buffer.close()



  return {'word_cloud':img_base642}

def freq_words(df):
  user_message_counts = df['User'].value_counts().reset_index()
  user_message_counts.columns = ['User', 'message_count']
  user_message_counts = user_message_counts.sort_values(by='message_count', ascending=False)
  top_20_users = user_message_counts.head(20)
  top_20_user_list = top_20_users['User'].tolist()
  top_20_users_data = df[df['User'].isin(top_20_user_list)]
  combined_messages = ' '.join(top_20_users_data['message'])
  words = re.findall(r'\w+', combined_messages.lower())
  word_counts = Counter(words)
  top_words = word_counts.most_common(20)
  labels = [pair[0] for pair in top_words]
  values = [pair[1] for pair in top_words]

  plt.figure(figsize=(12, 6))
  plt.bar(labels, values)
  plt.xlabel('')
  plt.ylabel('count')
  plt.title('Bar Plot most frequent words')
  plt.xticks(rotation='vertical')

  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

    # Convert buffer to base64 string
  img_base641 = base64.b64encode(buffer.read()).decode('utf-8')
  buffer.close()
  return {'freq_words':img_base641}

def top_word_per_user(df):

    user_message_counts = df['User'].value_counts().reset_index()
    user_message_counts.columns = ['User', 'message_count']
    user_message_counts = user_message_counts.sort_values(by='message_count', ascending=False)
    top_20_users = user_message_counts.head(20)
    top_20_user_list = top_20_users['User'].tolist()
    top_20_users_data = df[df['User'].isin(top_20_user_list)]
    top_words_per_user = {}
    grouped = top_20_users_data.groupby('User')
    for user in top_20_user_list:
    # Combine messages for the current user
      combined_messages = ' '.join(df['message'])
      words = re.findall(r'\w+', combined_messages.lower())
      word_counts = Counter(words)
      top_words = word_counts.most_common(20)
      top_words_per_user['user'] = top_words
# Display the top words for each user
    for user, top_words in top_words_per_user.items():
      print(f'\nTop words for {user}:')
      for word, count in top_words:
          print(f'{word}: {count}')
    print()


