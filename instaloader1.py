import instaloader
from datetime import datetime, timedelta

L = instaloader.Instaloader()

def post_timeframe_filter(post, since, until):
    posttime = post.date_local.timestamp()
    return posttime > since and posttime < until

# n is the max number of posts to consider
# send in since, until params as timestamp()
def download_posts_in_timeframe(n, since, until, profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()
    for i in range(n):
        next_post = posts.__next__()
        if (post_timeframe_filter(next_post, since, until)):
            L.download_post(next_post, target=profile_name)

# download_posts_in_timeframe(10, (datetime.now() - timedelta(hours=1)).timestamp(), datetime.now().timestamp(), "sportscenter")

# find number of pinned posts by seeing the discrepancy between sooner posts and later
# on the unfortunate edge case that they pin a more recent post, it shouldn't really matter b/c we want
# the most recent post anyways
def get_number_of_pinned_posts(username):
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()
    dates = []
    n = 4 # max number of pinned posts is 3
    # get original set of dates
    for i in range(n):
        next_post = posts.__next__()
        dates.append(next_post.date_local.timestamp())
    # print(find_inversion_point(dates))
    return find_inversion_point(dates)

def find_inversion_point(dates):
    for i in range(1, len(dates)):
        print("first date")
        print(dates[i-1])
        print("second date")
        print(dates[i])
        if dates[i-1] < dates[i]:
            return i
    return -1  # Return -1 if no such point is found

# TODO: edge case of only pinned posts
def download_latest_post(profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()

    pinned_count = get_number_of_pinned_posts(profile_name)
    print(pinned_count)
    # should get first post
    if (pinned_count == -1):
        L.download_post(posts.__next__(), target=f"{profile_name}_recentpost")
    else:
        for i in range(pinned_count):
            posts.__next__()
        L.download_post(posts.__next__(), target=f"{profile_name}_recentpost")

# download_latest_post("drake.maye")

# downloads most recent (most recently visible on profile)
# excludes pinned posts if specified
def download_latest_n_posts(n, include_pinned, profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()

    # it is more expensive to get the total count of posts, so safeguarding all calls w/ try catch
    #if (len(posts) < n):
       # print(f"user {profile_name} does not have {n} posts! Grabbing the all available posts instead.")
       # n = len(posts)

    if (not include_pinned):
        pinned_count = get_number_of_pinned_posts(profile_name)
        for i in range(pinned_count):
           posts.__next__()
        for i in range(n):
            # safeguarding edge case where number of regular posts + pinned posts > n
            try:
                L.download_post(posts.__next__(), target=profile_name)
            except:
                break
    else:
        for i in range(n):
            try:
                L.download_post(posts.__next__(), target=profile_name)
            except:
                break

download_latest_n_posts(7, True, "yeat")