from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("df to mysql")
    .config("spark.some.config.option", "some-value")
    .getOrCreate()
)

df = spark.range(1, 10000001, 1)
df = df.repartition(4)

print(df.rdd.getNumPartitions)

(
    df.write.format("jdbc")
    .option(
        "url",
        "jdbc:mysql://mysql:3306/test?useServerPrepStmts=false&rewriteBatchedStatements=true",
    )
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("user", "root")
    .option("password", "admin")
    .option("useSSL", "false")
    .option("dbtable", "test")
    .mode("append")
    .save()
)
