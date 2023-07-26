from tqdm import tqdm
import pandas as pd


def get_dtm_array(df, tagger, vectorizer, sentence_num=None, words_list=None):
    for senetence in tqdm(df['content'][:sentence_num], desc='진행도'):
        words_list.append(' '.join(tagger.nouns(senetence)))
        dtm_array = vectorizer.fit_transform(words_list).toarray()
        features = vectorizer.get_feature_names_out()
    return dtm_array, features

def get_words_freq(df, features):
    df_list = []
    for i in range(df.shape[0]):
        df_list.append((features[i], df.iloc[:,i].sum()))

    freq_df = pd.DataFrame(df_list, columns=['words', 'freq'])
    freq_df.sort_values(by='freq', ascending=False, inplace=True)
    return freq_df

