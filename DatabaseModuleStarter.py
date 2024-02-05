################
## Code Notes ##
################
# All code in this file has been written by Alan Fang, Ana Marie Peric, and Nolan Moody.
# This code must be run in order to successfully interact with the
# other file provided and contains the logic for creating and
# populating our twitterlike database with initial data.

# flask_bcrpyt must be installed prior to running this code.
# Please run the following command in your terminal:
# pip install flask_bcrypt

#### Start Program ####

import sqlite3
from flask_bcrypt import Bcrypt
# Initialize a new instance of Bcrypt for hashing.
bcrypt = Bcrypt()
# Create a new SQLite database (or connect to an existing one).

# Try connecting to the database. 
try:
    conn = sqlite3.connect("twitter_like.db")
    # Create a cursor object to interact with the database.
    cursor = conn.cursor()
    # Create a new datase if it doesn't exist.
except sqlite3.OperationalError:
    # Create a new database if it doesn't exist.
    conn = sqlite3.connect("twitter_like.db")
    cursor = conn.cursor()

# Turn on foreign key constraints to enforce referential integrity.
cursor.execute("PRAGMA foreign_keys = ON")

# Create a table for user profiles.
# user_id is the primary key, and username and password
# are required fields. The other information is optional
# and can be null. A timestamp is created automatically
# everytime a new user is inserted into the table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_profiles 
(user_id INTEGER PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
full_name TEXT NOT NULL,
email TEXT,
profile_image TEXT,
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
''')

# Create a table for tweets.
# tweet_id is the primary key, and user_id
# is the foreign key pointing to the user 
# profiles table. The tweet must contain
# text and so cannot be null. A timestamp is
# automatically created everytime a tweet
# is insterted into the table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS tweets 
(tweet_id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL,
tweet_content TEXT NOT NULL,
creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id)
    REFERENCES user_profiles(user_id));
''')

# Create a table for followers/following.
# follow_id is the priamry key, and the 
# follower_user_id and following_user_id 
# are foreign keys pointing back to the
# user_profiles table.
cursor.execute('''
CREATE TABLE IF NOT EXISTS followers_following
(follow_id INTEGER PRIMARY KEY,
follower_user_id INTEGER NOT NULL,
following_user_id INTEGER NOT NULL,
FOREIGN KEY (follower_user_id)
    REFERENCES user_profiles (user_id),
FOREIGN KEY (following_user_id)
    REFERENCES user_profiles (user_id));
''')

# Create a table for likes/retweets.
# like_retweet_id is the primary key,
# and user_id is a foreign key that
# points to the user profiles table.
# tweet_id is also a foreign key that 
# points to the tweet table. 
cursor.execute('''
CREATE TABLE IF NOT EXISTS likes_retweets
(like_retweet_id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL,
tweet_id INTEGER NOT NULL,
FOREIGN KEY (user_id)
    REFERENCES user_profiles (user_id),
FOREIGN KEY (tweet_id)
    REFERENCES tweets (tweet_id));
''')

# Create a table for comments.
# comment_id is the primary key,
# and user_id is a foreign key that
# points to the user profiles table.
# tweet_id is also a foreign key
# that points to the tweet table.
# a timestamp for the comment is
# automaticaly created everytime a new 
# comment is added to a tweet.
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments
(comment_id INTEGER PRIMARY KEY,
user_id INTEGER NOT NULL,
tweet_id INTEGER NOT NULL,
comment_text TEXT NOT NULL,
comment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id)
    REFERENCES user_profiles (user_id),
FOREIGN KEY (tweet_id)
    REFERENCES tweets (tweet_id));
''')

# Insert initial data into the tables upon initialization of the database.
# Password hashing is used so that the passwords stored in the database 
# do not appear in their original form. This also allows those testing
# the program to log in as one of these already created users if they wish.
password1 = "admin"
password2 = "hey123!"
password3 = "aushgh213$"
password4 = "aue734$"
password5 = "wgksh643!"
password6 = "hey123!"

hashed_passwords = (
    bcrypt.generate_password_hash(password1),
    bcrypt.generate_password_hash(password2),
    bcrypt.generate_password_hash(password3),
    bcrypt.generate_password_hash(password4),
    bcrypt.generate_password_hash(password5),
    bcrypt.generate_password_hash(password6))
try:
    cursor.execute('''INSERT INTO user_profiles (user_id, username, password, full_name) \
                VALUES 
               (1, "admin", ?, "admin"),
               (2, "Nolan", ?, "Nolan"),
               (3, "Ana",?,"Ana"),
               (4, "Alan", ?,"Alan"),
               (5, "DataRox", ?, "Joe Smith"),
               (6, "PythonEnthusiast",?, "Ken Henry")''',
               (hashed_passwords))

    cursor.execute('''INSERT INTO tweets (tweet_id, user_id, tweet_content) \
               VALUES 
               (1, 5, "I consider myself a data pro"),
               (2, 5, "I accidentally deleted the project i've been working on for 36 hours..."),
               (3, 5, "comment so i feel validated please"),
               (4, 2, "First tweet ever. Hey ya'll"),
               (5, 4, "so mad at my wifi right now..."),
               (6, 3, "UberEats > paying off my student loans"),
               (7, 3, "why am i the way that i am"),
               (8, 4, "why don't we still know where the pyramids came from? What's your theory?"),
               (9, 5, "i can't catch up on sleep"),
               (10, 2, "What's everyone's favourite thing about Twitter?"),
               (11, 6, "Starbucks Christmas drinks are back"),
               (12, 6, "Why did the python programmer go broke? Because he missed too many commas."),
               (13, 5, "I told my wife she should embrace her mistakes. She gave me a hug"),
               (14, 3, "What's everyone's favourite song right now?"),
               (15, 6, "More money more problems")''')

    cursor.execute('''INSERT INTO followers_following (follow_id, follower_user_id, following_user_id) \
               VALUES 
               (1, 5, 2),
               (2, 5, 3),
               (3, 5, 6),
               (4, 2, 4),
               (5, 2, 6),
               (6, 2, 3),
               (7, 3, 2),
               (8, 3, 4),
               (9, 3, 6),
               (10, 4, 2),
               (11, 4, 3),
               (12, 4, 5),
               (13, 6, 5),
               (14, 6, 4),
               (15, 6, 3)''')

    cursor.execute('''INSERT INTO likes_retweets (like_retweet_id, user_id, tweet_id) \
               VALUES 
               (1, 5, 8),
               (2, 5, 6),
               (3, 5, 10),
               (4, 2, 8),
               (5, 2, 6),
               (6, 2, 4),
               (7, 3, 8),
               (8, 3, 15),
               (9, 3, 4),
               (10, 4, 8),
               (11, 4, 4),
               (12, 4, 5),
               (13, 6, 8),
               (14, 6, 13),
               (15, 6, 3)''')

    cursor.execute('''INSERT INTO comments (comment_id, user_id, tweet_id, comment_text) \
               VALUES 
               (1, 6, 1, "ehem... i believe that would be me."),
               (2, 3, 8, "this exact thought keeps me up a lot at night..."),
               (3, 2, 2, "try 'ctrl' z"),
               (4, 3, 12, "ha."),
               (5, 4, 11, "literally no one cares."),
               (6, 5, 4, "Welcome, Nolan!"),
               (7, 5, 6, "i approve"),
               (8, 6, 4, "Welcome!"),
               (9, 6, 3, "validation, check."),
               (10, 2, 8, "aliens.")''')
except:
    print("Database and users already exist")
#commit the changes and close the connection
conn.commit()
conn.close()
