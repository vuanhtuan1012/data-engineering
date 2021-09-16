# Implementing DWH on AWS

- [x] Why DWH on AWS
- [x] Amazon Redshift
- [x] General ETL Concepts
- [x] ETL for Redshift
- [x] Building a Redshift Cluster
- [x] Optimizing Redshift Table Design
- [x] Terminology

## Why DWH on AWS

### On-Premise vs. Cloud

**On-Premise:**
- Heterogeneity, scalability, elasticity of the tools, technologies, and processes.
- Need for diverse IT staff skills & multiple locations.
- Cost of ownership.

**Cloud:**
- Lower barrier to entry.
- May add as you need. It's ok to change your opinion.
- Scability & elasticity out of the box. We can add/remove resources.
- Operational cost might be high and heterogeneity/complexity won't disappear because we went through the cloud.

### DWH Dimensional Model Storage on AWS

**Cloud-Managed** (Amazon RDS, Amazon DynamoDB, Amazon S3):
- Re-use of expertise.
- The way less IT staff for security, upgrades, etc.
- The way less OpEx.
- Deal with complexity with techniques like *infrastructure as code*.

**Self-Managed** (EC2 + Postgresql, EC2 + Cassandra, EC2 + Unix FS): Always *catch-all* option if needed.

On AWS, there are 2 products to manage SQL way for DWH storage: AWS RDS (Relational Data Store) and Amazon Redshift (SQL Columnar Massively Parallel).

## Amazon Redshift

### Technology
- **Column-oriented storage.** The idea of column-oriented is that we have ability of accessing one column and doing one aggregation operation on it. That's very nice because sometimes that could be a big fact. There're lot of column, we try to look for one column, we don't want actually to look for the other columns. So, that actually works out as a very nice performance boost.
- **Best suited for storing OLAP workloads**, summing over a long history.
- Internally, it's a modified Postgresql.

**Concurrence**
- Most relational databases execute multiple queries in parallel if they have access to many cores/servers.
- However, every query is always executed on **a single CPU of a single machine**. So, at a point in time, we have one query running, it doesn't matter how many CPUs we have because it always going to run on one CPU. If we have lots of concurrent users running those queries, we can schedule those ones on the CPU.
- That's actually very nice for OLTP because indeed, we **have a lot of concurrent users** and each query on **itself is not long**. It's either like an update or a few rows retrieved. It's actually **well suited for OLTP**.
- **Massively Parallel Processing** (MPP) databases **parallelize the execution of one query on multiples CPUs/machines**. The idea of the MPP databases is that a table is partitioned into smaller partitions and distributed across CPUs where actually each CPU would also have its associated storage. So, when a query comes, that query can process this whole table in parallel where each CPU would be basically crunching one partition of the data.
- Amazon Redshift is a cloud-managed, column-oriented, MPP database.

### Architecture
- A **Readshift is actually a cluster** and the cluster **would be composed of** one leader node and one or more compute nodes.
- Leader node:
    - **handles external communication**. The leader node is the one actually which interacts with the outside world. All client applications actually talk to the leader node using protocols like JDBC or ODBC like any other normal database.
    - coordinates compute nodes.
    - **optimizes query execution**. It puts a plan on what goes where and how compute nodes should work together.
- Compute Nodes:
    - Each with own CPU, memory, and disk (determined by the node type).
    - Scale up: get more powerful nodes.
    - Scale out: get more nodes.
    - Each compute node is logically divided into a number of slices.
- Node Slices:
    - can be considered as a CPU with dedicated storage and memory for the slice.
    - A cluster with N slices can process N partitions of tables simultatneously. **It doesn't matter these slices are on one machine or many machines**. We think of the sum of all slices across all compute nodes and that would be our unit for parallelization.
    - The total number of slices in a cluster is our unit of parallelism and it is equal to the sum of all slices on the cluster.
- The total number of nodes in a Redshift cluster is equal to the number of AWS EC2 instances used in the cluster. **Each node is an AWS EC2 instance**.

## General ETL Concepts

- To copy the results of a query to another table **in the same database**, we can use SELECT INTO.
```SQL
SELECT fact1, fact 2
INTO new_fact_table
FROM table_x, table_y
WHERE ...
GROUP BY ...
...
```
- But how to copy the results of a query to **another table on a totally different database server**?
    - If both servers are running the same RDBMS, that might be possible, but harder between two completely different RDBMSs.
    - Even if we can, we probably need to do some transformations, cleaning, governance, etc.
- **Solution:** use an ETL server in the middle to simplify the problem of SQL to SQL ETL: DB Server 1 -> ETL Server -> DB Server 2
    - ETL server can talk to the source server and run a SELECT query on the source DB server.
    - ETL server stores the results in CSV files => needs large storage.
    - ETL server does insert/copy the results in the destination DB server.
    - We can automate this process.

## ETL for Redshift

In the ETL implementation on AWS, the purpose of the EC2 instance just a machine that acts a client to RDS and Redshift to issue COPY command.
- Amazon EC2 machine can copy from one SQL server to another SQL server.
- Amazon EC2 **issues commands only** and **data** is copied, transferred between DB and S3 **directly**.

S3 is AWS-managed, we don't need to worry about storage reliability. By using S3:
- we only pay for the storage we use.
- we don't need to worry about not having enough storage.

We might need to copy data already stored in S3 to another S3 staging bucket during ETL process because it would be transformed before insertion into the DWH.

### Ingesting at Scale
- To transfer data from an S3 staging area to Redshift use the **COPY** command.
- Inserting data row by using INSERT will be **very slow**.
- If the file is large:
    - It's better to break it up to **multiple files**.
    - Ingest **in parallel**: either using a **common prefix**, or a **manifest file**.
- Other considerations:
    - Better to ingest from the same AWS region.
    - Better to compress the all the CSV files (e.g; in gzip files).
- One can also specify the delimiter to be used.

### Common Prefix Example

```SQL
COPY sporting_event_ticket
FROM 's3://udacity-labs/tickets/split/part'
CREDENTIALS 'aws_iam_role=arn:aws:iam:464956546:role/dwhRole'
gzip DELIMITER ';' REGION 'us-west-2'
```

The command above will copy files with prefix `path` from s3 bucket `udacity-lab`, e.g: tickets/split/part-000.csv.gz, tickets/split/part-001.csv.gz, etc.

If we want to copy from explicit files, we can specify the manifest method and declare explicit files in manifest file like in the example below.

```SQL
COPY customer
FROM 's3://udacity-labs/cust.manifest'
IAM_ROLE 'arn:aws:iam:464956546:role/dwhRole'
manifest;
```

```JSON
# cust.manifest

{
    "entries": [
        {"url": "s3://mybucket-alpha/2020-10-04-custdata", "mandatory": true},
        {"url": "s3://mybucket-beta/2020-10-05-custdata", "mandatory": true}
    ]
}
```

### Redshift ETL Automatic Compression Optimization
- The optimal compression strategy for each column type is different.
- Redshift gives the user control over the compression of each column.
- The COPY command makes automatic best-effort compression decisions for each column.

### ETL from Other Sources
- It's possible to **ingest directly** using SSH from EC2 machines.
- Other than that:
    - S3 needs to be used as a **staging area**.
    - Usually, an EC2 ETL worker needs to run the ingestion jobs **orchestrated by a dataflow product** like Airflow, Luigi, Nifi, StreamSet or AWS Data Pipeline.

### ETL out of Redshift
- Redshift is accessible, like any relational database, as a JDBC/ODBC source: naturally used by BI apps.
- We may need to extract data out of Redshift to pre-aggregated OLAP cubes by using command UNLOAD.

```SQL
UNLOAD ('SELECT * FROM venue LIMIT 10')
TO 's3://mybucket/venue_pipe_'
IAM_ROLE 'arn:aws:iam::0123456789012:role/myRedshiftRole';
```
- Usually we'll want to use S3 as a staging area, but for very small data, we might want to copy it directly from the EC2 machine.

## Building a Redshift Cluster

### Quick Launcher

The cluster created by the Quick Launcher is a fully-functional one, but we need more functionality:
- Security settings:
    - the cluster is accessible only from the virtual private cloud (VPC).
    - we need to access it from our jupyter workspace.
- Access to S3: the cluster needs to access an S3 bucket.

### Infrastructure as Code (IaC)
An advantage of being in the cloud is the ability to create infrastructure, e.g. machines, users, roles, folders and processes using code.
- IaC lets us automate maintain, deploy, replicate and share complex infrastructures as easily as we maintain code (undreamt-of in an on-premise deployment).
- IaC is border-line dataEng/devOps.
- We have a number of options to achieve IaC on AWS
    - **aws-cli** scripts:
        - similar to bash scripts.
        - simple & convenient.
    - AWS SDK (aka **boto3**):
        - available in lots programming language.
        - more power, could be integrated with apps.
    - Amazon Cloud Formation:
        - JSON description of all resources, permission, constraints.
        - Atomic, either all succeed or all fail.
- Advantages of Infrastructure-as-Code (IaC) over creating infrastructure by clicking-around:
    - Sharing: One can share all the steps with others easily
    - Reproducibility: One can be sure that no steps are forgotten
    - Multiple deployments: One can create a test environment identical to the production environment
    - Maintainability: If a change is needed, one can keep track of the changes by comparing the code

#### Create an IAM role

```Python
import boto3

# create client for IAM
iam = boto3.client(
    "iam", region_name="us-west-2",
    aws_access_key_id=[YOUR_KEY_ACCESS],
    aws_secret_access_key=[YOUR_KEY_SECRET]
)

# create IAM role
dwhRole = iam.create_role(
    Path='/',
    RoleName=[YOUR_IAM_ROLE_NAME],
    Description="Allows Redshift clusters to call AWS services on your behalf.",
    AssumeRolePolicyDocument=json.dumps({
        'Statement': [{
            'Action': 'sts:AssumeRole',
            'Effect': 'Allow',
            'Principal': {'Service': 'redshift.amazonaws.com'}
        }],
        'Version': '2012-10-17'
    })
)

# attach policy
iam.attach_role_policy(
    RoleName=[YOUR_IAM_ROLE_NAME],
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)['ResponseMetadata']['HTTPStatusCode']

# get and print IAM role ARN
roleArn = iam.get_role(RoleName=[YOUR_IAM_ROLE_NAME])['Role']['Arn']
print(roleArn)
```

#### Create a Redshift cluster

```Python
# create client for Redshift
redshift = boto3.client(
    "redshift", region_name="us-west-2",
    aws_access_key_id=[YOUR_KEY_ACCESS],
    aws_secret_access_key=[YOUR_KEY_SECRET]
)

response = redshift.create_cluster(
    # parameters for hardware
    ClusterType=[YOUR_CLUSTER_TYPE],
    NodeType=[YOUR_NODE_TYPE],
    NumberOfNodes=int([YOUR_NUM_NODES]),

    # add parameters for identifiers & credentials
    DBName=[YOUR_DB],
    ClusterIdentifier=[YOUR_CLUSTER_IDENTIFIER],
    MasterUsername=[YOUR_DB_USER],
    MasterUserPassword=[YOUR_DB_PASSWORD],

    # parameter for role to allow S3 access
    IamRoles=[roleArn]  # get from creating IAM role
)

# get list of clusters
clusters = redshift.describe_clusters()['Clusters']

# get a cluter and print its properties
clusterProps = redshift.describe_clusters(ClusterIdentifier=[YOUR_CLUSTER_IDENTIFIER])['Clusters'][0]

import pandas as pd
def pretty_cluster_props(props):
    pd.set_option('display.max_colwidth', None)
    keys2Show = ["ClusterIdentifier", "NodeType",
                 "ClusterStatus", "MasterUsername",
                 "DBName", "Endpoint",
                 "NumberOfNodes", "VpcId"]
    data2Show = [(k, v) for k, v in props.items() if k in keys2Show]
    return pd.DataFrame(data=data2Show, columns=["Key", "Value"])
display(pretty_cluster_props(clusterProps))
```

#### Open an incoming TCP port to access the cluster endpoint

```Python
# create resource for EC2
ec2 = boto3.resource(
    "ec2", region_name="us-west-2",
    aws_access_key_id=[YOUR_KEY_ACCESS],
    aws_secret_access_key=[YOUR_KEY_SECRET]
)

# create a VPC (Virtual Private Cloud)
vpc = ec2.Vpc(id=clusterProps['VpcId'])  # clusterProps get from creating cluster
# get & print default security group
defaultSg = list(vpc.security_groups.all())[0]
print(defaultSg)

# authorize access using TCP
defaultSg.authorize_ingress(
    GroupName=defaultSg.group_name,
    CidrIp='0.0.0.0/0',
    IpProtocol='TCP',
    FromPort=int([YOUR_DWH_PORT]),
    ToPort=int([YOUR_DWH_PORT])
)

# make sure we can connect to the cluster
%load_ext sql

DWH_ENDPOINT = clusterProps['Endpoint']['Address']
conn = "postgresql://{}:{}@{}:{}/{}".format(
    [YOUR_DB_USER], [YOUR_DB_PASSWORD], DWH_ENDPOINT,
    [YOUR_DWH_PORT], [YOUR_DB]
)
%sql $conn
```

#### Clean up resources

```Python
# delete cluster
redshift.delete_cluster(
    ClusterIdentifier=[YOUR_CLUSTER_IDENTIFIER],
    SkipFinalClusterSnapshot=True
)
# verify cluster deletion
if redshift.describe_clusters()['Clusters']:
    clusterProps = redshift.describe_clusters(ClusterIdentifier=[YOUR_CLUSTER_IDENTIFIER])['Clusters'][0]
    pretty_cluster_props(clusterProps)

# detach role policy & delete role
iam.detach_role_policy(
    RoleName=[YOUR_IAM_ROLE_NAME],
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
)
iam.delete_role(RoleName=[YOUR_IAM_ROLE_NAME])
```

## Optimizing Redshift Table Design

- When a table is partioned up into many pieces and distributed across slices in different machines, this is done blindly.
- If one has an idea about the frequent access pattern of a table, one can choose a more clever strategy.
- The 2 possible strategies are:
    - Distribution styles.
    - Sorting key.

### Distribution Styles
- EVEN distribution:
    - Round-robin over all slices to achieve **load-balancing**. EVEN load-balances the partitioning of the table on the slices.
    - Good if a table won't be joined because JOIN results with lots of **shuffling**. A given key of table 1 will not be on the same slice as the corresponding record in table 2, so record will be copied (shuffled) between slices on different nodes, which results in slow performance.
- ALL distribution:
    - Small tables could be replicated on all slices to speed up JOINs. JOIN result in parallel, **no shuffling**.
    - Used frequently for dimension tables.
    - Aka **broadcasting**.
- AUTO distribution:
    - Leave decision to Redshift.
    - **Small enough** tables are distributed with an ALL strategy.
    - Large tables are distributed with EVEN strategy.
- KEY distribution:
    - Rows having similar values are placed in the same slice. This can lead to a skewed distribution if some values of the `distkey` are more frequent than others.
    - It's very useful when a dimension table is too big to be distributed with ALL strategy. In that case, we distribute both the fact table and the dimension table using the same `distkey`.
    - If two tables are distributed on the joining keys, Redshift co-locates the rows from both tables on the same slices.

### Sorting Key
- One can define its columns as `sortkey`.
- Upon loading, rows are sorted before distribution to slices.
- Minimizes the query time since each node already has contiguous ranges of rows based on the sorting key.
- Useful for columns that are used frequently in sorting like the date dimension and its corresponding foreign key in the fact table.

## Terminology
1. IAM
2. ARN
3. EC2
4. S3
5. 