from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("word count")
    .config("spark.some.config.option", "some-value")
    .getOrCreate()
)

df1 = spark.range(2, 100000, 2)
df2 = spark.range(2, 100000, 4)

step1 = df1.repartition(5)
step12 = df2.repartition(6)

step2 = step1.selectExpr("id*5 as id")
step3 = step2.join(step12, ["id"])

step4 = step3.selectExpr("sum(id)")

answer = step4.collect()

print(answer)
