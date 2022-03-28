import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import os
import re

CANDIDATE = {
    'Macron':['emmanuel macron', 'emmanuelmacron', 'macron'],
    'Arthaud':['nathalie arthaud', 'nathaliearthaud', 'arthaud'],
    'Roussel':['fabien roussel', 'fabienroussel', 'roussel'],
    'Lassalle':['jean lassalle', 'jeanlassalle', 'lassalle'],
    'Le Pen':['marine le pen', 'marinelepen', 'le pen', 'lepen'],
    'Zemmour':['éric zemmour', 'ériczemmour', 'eric zemmour', 'ericzemmour', 'zemmour'],
    'Melenchon':['jean-luc mélenchon', 'jean-luc melenchon', 'jeanlucmélenchon',
                 'jeanlucmelenchon', 'melenchon', 'mélenchon'],
    'Hidalgo':['anne hidalgo', 'annehidalgo', 'hidalgo'],
    'Jadot':['yannick jadot', 'yannickjadot', 'jadot'],
    'Pecresse':['valérie pécresse', 'valériepécresse', 'valerie pecresse', 'valeriepecresse',
                'pécresse', 'pecresse'],
    'Poutou':['philippe poutou', 'philippepoutou', 'poutou'],
    'Dupont_Aignan':['nicolas dupont-aignan', 'nicolasdupont-aignan', 'nicolasdupontaignan',
                     'nicolas dupont', 'nicolas aignan', 'dupont-aignan', 'aignan']
}




def data_processing(raw_df):

    # ----- Content Extractions:
    raw_df['content'] = raw_df['content'] + ' '
    raw_df['content'] = raw_df['content'].str.replace('\n', ' ')
    raw_df['content'] = raw_df['content'].str.replace('?', ' ', regex=False)
    raw_df['content'] = raw_df['content'].str.replace(',', ' ')
    raw_df['content'] = raw_df['content'].str.replace('!', ' ')
    raw_df['content'] = raw_df['content'].str.replace('.', ' ', regex=False)
    raw_df['tags'] = raw_df['content'].str.findall(r'@(.*?) ')
    raw_df['htags'] = raw_df['content'].str.findall(r'#(.*?) ')

    # ----- Dates Manipulations:
    raw_df['day'] = raw_df['date'].str[0:10]
    raw_df['date'] = pd.to_datetime(raw_df['date'])
    raw_df['hour'] = raw_df['date'].dt.hour
    raw_df['account_creation_date'] = pd.to_datetime(raw_df['account_creation_date'])
    raw_df['account_history'] = (raw_df['date'] - raw_df['account_creation_date']).dt.days

    return raw_df



def update_data(max_date, list_ids):


    today = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    last_date = max_date
    query = '#presidentielles2022 since:{} until:{}'.format(last_date, today)
    items = sntwitter.TwitterSearchScraper(query).get_items()
    tweets_list = []
    for i,tweet in enumerate(items):
        tweets_list.append([tweet.id, tweet.date,
                            tweet.replyCount, tweet.retweetCount,
                            tweet.likeCount, tweet.quoteCount, tweet.source,
                            tweet.place,
                            tweet.hashtags, tweet.cashtags,
                            tweet.content, tweet.user.username,
                            tweet.user.created, tweet.user.followersCount,
                            tweet.user.friendsCount, tweet.user.statusesCount])

    tweets_df = pd.DataFrame(tweets_list, columns=['tweet_id', 'date', 'n_reply',
                                                   'n_retweet', 'n_like', 'n_quote',
                                                   'source', 'place', 'hashtags',
                                                   'cashtags', 'content', 'username',
                                                    'account_creation_date',
                                                   'n_followers', 'n_friends',
                                                   'n_status'])

    tweets_df = tweets_df[~tweets_df['tweet_id'].isin(list_ids)]
    tweets_df.to_csv('datasets/tweets_prez.csv', mode='a',
                     header=not os.path.exists('datasets/tweets_prez.csv'),
                     index=False, encoding='utf-8-sig')
    return 'Added {} entries since {} '.format(len(tweets_df), last_date)


def count_htags(raw_df):
    full_hashtags = raw_df['htags'].sum()
    full_hashtags = Counter(full_hashtags)
    df = {}
    df['hashtag'], df['counts'] = [], []
    for e in full_hashtags.keys():
        if e not in ['presidentielles2022', 'presidentielle2022',
                     'Presidentielle2022', 'Presidentielles2022',
                     'Présidentielle2022', 'France', 'Presidentielle',
                     'Présidentielles2022', 'Elections2022', 'Elysee2022',
                     'presidentielle']:
            df['hashtag'].append(e)
            df['counts'].append(full_hashtags[e])
    df = pd.DataFrame(df).sort_values(by='counts', ascending=False)
    return df.reset_index(drop=True)

def count_tags(raw_df):
    full_tags = raw_df['tags'].sum()
    full_tags = Counter(full_tags)
    df = {}
    df['tag'], df['counts'] = [], []
    for e in full_tags.keys():
        df['tag'].append(e)
        df['counts'].append(full_tags[e])
    df = pd.DataFrame(df).sort_values(by='counts', ascending=False)
    return df.reset_index(drop=True)

def summary(raw_df, on='number', by_cols='day'):
    if on=='number':
        df = raw_df.groupby(by=by_cols, as_index=False)['tweet_id'].nunique()
    elif on=='account':
        df = raw_df.groupby(by=by_cols, as_index=False)['username'].nunique()
    else:
        df = raw_df.groupby(by=by_cols, as_index=False)[on].sum()
    return df

def is_candidate_summary(raw_df, candidate, on='number', by_cols='day'):
    df = raw_df.copy()
    df_result = pd.DataFrame()
    if candidate=='All':
        for k in CANDIDATE.keys():
            df_result = pd.concat([df_result,is_candidate_summary(df, k, on=on, by_cols=by_cols)], ignore_index=True)
    else:
        df['found'] = 0
        for elt in CANDIDATE[candidate]:
            df['found'] += df['content'].str.lower().str.contains(elt, regex=False).astype('int')
        df = df[df['found']>0]
        df = summary(df, on=on, by_cols=by_cols)
        df['Candidat'] = candidate
        df_result = df
    return df_result


def candiate_filter(raw_df, candidate):
    df = raw_df.copy()
    df['found'] = 0
    for elt in CANDIDATE[candidate]:
        df['found'] += df['content'].str.lower().str.contains(elt, regex=False).astype('int')
    return df[df['found']>0].reset_index(drop=True)


def account_candidate_hist(raw_df, candidate):
    df = raw_df.copy()
    df_result = pd.DataFrame()
    if candidate=='All':
        for k in CANDIDATE.keys():
            df_result = pd.concat([df_result, account_candidate_hist(df, k)], ignore_index=True)
    else:
        df['found'] = 0
        for elt in CANDIDATE[candidate]:
            df['found'] += df['content'].str.lower().str.contains(elt, regex=False).astype('int')
        df = df[df['found']>0]
        df['Candidat'] = candidate
        df_result = df[['Candidat', 'account_history']]
    return df_result

dataframe = pd.read_csv('datasets/tweets_prez.csv', encoding='utf-8-sig')
dataframe = data_processing(dataframe)

def data_refresh(dataframe):
    dataframe = pd.read_csv('datasets/tweets_prez.csv', encoding='utf-8-sig')
    dataframe = data_processing(dataframe)
    return dataframe
