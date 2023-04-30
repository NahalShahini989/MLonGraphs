#!/usr/bin/env python
# coding: utf-8

# # ChessDB Dataset
# https://www.kaggle.com/datasets/milesh1/35-million-chess-games
# 
# https://chess-research-project.readthedocs.io/

# ## Column descriptions
# 1. Position of the game in the original PGN file. 
#     
# 2. Date at which the game was played (the format is ``year.month.day``).
#     
# 3. Game result specified inside brackets in the PGN file. The value can be ``1``, ``0`` or ``-1`` corresponding to white win, draw or loose, respectively.
#     
# 4. `ELO <https://en.wikipedia.org/wiki/Elo_rating_system>`_ of withe player (an integer number).
#     
# 5. ELO of black player (an integer number).
#     
# 6. Number of moves in the game (for some games it may be zero!)
#     
# 7. ``date_c`` = date (in ``year.month.day``) is corrupted or missing? the label should be ``date_true``, meaning the date is corrupted, or ``date_false``, meaning the date is NOT corrupted. The same logic applies to the following attributes ending in "_c" (i.e. _corrupted).
#     
# 8. ``resu_c`` = result (``1-0``, ``1/2-1/2``, or ``0-1``) is corrupted or missing?
#     
# 9. ``welo_c`` = withe ELO is corrupted or missing? 
#     
# 10. ``belo_c`` = black ELO is corrupted or missing?
#     
# 11. ``edate_c`` = event date is corrupted or missing? The event where the game was held (if there is one).
#     
# 12. ``setup`` may be ``setup_true`` or ``setup_false``. If it is true then the game initial position is specified. This is used when playing Fischer Random Chess for example.
#     
# 13. ``fen`` may be ``fen_true`` and ``fen_false``. It is related to column 12.
#     
# 14. In the original file the result is provided in two places. At the end of each sequence of moves and in the attributes part. This flag indicates if the result is (is not) properly provided after the sequence of moves (just for checking consistency in the PGN file).
#     
# 15. ``oyrange`` may be ``oyrange_true`` or ``oyrange_false``. This flag is false only for games with dates in the range of years [1998,2007]. The ``oyrange`` means ``out of year range``.
#     
# 16. ``bad_len`` (or bad len) flag indicates, when ``blen_true`` (``blen_false``), if the length of the game is (is not) good.
#     
# 17. Finally, after the token ``###``, you can find the sequence of moves. Each move has a number and a letter ``W`` (white) or ``B`` (black) indicating the th-move of the white or black player, respectively. 

# In[25]:


import pandas as pd
FPATH = 'dataset/all_with_filtered_anotations_since1998.txt'
df = pd.read_csv(FPATH, engine='python', skiprows=4, sep='###', nrows=1000)


# In[26]:


df = df.reset_index()
df[['id', 'Date', 'Result', 'welo' ,'belo', 'len', 'date_c', 'resu_c', 'welo_c', 'belo_c',
    'edate_c', 'setup', 'fen', 'resu2_c', 'oyrange', 'bad_len']] = df['index'].str.split(' ', expand=True).iloc[:,:-1]
df['moves'] = df.iloc[:,1]
df['moves'] = df['moves'].str.replace('[WB]\d+?\.', '', regex=True)
df = df.iloc[:,2:].set_index('id')
df.head()


# ## Dataset to `python-chess` game

# In[27]:


import chess
import chess.pgn
import io


# In[35]:


moves = io.StringIO(df.iloc[0]['moves'])
game = chess.pgn.read_game(moves)


# In[36]:


game.headers.update(df.iloc[0].drop('moves', inplace=False))


# In[5]:


cur = game
for i in range(3):
    cur = cur.next()
    if not cur: break
    display(cur.board())

