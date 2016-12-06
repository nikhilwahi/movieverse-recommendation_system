import UI as ui

def main():
	sample_movies, my_ask = ui.main_function(0, None, None, None, None, None)
	for movie in sample_movies:
		print movie

	user_ratings = [1,2,3,1,4,2,3,2,1,5]
	genres_liked = ui.main_function(1, user_ratings, 21, 'M', 'student', my_ask)
	for genre in genres_liked:
		print genre

if __name__ == "__main__":
    main()