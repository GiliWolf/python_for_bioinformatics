# Gili Wolf 315144907
import sys
import pandas as pd

class myData:
    def __init__(self, path1, path2, path3) -> None:
        self.books_data = pd.read_csv(path1, sep=";", on_bad_lines='skip', encoding='latin-1')
    
    # cleans all the rows containing non numeric values of 'year of publication'
    def clean_publication_data(self):
        self.books_data['Year-Of-Publication'] = self.books_data['Year-Of-Publication'].astype('str')
        self.books_data = self.books_data[pd.to_numeric(self.books_data['Year-Of-Publication'], errors='coerce').notnull()]
        self.books_data['Year-Of-Publication'] = self.books_data['Year-Of-Publication'].astype('int32')
    
    # returns the number of books which were published in the range [start_year, end_year) (not including end_year)
    # raises an assertion value if start_year is bigger or equal to end_year
    def num_year(self, start_year, end_year):
        self.check_range_of_years(start_year,end_year)
        self.clean_publication_data()
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
        self.clean_publication_data()
        filtered_df = self.books_data[self.books_data['Year-Of-Publication'] == int(year)]
        new_df = filtered_df[['Book-Title', 'Year-Of-Publication']]
        return new_df
    
    # raises an assertion value if start_year is bigger or equal to end_year
    # if valid- cleans publication data
    def check_range_of_years(self, start_year, end_year):
        assert int(end_year)>int(start_year), "start year is bigger than end year "
        self.clean_publication_data()
    
    def num_books_by_year(self, start_year, end_year):
        self.check_range_of_years(start_year,end_year)
        books_list =[]
        for year in range(int(start_year), int(end_year) + 1):
            num_of_books = self.num_year(year, year+1)
            if (num_of_books == 0):
                continue
            books_list.append((year, num_of_books))
        return books_list





md = myData("books.csv","a","b")
print(md.num_books_by_year(1900,1919))
# df = md.books_data
# print(df.size())
# df['Year-Of-Publication'] = df['Year-Of-Publication'].astype('str')
# df = df[pd.to_numeric(df['Year-Of-Publication'], errors='coerce').notnull()]
# df['Year-Of-Publication'] = df['Year-Of-Publication'].astype('str')
# print(df.size())

# df_new = df_new.astype({'Year-Of-Publication': 'int32'}).dtypes
# print(df_new['Year-Of-Publication'])
# df_new.size()
# df_new[3] = df_new[3].astype(int)
# df_new = df_new.astype({'Year-Of-Publication': 'int32'}).dtypes
# df_new.loc[:, 'Year-Of-Publication'] = df_new.loc[:, 'Year-Of-Publication'].astype('int32').copy()
