<head><body bgcolor=#abcaf2></head>
<?php
$con=mysqli_connect("localhost", "stockuser", "123456", "stock_advisor");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM history");


echo "<table border='1'>
<tr>
<th>Market</th>
<th>Date</th>
<th>Price</th>
<th>AI Price</th>
<th>Candle Score</th>
<th>Pos.tweets</th>
<th>Neg.tweets</th>
<th>Twitter ratio</th>
<th>New score</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['symbol'] . "</td>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td>" . $row['predicted_price'] . "</td>";
echo "<td>" . $row['candle_score'] . "</td>";
echo "<td>" . $row['positive_tweets'] . "</td>";
echo "<td>" . $row['negative_tweets'] . "</td>";
$tweet_ratio=($row['positive_tweets']/$row['negative_tweets'])
$tweets_ratio = number_format($tweet_ratio, 2, '.', '');
//echo "<td>" . $row['positive_tweets']/$row['negative_tweets'] . "</td>";        
echo "<td>" . $row['news_score'] . "</td>";
echo "</tr>";
}
echo "</table>";

mysqli_close($con);
?>
