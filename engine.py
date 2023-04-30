#!/usr/bin/env python
# coding: utf-8

# ## Deploy engines locally
# Stockfish + NNUE (Efficiently Updatable NN)
# - v15.1
# - NNUE portion was merged 25 July 2020
# - https://github.com/official-stockfish/Stockfish/wiki/Compiling-from-source
# 
# Leela Chess Zero (Lc0) v0.29
# - open-source engine using NN
# - https://github.com/LeelaChessZero/lc0/blob/master/README.md#building-and-running-lc0
# 

# In[1]:


import chess
import chess.engine


# In[4]:


STOCKFISH_BIN = '/home/asy51/repos/Stockfish-sf_15.1/src/stockfish'
LC0_BIN = '/home/asy51/repos/lc0/build/release/lc0'

stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_BIN)
lc0 = chess.engine.SimpleEngine.popen_uci(LC0_BIN)

board = chess.Board()
while not board.is_game_over():
    engine = stockfish if board.turn else lc0
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    # display(board)
    # if input() == 'q': break
    print(len(board.move_stack), end='\r')
stockfish.quit()
lc0.quit()


# In[11]:


board.outcome().result()


# ## Leela Chess Zero NN Arthitecture
# From (https://lczero.org/dev/backend/nn/), based on AlphaGoZero and AlphaZero
