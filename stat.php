<?php
$con=mysqli_connect("localhost", "stockuser", "123456", "stock_advisor");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM logs order by log_id desc limit 10");
echo "<html><head><title>Stock advisor statistics</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Stock Advisor Stats Page</h2>
<br><b>Stats</b><br>";


$result = mysqli_query($con,"SELECT * FROM symbols where active = 1");


echo "<table border='1'>
<tr>
<th>Stock name</th>
<th>Historical Chart for news, tweets, indicators</th>
<th>AI Historical Chart for machine learning predictions</th>
<th>Candle Patterns Chart</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['name'] . "</td>";
echo "<td><a href='images/". $row['symbol'] ."_history.png'><img src='images/". $row['symbol'] ."_history.png' width='1000px' height='700px'></td>";
echo "<td><a href='images/". $row['symbol'] ."_ai_history.png'><img src='images/". $row['symbol'] ."_ai_history.png' width='1000px' height='700px'></td>";
echo "<td><a href='images/". $row['symbol'] ."_candlesticks.png'><img src='images/". $row['symbol'] ."_candlesticks.png' width='1000px' height='700px'></td>";
echo "</tr>";
}
echo "</table>";

mysqli_close($con);
?>
