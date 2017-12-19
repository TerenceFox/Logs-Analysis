#!/usr/bin/env python

import psycopg2

DBNAME = 'news'

# Returns Question 1 of Log Analysis: Top three articles of all time, ranked by
# number of pageviews.


def question_1():
    """Sends a select query to the database and returns tuples of
    article titles and their pageviews. See comments in SQL for more detail.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT articles.title, subq.hits
        FROM articles,
        (
        --Group pageviews according to their slug, then sort, omitting root
            SELECT log.path AS slug, COUNT(log.path) AS hits
            FROM log
        --Omit 404s
            WHERE status = '200 OK'
            GROUP BY path
            ORDER BY hits DESC
        --Omit root
            OFFSET 1
        ) AS subq
        WHERE articles.slug = SUBSTRING(subq.slug, 10, 100)
        LIMIT 3;
    """)
    db.close()
    return c.fetchall()



# Returns Question 2 of Log Analysis: The article authors, ranked in
# descending order by pageview.


def question_2():
    """Sends a select query to the database and returns tuples of article
    authors and their total pageviews, ranked. See the README file for the
    view that this query utilizes.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT authors.name, author_rank.hits
            FROM authors, author_rank
            WHERE authors.id = author_rank.author_id;
    """)
    db.close()
    return c.fetchall()



# Returns Question 3 of Log Analysis: On which days did more than 1% of
# requests lead to errors?


def question_3():
    '''Sends a select query to the database that returns tuples of the
    timestamp of days with >1% error rate and the error rate. See SQL comments
    below for more detail.
    '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT good.log_d, round(((((error.http+0.0) / (good.http+0.0)))*100),
        2) AS error_rate
            FROM
        -- Count instances of 200 responses in each day.
                (
                SELECT count(*) AS http, date_trunc('day', TIME) AS log_d
                FROM log
                WHERE status = '200 OK'
                GROUP BY log_d
                ORDER BY log_d
            ) AS good JOIN
        --Count instances of 404 responses in each day.
                (
                SELECT count(*) AS http, date_trunc('day', TIME) AS log_d
                FROM log
                WHERE status = '404 NOT FOUND'
                GROUP BY log_d
                ORDER BY log_d
            ) AS error
            ON good.log_d = error.log_d
        -- Only return error rates equal to or above 1 percent.
            WHERE error.http >= (good.http/100);
        """)
    db.close()
    return c.fetchall()



# This section will display to the user with the results of the queries.
print('''\nHello newspaper peon. Here is the data you asked for.
\n \n
''')

# Display answer to Question 1
print('''Here are the top three authors by pageview:
-------------------------------------------
''')

for i in question_1():
    print('"{}" \u2014 {} views'.format(str.title(i[0]), str(i[1])))

print('\n')

# Display answer to Question 2
print('''Here are the authors ranked by all-time pageviews:
--------------------------------------------------
''')

for i in question_2():
    print("{} \u2014 {} views".format(i[0], i[1]))

print('\n')

# Display answer to Question 3
print('''Here are the days in which more than 1% of requests created errors:
-------------------------------------------------------------------
''')

for i in question_3():
    error_date = i[0]
    error_rate = i[1]
    print(
        "{}  {}% error rate".format(error_date.strftime("%B %e %Y"),
                                    error_rate)
        )

print('\n\nWell, off I go!')
