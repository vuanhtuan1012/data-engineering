# NoSQL Data Models

- [x] [Non-Relational Databases](#non-relational-databases)
- [x] [Distributed Databases](#distributed-databases)
- [x] [The CAP theorem](#the-cap-theorem)
- [x] [Importance of Denormalization](#importance-of-denormalization)
- [x] [Cassandra Query Language: CQL](#cassandra-query-language-cql)
- [x] [Primary Key, Partition Key, and Clustering Column](#primary-key-partition-key-and-clustering-column)
- [x] [WHERE clause](#where-clause)
- [x] [Terminology](#terminology)
- [x] [Reference](#reference)

> Jupyter notebooks are in files with prefix `L3_`

## Non-Relational Databases

> NoSQL and Non-Relational are interchangeable terms: NoSQL = Not Only SQL

**When to Use NoSQL:**
- need high availability: indicates the system is always up and there is no downtime.
- have large amounts of data
- need linear scalability: the need to add more nodes to the system so performance will increase linearly.
- low latency: shorter delay before the data is transferred once the instruction for the transfer has been received.
- need fast reads and write

**Apache Cassandra:**
- Open Source NoSQL Database
- Masterless Architecture
- High Availability
- Linearly Scalable
- Used by Uber, Netflix, Twitter, etc.

## Distributed Databases

**Distributed database** is a database that has been scaled out horizontally. It's not just a single system but a dabase made up of multiple machines.

> In a **distributed database**, in order to have high availability, you will need copies of your data.

**High availability** means the system is always up and there's no down time, or very little downtime but essentially no downtime.

In distributed system, data cannot just live in one place. With the fact that the data is copied throughout the system leads to the fact that the data may not be up to date in all locations. This is called eventual consistency.

**Eventual consistency** is a consistency model used in distributed computing to achieve **high availability** that informally guarantees that, **if no new updates** are made to a given data item, eventually all accesses to that item will **return the last updated value**.

This means that if there are new changes, the value of my data I should say, maybe different in different locations.

- We are talking about miliseconds that the data may be in fact inconsistent.
- There are workarounds to prevent getting stale data. That are outside the scope of this course but rest assure they've been put in place to prevent issues.

## The CAP theorem

The CAP theorem states that it is impossible for a distributed data store to simultaneously provide more than two out of the following guarantees:
- **Consistency:** every read from the database get the latest piece of data or an error.
- **Availability:** every request is received and a response is given without a guarantee that the data is the latest update.
- **Partition tolerance:** the system continues to work regardless of losing network connectivity between nodes.

It means that when the system is running fine, no network failure, we can also have availability and consistency. But when the system has network failures, then we may only have consistency or availability.

Apache Cassandra and other NoSQL databases choose to be highly available at the potential cost of consistency. It is an AP (Availability and Partition tolerance) database.

**Is Eventual Consistency the opposite of what is promised by SQL database per the ACID principle?**

Much has been written about how _Consistency_ is interpreted in the ACID principle and the CAP theorem.
- Consistency in the ACID principle refers to the requirement that only transactions that abide by constraints and database rules are written into the database, otherwise the database keeps previous state. In other words, the data should be correct across all rows and tables.
- However, consistency in the CAP theorem refers to every read from the database getting the latest piece of data or an error.

**Which of these combinations is desirable for a production system - Consistency and Availability, Consistency and Partition Tolerance, or Availability and Partition Tolerance?**

As the CAP Theorem Wikipedia entry says, "The CAP theorem implies that in the presence of a network partition, one has to choose between consistency and availability." So **there is no such thing as Consistency and Availability in a distributed database** since it must always tolerate network issues. You can **only have** Consistency and Partition Tolerance (CP) or Availability and Partition Tolerance (AP).

Remember, relational and non-relational databases do different things, and that's why most companies have both types of database systems.

**Does Cassandra meet just Availability and Partition Tolerance in the CAP theorem?**

According to the CAP theorem, a database can actually only guarantee two out of the three in CAP. So supporting Availability and Partition Tolerance makes sense, since Availability and Partition Tolerance are the biggest requirements.

**If Apache Cassandra is not built for consistency, won't the analytics pipeline break?**

If I am trying to do analysis, such as determining a trend over time, e.g., how many friends does John have on Twitter, and if you have one less person counted because of "eventual consistency" (the data may not be up-to-date in all locations), that's OK.

In theory, that can be an issue but only if you are not constantly updating. If the pipeline pulls data from one node and it has not been updated, then you won't get it. Remember, in Apache Cassandra it is about  **Eventual Consistency**.

## Importance of Denormalization

The biggest take away when doing data modeling in Apache Cassandra is to **think about the queries first**. There are **no JOINS** in Apache Cassandra.

> Normalized tables in relational database will need to go through the process of denormalization to be able to fit into the Apache Cassandra data model.

**Data modeling** in Apache Cassandra:
- Denormalization is not just okay, it's a must. There are no joins in Apache Cassandra. We can **only query on one table at a time**.
- Denormalization must be done for fast reads. Apache Cassandra has been optimized for writes, so no concern about duplicate data.
- Think queries first.
- No JOINS.
- One table per queries is a great strategy.

**Relational database vs. Apache Cassandra:**
- In a relational database, one query can access and join data from multiple tables.
- In Apache Cassandra, the queries can only access data from a single table.

**I see certain downsides of this approach, since in a production application, requirements change quickly and I may need to improve my queries later. Isn't that a downside of Apache Cassandra?**

In Apache Cassandra, you want to model your data to your queries, and if your business need calls for quickly changing requirements, you need to create a new table to process the data. That is a requirement of Apache Cassandra.

If your business needs calls for ad-hoc queries, these are not a strength of Apache Cassandra. However keep in mind that it is easy to create a new table that will fit your new query.

## Cassandra Query Language: CQL

Cassandra query language (CQL) is the way to interact with the database and is very similar to SQL.

`JOINS`, `GROUP BY`, or subqueries are not in CQL and are not supported by CQL.

## Primary Key, Partition Key, and Clustering Column

### Primary Key
- The PRIMARY KEY is how each row can be uniquely identified and how the data is distributed across the nodes (or servers) in our system.
- The **first element** of the PRIMARY KEY is the PARTITION KEY (which will determine the distribution).
- The PRIMARY KEY is made up of either just the PARTITION KEY or with the addition of CLUSTERING COLUMNS. The PARTITION KEY will determine the distribution of data across the system.
- The partition key's row value will be hashed (turned into a number) and stored on the node in the system that holds that range of values.

```SQL
CREATE TABLE music_library(
year int,
artist_name text,
album_name text,
PRIMARY KEY (year)
)
```
In the example above PRIMARY KEY is a simple key `year`. It's also PARTITION KEY. So, data will be distributed across the system by the year.

### Key Points about Primary Key
- Must be unique to each row. Data will be overwritten if a new value comes in with the same primary key. An **error will not be thrown** and the original data will be overwritten.
- Hashing of this value results in placement on a particular node in the system. The value will be hashed to a numeric value and the value will determine whether data will live on the system.
- Data distributed by this partition key. The data will be distributed across the system by this key.
- Simple or composite.
    - The simple primary key is just one column that is also the partition key.
    - A composite primary key is made up of more than one column and will assist in creating a unique value and will help in getting your retrieval queries.
    - May have one or more clustering columns.

```SQL
CREATE TABLE music_library(
year int,
artist_name text,
album_name text,
PRIMARY KEY (year, artist_name)
)
```
In the example above PRIMARY KEY is a composite key with PARTITION KEYS: `year`, `artist_name`.

### Clustering Columns
The PRIMARY KEY is made up of either just the PARTITION KEY or with the addition of CLUSTERING COLUMNS. The CLUSTERING COLUMNS will determine the sort order within a Partition.

- The clustering column will sort the data in sorted **ascending** order, e.g., alphabetical order.
- More than one clustering column can be added (or none!).
- From there the clustering columns will sort in order of how they were added to the primary key.

```SQL
CREATE TABLE music_library(
year int,
artist_name text,
album_name text,
PRIMARY KEY ((year), artist_name, album_name)
)
```
In the example above PRIMARY KEY is a composite key with PARTITION KEY `year` and CLUSTERING COLUMNS: `artist_name`, `album_name`.

## WHERE clause

- Data modeling in Apache Cassandra is query focused, and that focus needs to be on WHERE caluse.
- The PARTITION KEY must included in your query and any CLUSTING COLUMNS can be used in the order they appear in PRIMARY KEY.

**Notice:**
- fields in WHERE clause **have to be in order** that they appear in PRIMARY KEY. It means if we have primary keys are `year, album_name` this WHERE clause will result an error `WHERE album_name='Let It Be'`, but these WHERE clauses work well `WHERE year=1970`, `WHERE year=1970 and album_name='Let It Be'`.
- text in WHERE clause is put in single quotation-marks `'`, not in double quotation-marks `"`.
- fields not in PRIMARY KEY can't be in WHERE, ORDER BY clauses.
- if a field in PRIMARY KEY appears in WHERE clause, it has to appear after fields which are before it in PRIMARY KEY.
- Failure to include a WHERE clause will result in an error.

> The WHERE clause must be included to execute queries.

It is recommended that one partition be queried at a time for performance implications.

### SELECT * FROM table
It is possible to do a `select * from` table if we add a configuration `ALLOW FILTERING` to the query. This is risky, but available if absolutely necessary. This should be done with extreme caution.

NoSQL is all about big data and high-performance. Thounsands of nodes systems exist of Apache Cassandra and `select *` on that system will be trying to pull all the data to the client from thousands of nodes. This is called a full table scan. Best case, it'd be extremely slow. Worst case, it could bring down the system. Adding the WHERE clause we'll make sure this doesn't happen and we're serving the requests with low latency and high performance.

**Notice:** AVOID using `ALLOW FILTERING`.

**Why do we need to use a  `WHERE`  statement since we are not concerned about analytics? Is it only for debugging purposes?**

The `WHERE` statement is allowing us to do the fast reads. With Apache Cassandra, we are talking about big data -- think terabytes of data -- so we are making it fast for read purposes.

Data is spread across all the nodes. By using the `WHERE` statement, we know which node to go to, from which node to get that data and serve it back. For example, imagine we have 10 years of data on 10 nodes or servers. So 1 year's data is on a separate node. By using the `WHERE year = 1` statement we know which node to visit fast to pull the data from.

## Terminology
1. **ACID**: refers to the four key properties of a transaction: atomicity, consistency, isolation, and durability.

## Reference
1. [NoSQL Databases Overview, Types and Selection Criteria](https://www.xenonstack.com/blog/nosql-databases/)
2. [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)
3. [ACID properties of transactions](https://www.ibm.com/docs/en/cics-ts/5.4?topic=processing-acid-properties-transactions)
4. [Discussion about ACID vs. CAP](https://www.voltdb.com/blog/2015/10/22/disambiguating-acid-cap/)
5. [Data modeling concepts](https://docs.datastax.com/en/dse/6.7/cql/cql/ddl/dataModelingApproach.html)
6. [Primary Keys](https://docs.datastax.com/en/cql/3.3/cql/cql_using/useSimplePrimaryKeyConcept.html#useSimplePrimaryKeyConcept)
7. [Composite Partition Keys](https://docs.datastax.com/en/cql/3.3/cql/cql_using/useCompoundPrimaryKeyConcept.html)
8. [Difference between Partition Keys and Clustering Keys](https://stackoverflow.com/questions/24949676/difference-between-partition-key-composite-key-and-clustering-key-in-cassandra)
9. [ALLOW FILTERING explanation](https://www.datastax.com/dev/blog/allow-filtering-explained-2)