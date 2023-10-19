#!/usr/bin/env python
# coding: utf-8

# # What are the type of apps attract more users?

# ## 1. Introduction:
# This project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# ## 2. Exploring the dataset content:
# 
# let's open and start to explore the dataset

# In[1]:


def open_data(file_name):
    file_opened = open(file_name)
    from csv import reader
    file_reader = reader(file_opened)
    data_set = list(file_reader)
    return data_set


# In[2]:


apple_store_data = open_data('AppleStore.csv')


# In[3]:


google_play_data = open_data('googleplaystore.csv')


# In[4]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')
        
    if rows_and_columns:
        print('Number of rows: ', len(dataset))
        print('number of columns: ', len(dataset[0]))
    


# In[5]:


explore_data(apple_store_data, 1, 3, True)
explore_data(google_play_data, 1, 3, True)


# column names: 

# In[6]:


explore_data(apple_store_data, 0, 1)
explore_data(google_play_data, 0, 1)


# In[7]:


android_header = google_play_data[0]
print(android_header)


# ## 3. Data Cleaning

# ### 3.1 Removing Duplicate:

# 
# *Here we try to find data missing:*
# The answer is in row 10473 there is missing data in catagory column. we find that by notice the rating value which is incurrect.  

# In[8]:


for row in google_play_data[1:]:
    if len(row) != len(android_header):
        print(row)
        print("\n")
        print("Index postion is:", google_play_data.index(row))


# In[9]:


print(google_play_data[10473])


# Lets delete the row 10473:

# In[10]:


del google_play_data[10473]


#  Now we want to check if the "google play" dataset has duplicate:

# In[11]:


unique_value=[]
duplicated_value=[]

for app in google_play_data:
    if app[0] in unique_value:
        duplicated_value.append(app[0])
    else:
        unique_value.append(app[0])
        
print('Number of duplicate apps: ', len(duplicated_value))
print()
print('Examples of duplicate apps: \n', duplicated_value[:15])


# **For example, the "Box" app has duplicates:**

# In[12]:


for app in google_play_data:
    if app[0] == 'Box':
        print(app)


# **Another example, let's see the "Instagram" app:**

# In[13]:


for app in google_play_data:
    if app[0] == 'Instagram':
        print(app)


# **Notice that the 4th column has different values. The different numbers show the data was collected at different times. so we will keep the more recent**

# In[14]:


print(google_play_data[10473])


# Now, we will remove duplicates:

# In[15]:


reviews_max = {}

for row in google_play_data[1:]:
    name=row[0]
    reviews = float(row[3])
       
    if name in reviews_max and reviews_max[name]<reviews:
        reviews_max[name]=reviews
    
    elif name not in reviews_max:
        reviews_max[name]=reviews


# **In a previous code cell, we found that there are 1,181 cases where an app occurs more than once, so the length of our dictionary (of unique apps) should be equal to the difference between the length of our data set and 1,181:**

# In[16]:


print('Expected length:', len(google_play_data[1:]) - 1181)
print('Actual length:', len(reviews_max))


# Now, we update our dataset to google play data cleaned, we do that by 2 new lists: 

# In[17]:


google_play_data_clean = []
already_added = []

for row in google_play_data[1:]:
    name = row[0]
    reviews = float(row[3])
    
    if reviews == reviews_max[name] and name not in already_added:
        google_play_data_clean.append(row)
        already_added.append(name)
        


# lets check our data, to ensure everything went as expected:

# In[18]:


print(len(google_play_data_clean))


# ### 3.2 Removing Non-English Apps:

# here we create a function that check non english apps:

# In[19]:


def check_eng(a_string):
    characters_fallen = 0
    
    for character in a_string:
        if ord(character) > 127:
            characters_fallen+=1
            
    if characters_fallen > 3:
        return False
    else:
        return True


# In[20]:


print(check_eng('Docs To Go™ Free Office Suite'))
print(check_eng('Instachat 😜'))
print(check_eng('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# Now we filter out non-English apps:

# In[21]:


google_play_data_clean1=[]

for row in google_play_data_clean:
    name=row[0]
    if check_eng(name):
        google_play_data_clean1.append(row)
    


# In[22]:


apple_store_data_clean=[]

for row in apple_store_data:
    name=row[1]
    if check_eng(name):
        apple_store_data_clean.append(row)


# In[23]:


print('Google Data rows')
print('Before:', len(apple_store_data))
print('After:', len(apple_store_data_clean))
print()
print('App store rows')
print('Before:', len(google_play_data_clean))
print('After:', len(google_play_data_clean1))


# ### 3.3 Isolating the free apps:

# **Here our updated datasets**:
# apple_store_data_clean, 
# google_play_data_clean1

# In[24]:


google_play_data_clean2 = []

for row in google_play_data_clean1:
    price = row[6]
    
    if price == 'Free':
        google_play_data_clean2.append(row)


# In[25]:


print(len(google_play_data_clean2))
print(len(google_play_data_clean1))


# In[26]:


apple_store_data_clean1 =[]

for row in apple_store_data_clean[1:]:
    price = float(row[4])
    
    if price == 0.0:
        apple_store_data_clean1.append(row)


# In[27]:


print(len(apple_store_data_clean1))
print(len(apple_store_data_clean))


# ## 4. Most Common Apps by Genre

# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we then develop it further.
# 3. If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of the most common genres for each market. For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.

# **The updated datasets:** google_play_data_clean2, apple_store_data_clean1

# finding the relevante column:

# In[28]:


for row in google_play_data_clean2:
    print(row[9])


# finding the relevante column:

# In[29]:


for row in apple_store_data_clean1:
    print(row[11])


# freq_table function & display_table:

# In[30]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# Now we will use display_table function to analyze the datasets:

# In[31]:


display_table(apple_store_data_clean1, 11)


# **Summary Analysis:**
# 1. the most common genre is: 'Games'
# 2. the next most common is: 'Entertainment'
# 3. the general impression is that the most of the apps designed more for fun and entertainment.
# 4. However, the fact that fun apps are the most numerous doesn't also imply that they also have the greatest number of users — the demand might not be the same as the offer.

# In[32]:


display_table(google_play_data_clean2, 1)


# In[33]:


display_table(google_play_data_clean2, 9)


# **Summary Analysis:**
# 1. the most common genres: 'Tools'
# 2. followed by 'Entertainment' apps and then Education apps.
# 3. compared to the previous analysis, we can see here that doesn't happen the same, the fun apps not is the most popular in this market, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids

# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# In[34]:


table = freq_table(apple_store_data_clean1, 11)

for genre in table:
    total=0
    len_genre=0
    
    for row in apple_store_data_clean1:
        genre_app = row[11]
        
        if genre_app == genre:
            n_user_ratings=float(row[5])
            total += n_user_ratings
            len_genre += 1
            
    avg_n_user_ratings = total/len_genre
    print(genre,' : ',avg_n_user_ratings)


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:

# In[35]:


for row in apple_store_data_clean1:
    if row[-5] == 'Navigation':
        print(row[1], ':', row[5]) # print name and number of ratings


# ### 4.2 Most Popular Apps by Genre on Google Play:

# In[40]:


freq_table(google_play_data_clean2, 1)


# In[48]:


categories_android = freq_table(google_play_data_clean2, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in google_play_data_clean2:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, communication apps have the most installs: 38,456,119.

# ### 5. Conclusions
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
