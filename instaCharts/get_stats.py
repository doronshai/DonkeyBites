#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import sys, os
import sqlite3, logging
from os.path import exists as path_exists
from os.path import isfile as file_exists
from os.path import sep as native_slash

from database_engine import get_database
from settings import Settings
from exceptions import InstaPyError

def save_account_progress(username, followers, following, posts, logger):
    """
    Check account current progress and update database

    Args:
        :username: Account to be updated
        :logger: library to log actions
    """
    logger.info('Saving account progress...')

    try:
        # DB instance
        db, id = get_database()
        conn = sqlite3.connect(db)
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql = ("INSERT INTO accountsProgress (profile_id, followers, "
                   "following, total_posts, created, modified) "
                   "VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S'), "
                   "strftime('%Y-%m-%d %H:%M:%S'))")
            cur.execute(sql, (id, followers, following, posts))
            conn.commit()
    except Exception:
        logger.exception('message')

# def getTotalFollowers(api, user_id):
#     """
#     Returns the list of followers of the user.
#     It should be equivalent of calling api.getTotalFollowers from InstagramAPI
#     """

#     followers = []
#     next_max_id = True
#     while next_max_id:
#         # first iteration hack
#         if next_max_id is True:
#             next_max_id = ''

#         _ = api.getUserFollowers(user_id, maxid=next_max_id)
#         followers.extend(api.LastJson.get('users', []))
#         next_max_id = api.LastJson.get('next_max_id', '')
#     return followers

def get_instapy_logger(show_logs):
    """
    Handles the creation and retrieval of loggers to avoid
    re-instantiation.
    """

    existing_logger = Settings.loggers.get(username)
    if existing_logger is not None:
        return existing_logger
    else:
        # initialize and setup logging system for the InstaPy object
        logger = logging.getLogger(username)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(
            '{}general.log'.format(logfolder))
        file_handler.setLevel(logging.DEBUG)
        extra = {"username": username}
        logger_formatter = logging.Formatter(
            '%(levelname)s [%(asctime)s] [%(username)s]  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(logger_formatter)
        logger.addHandler(file_handler)

        if show_logs is True:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logger_formatter)
            logger.addHandler(console_handler)

        logger = logging.LoggerAdapter(logger, extra)

        Settings.loggers[username] = logger
        Settings.logger = logger
        return logger

def get_logfolder(username, multi_logs):
    if multi_logs:
        logfolder = "{0}{1}{2}{1}".format(Settings.log_location,
                                          native_slash,
                                          username)
    else:
        logfolder = (Settings.log_location + native_slash)

    validate_path(logfolder)
    return logfolder

def validate_path(path):
    """ Make sure the given path exists """

    if not path_exists(path):
        try:
            os.makedirs(path)

        except OSError as exc:
            exc_name = type(exc).__name__
            msg = ("{} occured while making \"{}\" path!"
                   "\n\t{}".format(exc_name,
                                   path,
                                   str(exc).encode("utf-8")))
            raise InstaPyError(msg)

if __name__ == "__main__":

    usersdetails = [(1111,'aaaaaa'), (22222,'bbbbb'), (33333,'ccccc'), (44444,'ddddd')]
    for username, password in usersdetails:
        Settings.profile["name"] = username

        api = InstagramAPI(username,password)
        api.login()

        multi_logs=True
        show_logs=True
        logfolder = get_logfolder(username, multi_logs)
        logger = get_instapy_logger(show_logs)

        # user_id = '1461295173'
        user_id = api.username_id

        # List of all followers
        followers = api.getTotalFollowers(user_id)
        following = api.getTotalFollowings(user_id)
        posts = api.getTotalUserFeed(user_id)
        print(len(followers))
        print(len(following))
        print(len(posts))
        
        save_account_progress("yoav.shai.2010", followers, following, posts, logger)

        # orig_stdout = sys.stdout
        # f = open('out.txt', 'w')
        # sys.stdout = f
        # print(followers)
        # sys.stdout = orig_stdout
        # f.close()