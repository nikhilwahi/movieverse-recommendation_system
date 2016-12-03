import UI as ui

def main():
	my_list = ui.supply_sample_movies()
	# for item in my_list:
	# 	print item

	user_ratings = [5,5,5,5,5,2,3,4,1,2]
	genres_liked = ui.return_preferred_genres(user_ratings, 21, 'M', 'student', 110018)
	print("Genres you like are")
	for genre in genres_liked:
		print genre


if __name__ == "__main__":
    main()