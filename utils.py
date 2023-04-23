# utils functions
import pandas as pd
import math

def time_to_rating(x):
    """
    Calculates the rating for a given watchtime.

    Parameters:
    x (float): The amount of time watched, in 10-min periods.

    Returns:
    int: The rating for the watchtime. The rating is calculated using the formula: rating = 2*(x/2)**(1/3).
         The rating is an integer between 1 and 10 inclusive.
    """
    rating = (x/2)**(1/2)
    rating = max(rating, 1)
    rating = min(rating, 10)
    return math.floor(rating)
	
def df_to_rating(df):
    """Converts a DataFrame containing start and stop times for user viewing sessions
    into a DataFrame containing user, streamer, and rating columns.

    Args:
        df (pandas.DataFrame): A DataFrame containing the following columns:
            - user (str): The name of the user who viewed the stream.
            - stream (str): The name of the stream viewed by the user.
            - streamer (str): The name of the streamer whose stream was viewed.
            - start (pandas.Timestamp): The start time of the user's viewing session.
            - stop (pandas.Timestamp): The stop time of the user's viewing session.

    Returns:
        pandas.DataFrame: A DataFrame containing the following columns:
            - user (str): The name of the user who viewed the stream.
            - streamer (str): The name of the streamer whose stream was viewed.
            - rating (float): The rating of the user's viewing sessions for the streamer,
              calculated as the total watchtime multiplied by a factor based on the duration
              of the viewing session.
    """
    watchtime_df = pd.DataFrame({
        'user': df.user,
        'stream': df.stream,
        'streamer': df.streamer,
        'watchtime': df.stop - df.start
    })
    
    grouped_watchtime = watchtime_df.groupby(['user', 'streamer'])['watchtime'].sum().reset_index()

    return pd.DataFrame({
      'user': grouped_watchtime.user,
      'streamer': grouped_watchtime.streamer,
      'rating': grouped_watchtime.watchtime.apply(time_to_rating)
    })