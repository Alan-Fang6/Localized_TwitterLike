################
## Code Notes ##
################
#  All code in this file has been written by Alan Fang, Ana Marie Peric, and Nolan Moody,
# Prior to running this code, please ensure that the code in the other provided file, 
# "DatabaseModuleStarter.py", has been run to initialize the database used in this program.

# Emoji and flask_bcrpyt must be installed prior to running this code. 
# Please run the following commands in your terminal:
# pip install emoji 
# pip install flask_bcrypt

#### Start Program ####

# Import the required packages.
import sqlite3
import emoji
import time
from flask_bcrypt import Bcrypt

# Command Line Interface 

# Connect to the database.
conn=sqlite3.connect("twitter_like.db")
cursor=conn.cursor()

# Initialize a new instance of Bcrypt for hashing.
bcrypt = Bcrypt()
pausetime = 1

# Check if the database tables exist. If not, the program will terminate. If this
# happens, please run the code in "DatabaseModuleStarter.py" and try again.
cursor.execute('''SELECT name FROM sqlite_master 
               WHERE type = 'table' and name = 'user_profiles';''')
if cursor.fetchone() is None: # This returns none when the user_profile table is not found.
    print("The database has not been initialized. Please use DatabaseModuleStarter file to intitialize the database.")
    conn.close() # Close the database connection.
    exit() # terminate the program.

# Initialize a username and id variable, and begin the login or registration process.
username = "temp"
current_userid = "temp"
print(emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'),
      "Welcome to Twitterlike",
      emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'),
      emoji.emojize(':front-facing_baby_chick:'))

# The main functionality of this program operates on for loops.
# Until a user provides a valid selection at any point where they
# are asked to provide an input, the loop will repeat. Once a valid
# selection is input, the loop with break.
while True:
    print("Please Select")
    print("1. Login (Existing Users)")
    print("2. Register (New Users)")
    print("3. Exit the program")
    choice = input("Enter your selection: ")
    # Check for validity of the user selection.
    # User must select 1, 2, or 3 to proceed.
    if choice in ["1", "2", "3"]:
        choice = int(choice) # Convert the input to an integer for ease of use in later code.
        break # loop breaks when user enters 1, 2, or 3.
    else: # Loop continues if selection is not valid.
        print("Selected option is not a valid option. Please select a valid choice from the menu.")
        time.sleep(pausetime)  
        
# Logging in.
if choice == 1:
    # Initialize a variable to record how many times a user unsuccessfully tries to login.
    login_attempts = 0 
    login_penalty_sec = 20
    while True:
        # Receiving username and password input, retrieving password from database for username
        username = input("Username: ")
        password = input("Password: ")
        cursor.execute('''SELECT password FROM user_profiles 
                       WHERE username = ?''', 
                       (username, ))
        user_password = cursor.fetchone()
        # If that user info doesn't exist in the database or if the password is wrong, then
        # the login is unsuccessful. 
        if user_password is None or not bcrypt.check_password_hash(user_password[0],password):
            login_attempts += 1 # Record failed login.
            # If the user has failed to login successfully 5 times, the login screen
            # is temporarily locked. The time it is locked for increases by 10 seconds
            # for each subsequent failure.
            if login_attempts < 5:
                print("Incorrect login information. Please try again.")
                time.sleep(pausetime)
                continue
            else:
                print("Max login attempts exceeded. Login suspended for ", 
                      login_penalty_sec, 
                      " seconds.")
                time.sleep(login_penalty_sec) # Force the program to pause. 
                login_penalty_sec += 10 # Add ten sec to the timeout variable.

        # If the username and password pair that the user provided matches the 
        # info in the database, the login is successful.
        else:
            print("Login successful. Welcome", username)
            time.sleep(pausetime)
            break

# Registering a new user.
elif choice == 2:
    # Generate the new user id by adding one to the largest 
    # of the current user ids in the database.
    cursor.execute('''SELECT MAX(user_id) FROM user_profiles''')
    new_user_id = cursor.fetchone()[0] + 1

    # Create a username.
    while True:
        username = input("Please choose a username: ")
        # Check if the username already exists in the database.
        cursor.execute("SELECT username FROM user_profiles WHERE username = ?", (username, ))
        username_test_fetch = cursor.fetchone()
        if username: # A user must enter a username to proceed.
            # The above query will return none if the username does not
            # exist already, and will not be none when it does exist.
            if username_test_fetch is not None:
                print("Username already taken. Please enter a different username.")
                continue
        else: # If the user failed to enter a username, they will be asked again.
            print("You must enter a username to proceed")
            continue
        break # Break the program when the user enters a unique username.

    # Creating a password.
    while True:
        special_characters = "[@_!$%^&*()<>?/\|}{~:]#+-=,.`" # Used to check password requirements. 
        # Ask the user for a password. 
        password = input("Please choose a password (must contain at least three letters, two numbers, and a special character): ")
        if password == username: # Passwords cannot be the same as the username for security purposes. 
            print("Password cannot be the same as your username. Please choose a different password.")
            time.sleep(pausetime)
            continue # Ask again.
        elif password: # Proceed if the user enters a password.
            # Initilize variables to count the number of letters,
            # numbers, and special characters in the password that
            # the user provided.
            letter_count = 0
            number_count = 0
            special_char_count = 0
            # Now count the number of letters, numbers, and
            # special characters in the password.
            for char in password:
                if char.isalpha():
                    letter_count += 1
                elif char.isdigit():
                    number_count += 1
                elif char in special_characters:
                    special_char_count += 1
            
            # If the password is accepted, then hash it and continue
            if letter_count >= 3 and number_count >= 2 and special_char_count >= 1:
                print("Username and password accepted. Please enter additional information.")
                password = bcrypt.generate_password_hash(password)
                time.sleep(pausetime)
                break
            else: # If the password does not meet security requirements, ask again.
                print("Password must contain at least three letters, two numbers, and a special character. Please try another password.")
                time.sleep(pausetime)
                continue
        else: # If the user did not enter a password, ask again.
            print("Please enter a valid password to proceed.")
            time.sleep(pausetime)
            continue
    # The following code only executes after a valid username and password are chosen by the user. 
    full_name = input("Please enter your full name (press enter to skip): ") # Optional field.
    email = input("Please enter your email address (press enter to skip): ") # Optional field.
    profile_image = input("Please enter a link to your profile image (press enter to skip): ") # Optional field.

    # Insert the new user information into the database.
    cursor.execute('''INSERT INTO user_profiles (user_id, username, password, full_name, profile_image) 
                   VALUES(?,?,?,?,?)''',
                    (new_user_id, username, password, full_name, profile_image))
    conn.commit() # Commit the insertion of the new user into the database.
    print("New user successfully created. Welcome,", username)
    time.sleep(pausetime)

# Exiting without logging in or registering. 
elif choice == 3:
    print("Goodbye") # Inform the user that they are exiting.
    conn.close() # Close the connection.
    exit() # Terminate the program.

# After a user logs in or registers, their user id is retrieved and stored
# for the duration of their interaction with the program. 
cursor.execute('''SELECT user_id FROM user_profiles WHERE username =?''',
                (username,))
current_userid = cursor.fetchone()[0]

# CLI interface selection screen. A while loop is used to
# return the user to this initial option screen when 
# required. The loop is terminated when the user wishes
# to logoff.
while True:
    print("Please Select")
    print("1. Post a Tweet")
    print("2. View Timeline")
    print("3. Like/Unlike a Tweet")
    print("4. Follow a User")
    print("5. Unfollow a User")
    print("6. View Followers/Following")
    print("7. Help")
    print("8. Exit")
    print("9. View your tweets")

    while True: # Check that the user entered a number.
        choice = input("Enter your choice: ")
        try:
            choice = int(choice) # Convert the input to an integer.
            break # Continue with the program.
        except ValueError or TypeError:
            print("That is not a valid choice")

    if choice == 1: # Posting a tweet.
        # Allow the user to generate the Tweet content.
        tweet_content = input("Enter Tweet: ")
        # Create the Tweet Id.
        cursor.execute('''SELECT MAX(tweet_id) FROM tweets''')
        newest_tweet_id = cursor.fetchone()
        if newest_tweet_id[0] is not None:
            newest_tweet_id = newest_tweet_id[0]+1
        elif newest_tweet_id[0] is None:
            newest_tweet_id = 1 
        # Insert the tweet content and relevant info into the Tweet table.
        cursor.execute('''INSERT INTO tweets (tweet_id, user_id, tweet_content) VALUES(?,?,?)''', 
                       (newest_tweet_id, current_userid, tweet_content))
        conn.commit()

    elif choice == 2: # Viewing user timeline.
        print("\n")
        print("Welcome,",username, "!\n")
        # Retrieve all tweets from users followed in descending order by tweet time stamp.
        cursor.execute('''SELECT user_profiles.username,tweet_id,
                       tweet_content FROM followers_following 
                       INNER JOIN tweets ON followers_following.following_user_id = tweets.user_id 
                       INNER JOIN user_profiles ON user_profiles.user_id=tweets.user_id 
                       WHERE followers_following.follower_user_id = ? 
                       ORDER BY tweets.tweet_id DESC ''',
                       (current_userid,))
        tweets = cursor.fetchall()
        # Create the timeline to display to the user.
        users = list()
        tweetid = list()
        tweetcontent = list()
        numberlikes = list()
        # Combine the retrieved columns into a list.
        for tweet in tweets:
            users.append(tweet[0])
            tweetid.append(tweet[1])
            tweetcontent.append(tweet[2])
        timeline = [users,tweetid,tweetcontent]

        # If there are no tweets from followed users or there are no followed users:
        if not tweets:
            print("Oh no! Looks like your timeline is empty. Let's take you back to the main list so you can change that. Happy Tweeting!")
            time.sleep(5)
            pass
        # Retrieve the count of likes for all followed users tweets.
        else:
            for tweet in timeline[1]:
                cursor.execute('''SELECT COUNT(tweet_id) 
                               FROM likes_retweets 
                               WHERE tweet_id =? ''',
                               (tweet,))
                numberlikes.append(cursor.fetchone()[0])
            timeline.append(numberlikes)
            
            for tweet in range(len(timeline[0])):
                print(timeline[0][tweet],"( Tweet ID:",timeline[1][tweet],")")
                print("   ",timeline[2][tweet])
                print(emoji.emojize(':thumbs_up:'), timeline[3][tweet], "\n")

            # Retrieve a tweet id from user to view all the comments for that tweet.
            selected_tweet_id = input("Enter the tweet ID to view/add comments (or hit Enter key to return to the main menu): ")
            cursor.execute('''SELECT tweet_content 
                           FROM tweets 
                           WHERE tweet_id = ?''', 
                           (selected_tweet_id,))
            selected_tweet = cursor.fetchone()
            # Retrieve all comments for the user inputted tweet id.
            if selected_tweet:
                print("\n", "Tweet: ", selected_tweet[0])
                # View the existing comments on selected tweet.
                cursor.execute('''SELECT user_profiles.username, comment_text 
                               FROM comments 
                               INNER JOIN user_profiles ON comments.user_id = user_profiles.user_id 
                               WHERE tweet_id = ?''', 
                               (selected_tweet_id,))
                existing_comments = cursor.fetchall()
                if existing_comments:
                    print("Comments:")
                    for comment in existing_comments:
                        print(comment[0], ":", emoji.emojize(comment[1]))
                else:
                    print("No comments yet.")
                # Allow the user to add a comment or return to main menu.
                comment_options = input("Add a new comment or type 'Return' to exit: ")
                if comment_options.upper() == "RETURN":
                    pass
                else:
                    # Add the user comments to the comments tables.
                    cursor.execute('''INSERT INTO comments (user_id, tweet_id, comment_text) 
                                   VALUES (?, ?, ?)''', 
                                   (current_userid, selected_tweet_id, comment_options))
                    conn.commit()
            else: # When a user enters a tweet id that doesn't exist.
                print("Tweet not found.")

    elif choice == 3: # Like and unlike a tweet.
        # Retrieving all liked tweets for the current user.
        cursor.execute('''SELECT tweets.tweet_id, tweet_content 
                       FROM user_profiles 
                       INNER JOIN likes_retweets ON user_profiles.user_id=likes_retweets.user_id 
                       INNER JOIN tweets ON likes_retweets.tweet_id = tweets.tweet_id 
                       WHERE user_profiles.username =? ''',
                       (username,))
        current_likes = cursor.fetchall()
        cursor.execute('''SELECT MAX(like_retweet_id) FROM likes_retweets''')
        newest_id = cursor.fetchone()
        if newest_id[0] is not None:
            newest_id = newest_id[0]+1
        elif newest_id[0] is None:
            newest_id = 1

        # Changing the retrieved data into list form for viewing
        tweet_ids = list()
        tweet_cont = list()
        tweet_likes = list()
        for tweet in current_likes:
            tweet_ids.append(tweet[0])
            tweet_cont.append(tweet[1])
            cursor.execute('''SELECT COUNT(tweet_id) 
                           FROM likes_retweets WHERE tweet_id =?''',
                           (tweet[0],))
            tweet_likes.append(cursor.fetchone()[0])

        
        # Retrieving all tweet ids to ensure a tweet exists later.
        cursor.execute('''SELECT tweet_id FROM tweets''') 
        id_list=cursor.fetchall()
        tweet_verification = list()
        for ids in id_list:
            tweet_verification.append(ids[0])


        while True:
            print("currently liked tweets:")
            # Printing all currently liked tweets.
            for tweet in range(len(tweet_ids)):
                print(tweet_ids[tweet], ":", tweet_cont[tweet])
                print(emoji.emojize(':thumbs_up:'), tweet_likes[tweet])
                time.sleep(pausetime)
            try:
                # User can either choose to like/unlike a tweet or return to the main menu.
                leave = input("Enter yes if you'd like to like/unlike a tweet or hit Enter key to return to main menu: ")
                if leave.upper() == "YES":
                    tweetToLike = int(input("Enter tweet id to like/unlike: "))
                    # If the tweet is already liked, give the user the option to unlike.
                    if tweetToLike in tweet_ids:
                        while True:
                            print("Are you sure you want to unlike that tweet?")
                            choice = input("yes/no: ")
                            # If the user unlikes the tweet, the database is updated.
                            if choice.upper() == "YES":
                                cursor.execute('''DELETE FROM likes_retweets WHERE user_id =? AND tweet_id=?''',
                                               (current_userid,tweetToLike))
                                unliked_id = tweet_ids.index(tweetToLike)
                                del tweet_ids[unliked_id]
                                del tweet_cont[unliked_id]
                                print("unliked")       
                                break  
                            elif choice.upper() == "NO":
                                break
                            else: 
                                print("please select yes or no")
                    
                    # Or if the tweet is not liked but exists, like it.
                    elif tweetToLike in tweet_verification: 
                        cursor.execute('''INSERT INTO likes_retweets (like_retweet_id, user_id, tweet_id) VALUES (?,?,?)''',
                                       (newest_id,current_userid,tweetToLike)) 
                        cursor.execute('''SELECT tweet_content 
                                       FROM tweets WHERE tweet_id = ?''',
                                       (tweetToLike,))
                        tweet_cont.append(cursor.fetchone()[0])
                        tweet_ids.append(tweetToLike)
                        newest_id +=1  
                    else:
                        print("Not an existing tweet")
                        time.sleep(pausetime)
                
                else:
                    print("returning to main menu")
                       
                conn.commit()
                time.sleep(pausetime)
                break
            
            except ValueError or TypeError:
                print("please enter a valid tweet id")

    # Code that handles if a user wishes to follow another user.
    elif choice == 4:
        # Ask the user for the username of the account they want to follow.
        UserToFollow = input("Enter username of user you wish to follow: ")
        # Handle case where the user tries to follow themselves.
        cursor.execute('''SELECT user_id 
                       FROM user_profiles 
                       WHERE username = ? AND user_id =?''', 
                       (UserToFollow, current_userid,))
        followingthemselves = cursor.fetchone()
        # If the query produced an output, that means they are trying to follow themselves.
        if followingthemselves: 
            print("Nice try! You can't follow yourself.")
            time.sleep(pausetime)
            pass
        else:
            # Retrieve the User ID of the user to follow from the user_profiles table
            cursor.execute('''SELECT user_id FROM user_profiles 
                           WHERE username = ? AND user_id != ?''', 
                           (UserToFollow, current_userid)) 
            user_id_to_follow = cursor.fetchone()
            # Check if the user is in the system.
            if user_id_to_follow is None:
                print("That user doesn't exist! Try again.")
                time.sleep(pausetime)
            else:
                # Check if the follow relationship already exists.
                user_id_to_follow = user_id_to_follow[0]
                cursor.execute('''SELECT * 
                               FROM followers_following 
                               WHERE follower_user_id = ? AND following_user_id = ?''', 
                               (current_userid, user_id_to_follow))
                existing_follow = cursor.fetchone()
                # If it returns an output, that means the follower/following relationship exists between the users already.
                if existing_follow is not None: 
                    print("You are already following this user")
                    time.sleep(pausetime)
                else:
                    # Checking/updating the follow_id pk val.
                    cursor.execute('''SELECT MAX(follow_id) FROM followers_following''')
                    follow_id = cursor.fetchone()
                    if follow_id[0] is not None:
                        follow_id = follow_id[0] + 1
                    else:
                        follow_id = 1
                    # Insert a new record into the follower_following table to record the user following an account.
                    cursor.execute('''INSERT INTO followers_following (follow_id, follower_user_id, following_user_id) 
                                   VALUES (?, ?, ?)''', (follow_id, current_userid, user_id_to_follow))
                    print("Followed!")
                    time.sleep(pausetime)
                    conn.commit()
    
    # Code that handles if a user wishes to unfollow another user.
    elif choice == 5:
        # ASk the user for the username of the account they wish to unfollow.
        UserToUnfollow = input("Enter username of user you wish to unfollow: ")

        # Retrieve the User ID of the user to follow from the user_profiles table
        cursor.execute('''SELECT user_id from user_profiles WHERE username =?''', 
                       (UserToUnfollow,))
        user_id_to_unfollow = cursor.fetchone()
         # Check if the user is in the system - if the previous query did not produce an output,
         # that means there is no user with that user id in the database.
        if user_id_to_unfollow is None:
            print("That user doesn't exist! Try again.")
            time.sleep(pausetime)
        else:
        # Check if the user is already NOT following the user they wish to unfollow.
            user_id_to_unfollow = user_id_to_unfollow[0]
            cursor.execute('''SELECT * FROM followers_following
                           WHERE follower_user_id = ? AND following_user_id = ?''', 
                           (current_userid, user_id_to_unfollow))
            notfollowing = cursor.fetchone()
            # If it does not return an output, that means they are already not following this person.
            if notfollowing is None: 
                print("You are already not following this user")
                time.sleep(pausetime)
            else:
                # Remove the association with the current user following the user that 
                # they want to unfollow by removing the record from the followers_following table
                cursor.execute('''DELETE FROM followers_following 
                               WHERE follower_user_id = ? AND following_user_id = ?''', 
                               (current_userid, user_id_to_unfollow))
                print("Unfollowed!")
                time.sleep(pausetime)
                conn.commit()

    # Code that allows users to view a list of their followers as well as who they are following.
    elif choice == 6:
        print("Do you want to view your followers or who you are following?")
        choice = input("Followers/Following: ")
        # If the user chooses to view their followers, query the database to pull 
        # the usernames where the logged on user_id matches the following_user_id in the followers_following table
        if choice.upper() == "FOLLOWERS":
            cursor.execute('''SELECT username 
                           FROM user_profiles 
                           INNER JOIN followers_following 
                           ON user_profiles.user_id = follower_user_id
                           WHERE following_user_id = ?''',
                           (current_userid,))
            followers = cursor.fetchall()
            print("\nFollowers:\n")
            # Print a list of all followers from the query output
            for follower in followers:
                print(follower[0])
            conn.commit()
            choice = input("\nHit Enter key to return to the main menu")
            # If the user chooses to view who they are currently following, 
            # query the database to pull the usernames where the logged on user_id
            # matches the follower_user_id in the followers_following table.
        elif choice.upper() == "FOLLOWING": 
            cursor.execute('''SELECT username 
                           FROM user_profiles 
                           INNER JOIN followers_following 
                           ON user_profiles.user_id = following_user_id 
                           WHERE follower_user_id = ?''', 
                           (current_userid,))
            following = cursor.fetchall()
            print("\nFollowing: \n")
            # Print the list of all usernames that the logged on user is following.
            for user in following:
                print(user[0])
            conn.commit()
            choice = input("\nHit Enter key to return to the main menu")
        # Handle case where user does not correctly type 'following' or 'followers'.
        else:
            print("That is not an option. Try again")
            time.sleep(pausetime)

    # Code that allows users to get more information regarding specific user menu options
    elif choice == 7:
        print("1. Will allow you to post a tweet to Twitterlike")
        print("2. Will show you all the tweets of people you're following with the newest first. It will also allow you to view and add comment on a specific tweet afterwards")
        print("3. Will show you all your currently liked tweets, then let you like or unlike a tweet")
        print("4. Will let you follow someone by entering their username")
        print("5. Will let you unfollow someone by entering their username")
        print("6. Will show you all your followers or people you're following")
        print("8. Will exit twitterlike,")
        print("9. Will show you all your tweets and let you comment on them too")
        print("Make sure you're entering the correct information, for example, if you're asked for a tweet id, enter a tweet id number")
        choice = input("\nHit Enter key to return to the main menu")

    # Allow a user to view their tweets.
    elif choice == 9:    
        print("\n")
        print(username,"'s Profile\n")
        # Retrieving all tweets logged in user has tweeted/interacted with in descending order of time stamp.
        cursor.execute('''SELECT user_profiles.username, tweets.tweet_id, tweets.tweet_content 
                       FROM tweets 
                       INNER JOIN user_profiles ON user_profiles.user_id = tweets.user_id 
                       WHERE user_profiles.user_id = ? 
                       ORDER BY tweets.tweet_id DESC ''',
                       (current_userid,))
        tweets = cursor.fetchall()
        # Creating the timeline.
        users = list()
        tweetid = list()
        tweetcontent = list()
        numberlikes = list()
        # Combining the retrieved columns into a list.
        for tweet in tweets:
            users.append(tweet[0])
            tweetid.append(tweet[1])
            tweetcontent.append(tweet[2])
        profile = [users,tweetid,tweetcontent]

        # If user hasn't tweeted yet: 
        if not tweets:
            print("Oh no! Looks like you haven't tweeted yet. Let's take you back to the main list so you can change that. Happy Tweeting!")
            time.sleep(5)
            pass
        # Retrieving the count of likes for all of user's tweets.
        else:
            for tweet in profile[1]:
                cursor.execute('''SELECT COUNT(tweet_id) 
                               FROM likes_retweets 
                               WHERE tweet_id =? ''',
                               (tweet,))
                numberlikes.append(cursor.fetchone()[0])
            profile.append(numberlikes)
            
            for tweet in range(len(profile[0])):
                print(profile[0][tweet],"( Tweet ID:",profile[1][tweet],")")
                print("   ",profile[2][tweet])
                print(emoji.emojize(':thumbs_up:'), profile[3][tweet], "\n")

            # Retrieving a tweet id from user to view all the comments for that tweet.
            view_tweets = input("Would you like to view a tweet in more detail? Enter Yes to view tweet. or enter anything else to return to main menu: ")
            if view_tweets.upper() == "YES": # user chooses to view tweet in more detail.
                try:
                    # Ask user for the tweet that they are interested in.
                    selected_tweet_id = input("Enter the tweet ID to view/add comments: ")
                    if int(selected_tweet_id) in tweetid:
                        cursor.execute('''SELECT tweet_content 
                                       FROM tweets WHERE tweet_id = ?''', 
                                       (selected_tweet_id,))
                        selected_tweet = cursor.fetchone()
                        # Retrieving all comments for the user inputted tweet id.
                        if selected_tweet:
                            print("\n", "Tweet: ", selected_tweet[0])
                            # View existing comments on selected tweet.
                            cursor.execute('''SELECT user_profiles.username, comment_text 
                                           FROM comments 
                                           INNER JOIN user_profiles ON comments.user_id = user_profiles.user_id
                                           WHERE tweet_id = ?''',
                                           (selected_tweet_id,))
                            existing_comments = cursor.fetchall()
                            if existing_comments:
                                print("Comments:")
                                for comment in existing_comments:
                                    print(comment[0], ":", emoji.emojize(comment[1]))
                            else:
                                print("No comments yet.")
                            # Allow a user to add a comment if they wish.
                            # Add a comment or return to main menu.
                            comment_options = input("Add a new comment or type 'Return' to exit: ")
                            if comment_options.upper() == "RETURN":
                                pass
                            else:
                                cursor.execute('''INSERT INTO comments (user_id, tweet_id, comment_text) 
                                               VALUES (?, ?, ?)''', 
                                               (current_userid, selected_tweet_id, comment_options))
                                conn.commit()
                        else: # When a user enters an invalid tweet id.
                            print("Tweet not found.")
                    else:
                        print("that's not one of your tweets")
                except ValueError or TypeError:
                    print("That is not a valid tweet id. Returning to main menu...")
                    time.sleep(pausetime)

    # Exits the code if the user wishes to exit
    elif choice == 8:
        conn.commit() # Commit all database changes.
        conn.close() # Close the database connection.
        print("Goodbye,", username)
        exit() # terminate the program.


