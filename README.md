# Project Title

#### This is Project \#3 in the Udacty Full Stack Nanodegree Program
It is written to perform a log analysis on a provided SQL database, simulating logs for a newspaper website.

`Catalog.py` is a python script performs analysis on the news SQL database. It answers the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started

This project is a python script. Running the `catalog.py` file by navigating to its directory and typing `python catalog.py` will output the results to the command line.
### Prerequisites

This project uses the `psycopg2` module to interpret the SQL database.
It interacts with PostgresSQL which needs to be installed.
The news database needs to be available locally.

The queries in the python script make use of the following view, which will need to be created in your database by copying and pasting the code below into your `psql` prompt:
```
create view author_rank as
    select articles.author as author_id, sum(subq.hits) as hits
        from articles,
        (
--Match log.path to article.slug and attach number of hits to each
            select substring(path, 10, 100) as slug, count(path) as hits
            from log
--Omit 404s
            where status = '200 OK'
            group by path
--Omit root
            offset 1
        ) as subq
        where articles.slug = subq.slug
        group by articles.author
        order by hits desc;
```
## Installation

The parameters of the project assume the presence of Python, PostgresSQL, the psycopg2 python module, and the news SQL database on your local machine. Once the view above is created in your psql prompt, simply run the script.

## Authors

* **Terence Fox**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
