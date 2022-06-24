# Introduction to Data Warehoses

- [x] Data Warehouse: A Business Perspective
- [x] Data Warehouse: A Technical Perspective
- [x] Dimensional Modeling
- [x] DWH Architecture
- [x] OLAP Cubes
- [x] DWH Storage Technology
- [x] Terminology

## Data Warehouse: A Business Perspective

- You are in charge of a retailer's data infrustructure.
- Let's look at some business activities:
    - **Customers** should be able to find goods & make orders
    - **Inventory staff** should be able to stock, retrieve and re-order goods
    - **Delivery staff** should be able to pick up & deliver goods
    - **HR** should be able to assess the performance of sales staff
    - **Marketing** should be able to see the effect of different sales channels
    - **Management** should be able to monitor sales growth
- Ask yourself:
    - Can I build a database to support these activities?
    - Are all of the above questions of the same nature?

### DWH in a Business Context
- Retailer has a nation-wide presence -> Scale?
- Acquired smaller retailers, brick & mortar shops, online store -> Single database? Complexity?
- Has support call center & social media accounts -> Tabular data?
- Customers, Inventory staff and Delivery staff expect the system to be fast & stable -> Performance
- HR, Marketing & Sales reports want a lot information but have not decided yet on everything they need -> Clear requirements?
=> **Maybe one single relational database won't suffice.**

### Operational vs. Analytical Processes
A business is in general set of business processes. Here, we separate operational processes from analytical processes.

The motto of the operational processes is "make it work". We need to:
- find goods & make orders (for customers)
- stock and find goods (for inventory staff)
- pick up & deliver goods (for delivery staff)

In operational processes we don't care about the reporting or analytics or anything like that.

The motto of the analytical processes is "what's going on?". We need to:
- assess the performance of sales staff (for HR)
- see the effect of different sales channels (for marketing)
- monitor sales growth (for management)

### Same data source for operational & analytical processes?
Operational processes (Data in) -> Database -> Analytical processes (Data out).

Operational Databases:
- Excellent for operations
- No redundancy, high integrity
- Too slow for analytics, too many JOINS
- Too hard to understand

**Solution:** create 2 processing modes, create a system for them to co-exist.

> Data Warehouse is a system (including processes, technologies & data representations) that enables us to support analytical processes.

OLTP (Data in) -> DWH -> OLAP (Data out)

## Data Warehouse: A Technical Perspective

### Definitions
- A data warehouse is a copy of transaction data specifically structured for query and analysis.
- A data warehouse is a **subject-oriented**, **integrated**, **nonvolatile**, and **time-variant** collection of data in support of management's decision.
- A data warehouse is a system that **retrieves** and **consolidates** data **periodically** from the source systems into a **dimensional** or **normalized** data store. It usually **keeps years of history** and is **queried for business intelligence** or other **analytical activities**. It is typically **updated in batches**, not every time a transaction happens in the source system.

### DWH: Tech Perspective
The first activity in DWH would be to do ETL:
- **extract** the data from the source system used for operations,
- **transform** them,
- and **load** them into a dimensional model.

The **dimensional model** is designed to:
- make it **easy** for business users to work with the data,
- improve analytical **queries performance**.

The **technologies** used for storing dimensional models are **different** than traditional technologies.

Business-user-facing application are needed, with clear visuals, aka **Business Intelligence (BI) apps**.

### DWH Goals
- Simple to understand
- Performance
- Quality Assured
- Handles new questions well
- Secure

## Dimensional Modeling
### Facts & Dimensions
Fact tables:
- Record business events, like an order, a phone call, a book review
- Fact tables columns record events recorded in quantifiable **metrics** like quantity of an item, duration of a call, a book rating

Dimension tables:
- Record the context of the business events, e.g. who, what, where, why, etc.
- Dimension tables columns contain **attributes** like the store at which an item is purchased, or the customer who made the call, etc.

### Fact or Dimension Dilemma
- For facts, if you're unsure if a column is a fact or dimension, the simplest rule is that a fact is usually: **numeric & additive**.
- Examples facts:
    - A comment on an article represents an event but we can not easily make a statistic out of its content per se => not a good fact.
    - Invoice number is numeric but adding it does not make sense => not a good fact.
    - Total amount of an invoice could be added to compute total sales => a good fact.
- Examples dimensions:
    - Date & time are always a dimension.
    - Physical locations and their attributes are good candidates dimensions.
    - Human roles like customers and staff always good candidates for dimensions.
    - Goods sold always good candidates for dimensions.

### Naive ETL: from 3NF to ETL
- Query the 3NF Database (**extract**) and **transform**
    - join tables together
    - change types
    - add new columns
- Loading (**load**)
    - insert into facts & dimension tables

## DWH Architecture

### Kimball's Bus Architecture

#### ETL System:
- Transform from source to target.
- Conform dimensions.
- No user query support.

#### Presentation Area:
- **Dimensional**.
- **Atomic** & summary data. It means the dimensional model facts are not aggregated. We come to a number that we cannot divide further. We can pre-aggregate it but the atomic level has to be always there in case we need to go to the lowest level.
- Organized by business process.
- **Uses conformed dimensions**. It means that we try to generalize and build all the dimensions in a way that is usable by the whole organization. It needs some careful designe to be able to do something like that.

#### Design Goals:
- Ease of use.
- Query performance.

#### Kimball's Bus Matrix
We actually go and give to users what's known as the bus matrix indicating for each business process it's going to use which dimensions.
|Business processes|Date|Product|Warehouse|Store|Promotion|Customer|Employee|
|--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|Issue purchase order|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|  |  |  |  |
|Receive warehouse deliveries|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|  |  |  |:heavy_check_mark:|
|Store inventory|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|  |  | |
|Retail sales|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|
|...| | | | | | | |

#### ETL: A Closer Look
- Extracting:
    - Get the data from its store.
    - Possibly deleting old state.
- Transforming:
    - Integrates many sources together.
    - Possibly cleansing: inconsistencies, duplication, missing values, etc.
    - Possibly producing diagnostic metadata.
- Loading:
    - Structuring and loading the data into the dimensional data model.

### Independent Data Marts

- Departments have independent ETL processes & dimensional models.
- These **separate & smaller** dimensional models are called **Data Marts**.
- Different fact tables for the same events, **no conformed dimensions**.
- Uncoordinated efforts can lead to **inconsistent views**.
- Despite awareness of the emergence of this architecture from departmental autonomy, it is **generally discouraged**.

### Inmon's Corporate Information Factory (CIF)

- Two ETL processes:
    - Source systems -> 3NF DB, an improved copy of reality with the same model.
    - 3NF DB -> Departmental Data Marts. These data marts are not uncoordinated because they have one baseline.
- The 3NF DB acts an enterprise wide data store.
    - Single integrated source of truth for data marts.
    - Could be accessed by end-users if needed
- Data marts dimensionally modelled & unlike Kimball's dimensional models, they are mostly aggregated.

> CIF build on a 3NF normalized database and then allow for documented data denormalization for Data Marts.

### Hybrid Kimball Bus & CIF

This approach is the combination of Kimball model and Inmon model (CIF). It contains 2 ETL processes:
- Source systems -> 3NF DB
- 3NF DB -> do conformed dimensions instead of data marts.

## OLAP Cubes

An OLAP cube is an aggregation of a fact metric on a number of dimensions. E.g. Movie, Branch, Month
- Easy to communicate to business users.
- Common OLAP operations include: Rollup, drill-down, slice, and dice.

### Roll-up & Drill Down
- **Roll-up**: aggregates or combines values and reduces number of rows or columns. For example, from *branch* dimension, we group all the cities and sum up the sales of each city by Country: e.g. US, France (less columns in branch dimension). With that, we have roll up the branch dimension.
```SQL
# query calculates revenue (sales_amount) by day, rating,  and
# country

SELECT day, rating, country, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimmovie m ON (f.movie_key = m.movie_key)
JOIN dimcustomer c ON (f.customer_key = c.customer_key)
GROUP BY (day, rating, country)
ORDER BY revenue DESC
LIMIT 20;
```
- **Drill Down**: decomposes values and increases number of rows or columns. For example, decomposing the sales of each city into smaller districts (more columns in branch dimension). For example, we take a city and decompose it to district.
```SQL
# query calculates revenue (sales_amount) by day, rating, and 
# district (city is broken up into districts).

SELECT day, rating, district, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimmovie m ON (f.movie_key = m.movie_key)
JOIN dimcustomer c ON (f.customer_key = c.customer_key)
GROUP BY (day, rating, district)
ORDER BY revenue DESC
LIMIT 20;
```
- With roll-up we have fewer values, and with drill down we have more values.
- The OLAP cubes should store the finest grain of data (atomic data), in case we need to drill-down to the lowest level, e.g. Country -> City -> District -> Street, etc.

### Slice & Dice
- **Slice**: reducing N dimensions to N-1 dimensions by restricting one dimension to a single value. E.g. *month* is `mar`.
```SQL
# query calculates the revenue (sales_amount) by day, rating, city 
# reducing the dimensionality of the results by limiting it to 
# only include movies with a `rating` of "PG-13"

SELECT day, rating, city, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimmovie m ON (f.movie_key = m.movie_key)
JOIN dimcustomer c ON (f.customer_key = c.customer_key)
WHERE m.rating = 'PG-13'
GROUP BY (day, rating, city)
ORDER BY revenue DESC, day ASC
LIMIT 20;
```
- **Dice**: same dimensions but computing a sub-cube by restricting the range of values (some of values of the dimensions). E.g. *month* in `['feb', 'mar']` and *movie* in `['avatar', 'batman']` and *branch* is `NY`.
```SQL
# query creates a subcube of the initial cube (3 dimensions: day, 
# rating, city) that includes movies with:
# - ratings of PG or PG-13
# - in the city of Bellevue or Lancaster
# - day equal to 1, 15, or 30

SELECT day, rating, city, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimmovie m ON (f.movie_key = m.movie_key)
JOIN dimcustomer c ON (f.customer_key = c.customer_key)
WHERE m.rating IN ('PG','PG-13') AND c.city IN ('Bellevue', 'Lancaster') AND d.day IN (1, 15, 30)
GROUP BY (day, rating, city)
ORDER BY revenue DESC, day ASC
LIMIT 20;
```

### Query Optimization
- Business users will typically want to slice, dice, roll-up and drill down all the time.
- Each sub combination will potentially go through all the facts table (suboptimal).
```SQL
# query calculates total revenue at the various grouping levels
# (total, by month, by country, by month & country) all at once

SELECT month, country, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimstore s ON (f.store_key = s.store_key)
GROUP BY GROUPING SETS ((), month, country, (month, country));
```
- The **GROUP by CUBE (movie, branch, month)** will make **one pass through the facts** table and will aggregate all possible combinations of groupings, of length 0, 1, 2 and 3. E.g:
    - total revenue.
    - revenue by movie/ branch/ month.
    - revenue by movie, branch/ branch, month/ month, movie.
    - revenue by movie, branch, month.
```SQL
# query calculates the various levels of aggregation done in the 
# grouping sets exercise (total, by month, by country, by month &
# country) using the CUBE function.

SELECT month, country, sum(sales_amount) as revenue
FROM factsales f
JOIN dimdate d ON (f.date_key = d.date_key)
JOIN dimstore s ON (f.store_key = s.store_key)
GROUP BY CUBE (month, country);
```
- Saving/Materializing the output of the CUBE operation and using it is usually enough to answer all forthcoming aggregations from business users without having to process the whole facts table again.

> GROUPING SETS and CUBE produce queries that are shorter to write, easier to read, and **more performance** (up to 45 times) than the naive query using UNION of GROUP BYs.

## DWH Storage Technology

> OLAP cubes is a very convenient way for slicing, dicing and drilling down. How do we serve these OLAP cubes?

- Multi-dimensional OLAP (**MOLAP**): **Pre-aggregate** the OLAP cubes and saves them on a special purpose non-relational database. This is **traditional approach**.
- Relational OLAP (**ROLAP**): Compute the OLAP cubes **on the fly** from the existing relational databases where the dimensional model resides. This is more kind of **popular approach right now**.

### Columnar Format
- Data is stored in rows and not columns.
- When we load data from disk, we load one column. 
- We consume way less memory, and let alone accessing the disk.
- We don't need to load the whole row to be able to get one value from it.

> Columnar storage is faster than naive storage.

```SQL
# load cstore_fdw extension
CREATE EXTENSION cstore_fdw;

# create c-store server
CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;

# create foreign table
CREATE FOREIGN TABLE customer_reviews_col
(
    customer_id TEXT,
    review_date DATE,
    review_rating INTEGER,
    review_votes INTEGER,
    review_helpful_votes INTEGER,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategory TEXT,
    similar_product_ids CHAR(10)[]
)
SERVER cstore_server
OPTIONS(compression 'pglz');

# insert database to table
COPY customer_reviews_col FROM '/tmp/customer_reviews_1998.csv' WITH CSV;
COPY customer_reviews_col FROM '/tmp/customer_reviews_1999.csv' WITH CSV;

# query to test
SELECT product_title, AVG(review_rating) as avg_rating
FROM customer_reviews_row
WHERE review_date >= '1995-01-01' AND review_date <= '1995-12-31'
GROUP BY product_title
ORDER BY avg_rating DESC
LIMIT 20;
```

> Do not use function in WHERE clause, it will take much time to execute.

## Terminology

1. **DWH**: Data Warehouse
2. **OLTP**: Online Transactional Processing
3. **OLAP**: Online Analytical Processing
4. **ETL**: Extract Transform Load