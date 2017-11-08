# -*- coding: utf-8 -*-

"""
futmarket.core
~~~~~~~~~~~~~~~~~~~~~
This module implements the futmarket's basic methods.
"""

# Imports
## Relies heavily on fut package.

import fut
import pandas as pd
from time import sleep

# Login
## Login to EA Sports. May require two-factor authentication. You will be prompted for code, which is likely in email inbox.

def login():
    global fut
    print('Email: ')
    email = raw_input()
    print('Password: ')
    password = raw_input()
    print('Secret: ')
    secret = raw_input()
    print('platform: [pc/ps3/ps4/xbox/xbox360] ')
    platform = raw_input()
    print('Loading...')
    fut = fut.Core(email, password, secret, platform)
    print('You have logged in successfully.')


# Keepailve
## Run this every ~10 mins so the program continues to run

def keepalive():
    global coins
    coins = fut.keepalive()
    return(coins)


# Sold
## Clean up tradepile of those who sold

def sold():
    tradepile = fut.tradepile()
    sold = []
    bids = []
    for i in range(0, len(tradepile)):
        if tradepile[i]['tradeState'] == 'closed':
            sold.append(fut.players[tradepile[i]['assetId']]['lastname'])
            bids.append(tradepile[i]['currentBid'])
            print('Sold %s %s for %s coins' % (fut.players[tradepile[i]['assetId']]['firstname'], fut.players[tradepile[i]['assetId']]['lastname'], tradepile[i]['currentBid']))
            fut.tradepileDelete(tradepile[i]['tradeId'])
    return('Sold %s players for %s coins' % (len(sold), sum(bids)))

# Not Sold
## Clean up tradepile of those that did not sell

def not_sold():
    tradepile = fut.tradepile()
    for i in range(0, len(tradepile)):
        if (tradepile[i]['tradeState'] == 'expired') or (tradepile[i]['tradeState'] == None):
            print('Did not sell %s %s. Moved back to team.' % (fut.players[tradepile[i]['assetId']]['firstname'], fut.players[tradepile[i]['assetId']]['lastname']))
            fut.sendToClub(tradepile[i]['id'])

# Active
## Gets active trades in tradepile

def active():
    tradepile = fut.tradepile()
    global active_players
    active_players = []
    for i in range(0, len(tradepile)):
        if (tradepile[i]['tradeState'] == 'active'):
            active_players.append(tradepile[i]['assetId'])
            print("""Actively selling %s %s. Expires in %s minutes. %s bids so far and a current price of %s.""" %
            (fut.players[tradepile[i]['assetId']]['firstname'], fut.players[tradepile[i]['assetId']]['lastname'],
            int(round(tradepile[i]['expires']/60)), tradepile[i]['offers'], tradepile[i]['currentBid']))

# My Team
## Get names and attributes of team members, including last sale price

def my_team():
    sold()
    not_sold()
    myclub = fut.club()
    my_auction = pd.DataFrame(myclub)
    my_auction = my_auction[my_auction['untradeable'] == False]
    assetIds = my_auction['assetId'].tolist()
    ids = my_auction['id'].tolist()
    firstnames = []
    lastnames = []
    for i in assetIds:
        firstnames.append(fut.players[i]['firstname'])
        lastnames.append(fut.players[i]['lastname'])
    players = [i + ' ' + j for i, j in zip(firstnames, lastnames)]
    position = my_auction['position'].tolist()
    rating = my_auction['rating'].tolist()
    contract = my_auction['contract'].tolist()
    lastSalePrice = my_auction['lastSalePrice'].tolist()
    discardValue = my_auction['discardValue'].tolist()
    my_values = [max(lastSalePrice, discardValue) for lastSalePrice, discardValue in zip(lastSalePrice, discardValue)]
    global team
    team = pd.DataFrame(
        {'assetId': assetIds,
         'id': ids,
         'name': players,
         'position': position,
         'rating': rating,
         'contract': contract,
         'my_value': my_values
         }
         )
    return(team)


# Min value function


def mins(items, n):
    mins = items[:n]
    mins.sort()
    for i in items[n:]:
        if i < mins[-1]:
            mins.append(i)
            mins.sort()
            mins= mins[:n]
        return(mins)


# Median value function


def median(lst):
    n = len(lst)
    if n < 1:
            return None
    if n % 2 == 1:
            return sorted(lst)[n//2]
    else:
            return sum(sorted(lst)[n//2-1:n//2+1])/2.0


# My Market
## Get market for my tradeable players. Constrain by page depth (time) and strategy option.

def my_market(depth=1, strategy=1):
    # See if team exists yet as a variable
    try:
        team
    except NameError:
        my_team()
    else:
        mkt_value = []
        # Loop through each team member to get market values
        for i in range(0, len(team)):
            print('Getting market value for: %s' % (team['name'][i]))
            mkt_values = []
            for page in range(0, depth):
                for d in fut.search(ctype='player', assetId=str(team['assetId'][i]), page_size='50', start=page):
                    mkt_values.append({'buy': d['buyNowPrice'], 'tradeId': d['tradeId']})
            if strategy == 1:
                # Gets median of min 5 market values
                mkt_value.append(median(mins(mkt_values, 5)))
                print('Checked %s players. Market value of %s coins added for %s' % (depth*50, mkt_value[i]['buy'], team['name'][i]))
            if strategy == 2:
                # New strategy here
                ###
                print('Checked %s players. Market value of %s coins added for %s' % (depth*50, mkt_value[i]['buy'], team['name'][i]))
            if strategy == 3:
                # New strategy here
                ###
                print('Checked %s players. Market value of %s coins added for %s' % (depth*50, mkt_value[i]['buy'], team['name'][i]))
        # Create a dataframe of market values that merges with team members
        mkt_value = pd.Series(mkt_value).values
        sell = []
        for i in mkt_value:
            sell.append(i['buy'])
        market = pd.DataFrame(
            {'mkt_value': sell}
            )
        global team_market
        team_market = pd.merge(team, market, left_index=True, right_index=True)


# List
## Put players on the block, send to tradepile and sell


def list_players(min_value=300, strategy=1):
    my_market()
    print('Cleaning up tradepile...')
    sold()
    not_sold()
    active()
    tradepile = fut.tradepile()
    # Get players on the block
    global block
    block = team_market[team_market['my_value']>min_value]
    print('%s players on the block with a value to you of %s coins and a market value of %s coins' % (len(block), block['my_value'].sum(), block['mkt_value'].sum()))
    global quicksell
    quicksell = team_market[team_market['my_value']<=min_value]
    if len(quicksell) == 0:
        print('No items to quicksell.')
    else:
        for index, row in quicksell.iterrows():
            fut.quickSell(row['id'])
            print('Quick sold %s items for %s coins' % (len(quicksell), quicksell['my_value'].sum()))
    # Get available space and send players from block to tradepile
    available_space = fut.pileSize().get('tradepile') - len(tradepile)
    block = block.head(n=available_space)
    for index, row in block.iterrows():
        if row['assetId'] in active_players:
            block.drop(index, inplace=True)
    if len(block) == 0:
        print('No players to list on market.')
    else:
        print('%s players can be added to tradepile.' % (len(block)))
        for index, row in block.iterrows():
            fut.sendToTradepile(row['id'])
            sleep(2)
            print('%s added to tradepile.' % (row['name']))
        print('%s players successfully added to tradepile.' % (len(block)))
    # List players on market
    # Strategy 1: List at my value, buy now at market value.
    if strategy==1:
        for index, row in block.iterrows():
            if row['mkt_value'] > row['my_value']:
                fut.sell(item_id = row['id'], bid = row['my_value'], buy_now = row['mkt_value'], duration = 3600)
                print('%s has been listed on the market for %s coins to buy now and %s coins starting bid' % (row['name'], row['mkt_value'], row['my_value']))
            if row['mkt_value'] <= row['my_value']:
                print('The market value for %s is below or equal to what you originally paid. Moving this card back to team for now.' % (row['name']))
                fut.sendToClub(row['id'])
            sleep(10)
    print('All tradeable players have been listed on the market. Check back in an hour to see if they sold')
