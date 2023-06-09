# Gili Wolf 315144907
import sys
import pandas as pd

class myData:
    def __init__(self, path1, path2, path3) -> None:
        self.books_data = pd.read_csv(path1, sep=";", on_bad_lines='skip', encoding='latin-1')
        self.clean_publication_data()
        self.ratings_data = pd.read_csv(path2, sep=";", on_bad_lines='skip', encoding='latin-1')
        self.users_data = pd.read_csv(path3, sep=";", on_bad_lines='skip', encoding='latin-1')
        # self.clean_age()

    # cleans all the rows containong non-numeric values of 'age' column
    def clean_age(self):
        print(len(self.users_data['Age']))
        self.users_data['Age'] = self.users_data['Age'].astype('str')
        self.users_data = self.users_data[pd.to_numeric(self.users_data['Age'], errors='coerce').notnull()]
        self.users_data['Age'] = self.users_data['Age'].astype('float')
        print(len(self.users_data['Age']))

    # cleans all the rows containing non numeric values of 'year of publication'
    def clean_publication_data(self):
        # print(len(self.books_data['Year-Of-Publication']))
        self.books_data['Year-Of-Publication'] = self.books_data['Year-Of-Publication'].astype('str')
        self.books_data = self.books_data[pd.to_numeric(self.books_data['Year-Of-Publication'], errors='coerce').notnull()]
        # print(len(self.books_data['Year-Of-Publication']))
        self.books_data['Year-Of-Publication'] = self.books_data['Year-Of-Publication'].astype('int32')
    
    # returns the number of books which were published in the range [start_year, end_year) (not including end_year)
    # raises an assertion value if start_year is bigger or equal to end_year
    def num_year(self, start_year, end_year):
        self.check_range_of_years(start_year,end_year)
        filtered_start_year = self.books_data[(self.books_data['Year-Of-Publication'] >= start_year)]
        filtered_start_and_end_year = filtered_start_year[(filtered_start_year['Year-Of-Publication']< end_year)]
        return len(filtered_start_and_end_year)
    
    # return new data frame of all the books published in the given year, with 2 columns: Book-Title', 'Year-Of-Publication'
    # raises an type error if the year is not an int
    def df_published(self, year):
        try: 
            int(year)
        except:
            raise TypeError("year is not an int")
        filtered_df = self.books_data[self.books_data['Year-Of-Publication'] == int(year)]
        new_df = filtered_df[['Book-Title', 'Year-Of-Publication']]
        return new_df
    
    # raises an assertion value if start_year is bigger or equal to end_year
    def check_range_of_years(self, start_year, end_year):
        assert int(end_year)>int(start_year), "start year is bigger than end year "
    
    # returns a tuple list of (year, num_of books) of the range [start_year,end_year]
    # num of books is number of published books in this year
    def num_books_by_year(self, start_year, end_year):
        self.check_range_of_years(start_year,end_year)
        books_list =[]
        for year in range(int(start_year), int(end_year) + 1):
            # using the num_of_books of the range [year, year +1)
            num_of_books = self.num_year(year, year+1)
            if (num_of_books == 0):
                continue
            books_list.append((year, num_of_books))
        return books_list

    # calculates and return a tuple of the mean and std of the ages of users_data
    def mean_std(self, country):
        #perperation- split the location into a list and get the last value as the user's country
        # add country column to the users data
        seperate_list_column = self.users_data['Location'].str.split(',')
        country_column = seperate_list_column.str[-1]
        country_column_cleaned = country_column.str.strip()
        #add country columns to the data frame
        self.users_data['Country'] = country_column_cleaned

        #group by name of the countries, and extract mean and std from the group of the given country
        gb = self.users_data.groupby('Country')
        try:
            users_of_country = gb.get_group(str(country))
        except:
            print(country, "is not a country in the users data")
            return
        age_series = users_of_country['Age']
        age_mean = age_series.mean(numeric_only = True)
        age_std = age_series.std(numeric_only = True)
        return (round(age_mean,3), round(age_std,3))
    
    #returns a series of the book's ISBNs according to the books data
    def book_name_to_isbn(self, book_name):
        filter_by_name = self.books_data[self.books_data['Book-Title'] == str(book_name)]
        return filter_by_name['ISBN']
    
    #return the mean of all of the ratings from all of the book's ISBNs
    def mean_rating(self, book_name):
        ISBNs =self.book_name_to_isbn(book_name)
        if ISBNs.size == 0:
            print("no ISNBs were found to this book's name")
            return
        rating_sum = 0
        num_of_ratings = 0
        for isbn in ISBNs:
            #add to total sum all of the book's rating from the current ISBN and add the count of the ratings to the total number of ratings
            filter_by_ISBN = self.ratings_data[self.ratings_data['ISBN'] == str(isbn)]
            rating_for_isbn = filter_by_ISBN["Book-Rating"]
            rating_sum += rating_for_isbn.sum(numeric_only= True)
            num_of_ratings += rating_for_isbn.count()
        if num_of_ratings == 0:
            print("no ratings were found")
            return
        return rating_sum / num_of_ratings




md = myData("books.csv","ratings.csv","users.csv")
print(md.mean_rating("The Kitchen God's Wife"))
# print(md.users_data)
# print(md.mean_std("usa"))
# print(md.users_data)
# df = md.books_data
