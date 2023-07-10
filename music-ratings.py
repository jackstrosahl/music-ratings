from collections import defaultdict
from math import inf
from operator import gt, lt

def max_ties(x, key, max=True):
    best = -inf if max else inf
    ties = None
    compare = gt if max else lt
    for val in x:
        res = key(val)
        if compare(res, best):
            best = res
            ties = [val]
        elif res == best:
            ties.append(val)
    return ties


chooser = "chooser"
ratings = "ratings"
title = "title"
total_rating = "total_rating"
num_ratings = "num_ratings"
num_songs = "num_songs"
avg_rating = "avg_rating"

def make_song():
    return {ratings: []}

def format_song(song):
    return f"{song[title]} from {song[chooser]} rated: {', '.join(str(x) for x in song[ratings])}"

songs = []
chooser_stats = defaultdict(lambda: {total_rating: 0, num_songs: 0, num_ratings: 0, avg_rating: 0})
with open("ratings.txt") as f:
    i = 0
    song = make_song()
    for row in f:
        row = row.replace("\n","")
        if i > 1:
            try:
                value = int(row)
                song[ratings].append(value)
                continue
            except ValueError:
                chooser_stats[song[chooser]][total_rating] += sum(song[ratings])
                chooser_stats[song[chooser]][num_ratings] += len(song[ratings])
                chooser_stats[song[chooser]][num_songs] += 1
                songs.append(song)
                song = make_song()
                i = 0
        if i == 0:
            song[chooser] = row
        elif i == 1:
            song[title] = row
        i += 1

print("Highest Rated Songs:")
for song in max_ties(songs, key=lambda x: sum(x[ratings])/len(x[ratings])):
    print(format_song(song))

print("Lowest Rated Songs:")
for song in max_ties(songs, key=lambda x: sum(x[ratings])/len(x[ratings]), max=False):
    print(format_song(song))

for chooser, stats in chooser_stats.items():
    chooser_stats[chooser][avg_rating] = stats[total_rating]/stats[num_ratings]

print("Average Ratings:")
for chooser, stats in sorted(chooser_stats.items(), key=lambda x:x[1][avg_rating]):
    print(f"{chooser}: {stats[avg_rating]} Average Rating")

print("Number of Songs:")
for chooser, stats in sorted(chooser_stats.items(), key=lambda x:x[1][num_songs], reverse=True):
    print(f"{chooser}: {stats[num_songs]} Songs")