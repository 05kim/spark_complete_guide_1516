from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("mongodb to mysql").getOrCreate()

partitionSize = 1000000

# 전체 레코드 수를 가져온다.
sizeDF = (
    spark.read.format("jdbc")
    .option(
        "url",
        "jdbc:mysql://mysql:3306/test?useServerPrepStmts=false&rewriteBatchedStatements=true",
    )
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("user", "root")
    .option("password", "admin")
    .option("query", "select max({}) from {}".format("id", "test.test"))
    .load()
)

maxId = sizeDF.collect()[0][0]
maxId = int(maxId)

# 레코드 수를 기반으로 파티션 개수를 산정한다.
numPartitions = (maxId // partitionSize) + 1

# mysql 데이터를 파티션을 나누어 가져온다.
df = (
    spark.read.format("jdbc")
    .option(
        "url",
        "jdbc:mysql://mysql:3306/test?useServerPrepStmts=false&rewriteBatchedStatements=true",
    )
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("user", "root")
    .option("password", "admin")
    .option("dbtable", "test")
    .option("partitionColumn", "id")
    .option("numPartitions", numPartitions)
    .option("lowerBound", 1)
    .option("upperBound", maxId)
    .load()
)

# 가져온 mysql 데이터를 mongodb 로 write 한다.
(
    df.select("id")
    .write.format("mongodb")
    .mode("append")
    .option("connection.uri", "mongodb://root:1234@mongodb:27017")
    .option("database", "test")
    .option("collection", "test")
    .option("convertJson", "any")
    .option("maxBatchSize", "100000")
    .save()
)
