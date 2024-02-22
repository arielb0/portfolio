import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from scull_suite.settings import BASE_DIR

class MovieRecommenderEngine:

    def __init__(self):
        '''
            Initialize a object to recommend movies.
        '''
        # Set datasets columns types. This allow use less memory when load data.

        self.dataset_columns = {
            'tconst': 'object',
            'originalTitle': 'object',
            'isAdult': 'int',
            'startYear': 'int',
            'Action': 'int',
            'Adult': 'int',
            'Adventure': 'int',
            'Animation': 'int',
            'Biography': 'int',
            'Comedy': 'int',
            'Crime': 'int',
            'Documentary': 'int',
            'Drama': 'int',
            'Family': 'int',
            'Fantasy': 'int',
            'Film-Noir': 'int',
            'Game-Show': 'int',
            'History': 'int',
            'Horror': 'int',
            'Music': 'int',
            'Musical': 'int',
            'Mystery': 'int',
            'News': 'int',
            'Reality-TV': 'int',
            'Romance': 'int',
            'Sci-Fi': 'int',
            'Short': 'int',
            'Sport': 'int',
            'Talk-Show': 'int',
            'Thriller': 'int',
            'War': 'int',
            'Western': 'int',
            'movie': 'int',
            'short': 'int',
            'tvEpisode': 'int',
            'tvMiniSeries': 'int',
            'tvMovie': 'int',
            'tvSeries': 'int',
            'tvShort': 'int',
            'tvSpecial': 'int',
            'video': 'int',
            'videoGame': 'int',
        }

        # Load dataset

        print('Loading movie datasets. Please wait..')
        self.dataset = pd.read_csv(BASE_DIR / 'movie/movie_dataset.tar.xz', usecols=self.dataset_columns)
        
        # Set feature columns
        '''

        self.feature_columns = ['isAdult', 'startYear', 'Action', 'Adult', 'Adventure'
                        , 'Animation', 'Biography', 'Comedy', 'Crime'
                        , 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir'
                        , 'Game-Show', 'History', 'Horror', 'Music', 'Musical'
                        , 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi'
                        , 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War'
                        , 'Western', 'movie', 'short', 'tvEpisode', 'tvMiniSeries'
                        , 'tvMovie', 'tvSeries', 'tvShort', 'tvSpecial', 'video'
                        , 'videoGame']
        '''

        self.feature_columns = ['isAdult', 'Action', 'Adult', 'Adventure'
                        , 'Animation', 'Biography', 'Comedy', 'Crime'
                        , 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir'
                        , 'Game-Show', 'History', 'Horror', 'Music', 'Musical'
                        , 'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi'
                        , 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War'
                        , 'Western', 'movie', 'short', 'tvEpisode', 'tvMiniSeries'
                        , 'tvMovie', 'tvSeries', 'tvShort', 'tvSpecial', 'video'
                        , 'videoGame']

        
        

    def search_movie(self, search_string, max_number_of_results: int) -> dict:
        '''
        Find a movie using search string on title column.

        Parameters
        ----------

        search_string : str Search string used to filter dataset.
        number_of_results : int Maximum number of results to return.

        Returns
        -------
        dict A dictionary that contain movies related by title with search string.

        '''        
        movies = self.dataset[self.dataset['originalTitle'].str.contains(search_string, case=False)]
        
        if len(movies) > max_number_of_results:
            return movies.iloc[0:max_number_of_results].to_dict('records')
        
        return movies.to_dict(orient='records')
    
    def get_movie(self, id:str) -> pd.DataFrame :
        '''
            Return a movie using alphanumeric unique identifier (tconst on dataset).

            Parameters
            ----------
            id : str The movie unique identifier.

            Returns
            -------
            pd.Dataframe A Pandas Dataset with movie or an empty dataset.
        '''
        return self.dataset[self.dataset['tconst'] == id]

    def get_recommendations(self, movie : pd.DataFrame, max_number_of_results : int) -> pd.DataFrame :
        '''
            Return movie recomendations.

            Parameters
            ----------
            movie: pd.Dataframe Movie to get recommendations
            max_number_of_results: int The maximum number of movie returned by method.

            Returns
            -------
            pd.Dataframe A Pandas dataframe with movie recommendations.
        '''
        
        user_movie_features = np.reshape(movie[self.feature_columns], (1, -1))

        print(f'Getting similar movies to {movie.at[movie.index.array[0], "originalTitle"]}. Please wait...')

        similarity_matrix = pairwise_distances(user_movie_features, self.dataset[self.feature_columns])
        recommendations = self.dataset.loc[:, self.dataset_columns.keys() ].merge(pd.Series(similarity_matrix[0], name='similarity'), left_index=True, right_index=True)
        recommendations.sort_values(by='similarity', inplace=True)

        if len(recommendations) < max_number_of_results:
            return recommendations.to_dict(orient='records')
        
        return recommendations.iloc[0:max_number_of_results].to_dict(orient='records')
