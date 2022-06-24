import flask
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/tmdb.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]


def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['runtime'].iloc[movie_indices]
    pop = df2['popularity'].iloc[movie_indices]
    vot = df2['vote_average'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title', 'Runtime','Popularity','vote'])
    return_df['Title'] = tit
    return_df['Runtime'] = dat
    return_df['Popularity'] = pop
    return_df['vote'] = vot
    return return_df
print
(df2)

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m_name not in all_titles:
            return (flask.render_template('nomatch.html', name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            runtime = []
            popularity =[]
            vote_average = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                runtime.append(result_final.iloc[i][1])
                popularity.append(result_final.iloc[i][2])
                vote_average.append(result_final.iloc[i][3])
            return flask.render_template('match.html', movie_names=names, movie_runtime=runtime, search_name=m_name, movie_popularity=popularity, movie_vote=vote_average)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')