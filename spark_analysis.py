from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder.appName("HotelAnalysis").getOrCreate()

# Load CSV
df = spark.read.csv("bookings.csv", header=True, inferSchema=True)

print("=== DATA ===")
df.show()

# 💰 Total revenue
print("=== TOTAL REVENUE ===")
df.groupBy().sum("total_price").show()

# 🏨 Most booked rooms
print("=== MOST BOOKED ROOMS ===")
room_stats = df.groupBy("room_id").count().orderBy("count", ascending=False)

# convert to pandas
room_stats_pd = room_stats.toPandas()

# save to CSV
room_stats_pd.to_csv("room_stats.csv", index=False)
revenue = df.groupBy().sum("total_price").toPandas()
revenue.to_csv("revenue.csv", index=False)
# 📅 Bookings per date
print("=== BOOKINGS PER DAY ===")
df.groupBy("check_in").count().show()