<?php
$con=mysqli_connect("database-service","cryptouser","123456","cryptodb");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM logs order by log_id desc limit 10");
echo "<html><head><title>Cryptobot</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Cryptobot Stats Page</h2>
<br><b>Stats</b><br>";


$result = mysqli_query($con,"SELECT * FROM stat");


echo "<table border='1'>
<tr>
<th>Market</th>
<th>Date</th>
<th>Price</th>
<th>AI Price</th>
<th>AI direction</th>
<th>HAH</th>
<th>HA</th>
<th>HAD</th>
<th>hah</th>
<th>ha</th>
<th>had</th>
<th>Ha_curr</th>
<th>Ha_prev</th>
<th>% change</th>
<th>Volume</th>
<th>Candles</th>
<th>Candle_sig_short</th>
<th>Score</th>
<th>Score_direction</th>
<th>Pos.tweets</th>
<th>Neg.tweets</th>
<th>Buy_orders_sum</th>
<th>Sell_orders_sum</th>
<th>Buy_orders_count</th>
<th>Sell_orders_count</th>
<th>Spread</th>
<th>Grow_hour_%</th>
<th>Grow_history_%</th>
<th>Fivemins_history_%</th>
<th>Active</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['market'] . "</td>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td>" . $row['ai_price'] . "</td>";
echo "<td>" . $row['ai_direction'] . "</td>";
echo "<td>" . $row['ha_direction_hour'] . "</td>";
echo "<td>" . $row['ha_direction'] . "</td>";
echo "<td>" . $row['ha_direction_daily'] . "</td>";
echo "<td>" . $row['ha_hour'] . "</td>";
echo "<td>" . $row['ha_fivehour'] . "</td>";
echo "<td>" . $row['ha_day'] . "</td>";
echo "<td>" . $row['ha_candle_current'] . "</td>";
echo "<td>" . $row['ha_candle_previous'] . "</td>";
echo "<td>" . $row['percent_chg'] . "</td>";
echo "<td>" . $row['volume'] . "</td>";
echo "<td>" . $row['candles'] . "</td>";
echo "<td>" . $row['candle_signal_short'] . "</td>";
echo "<td>" . $row['score'] . "</td>";
echo "<td>" . $row['score_direction'] . "</td>";
echo "<td>" . $row['positive_sentiments'] . "</td>";
echo "<td>" . $row['negative_sentiments'] . "</td>";
echo "<td>" . $row['buy_orders_sum'] . "</td>";
echo "<td>" . $row['sell_orders_sum'] . "</td>";
echo "<td>" . $row['buy_orders_count'] . "</td>";
echo "<td>" . $row['sell_orders_count'] . "</td>";
echo "<td>" . $row['spread'] . "</td>";
echo "<td>" . $row['grow_hour'] . "</td>";
echo "<td>" . $row['grow_history'] . "</td>"; 
echo "<td>" . $row['grow_fivemins'] . "</td>";    
echo "<td>" . $row['active'] . "</td>"; 
echo "</tr>";
}
echo "</table>";

mysqli_close($con);
?>
