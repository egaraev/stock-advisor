<?php
$con=mysqli_connect("localhost", "stockuser", "123456", "stock_advisor");
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
<body bgcolor=#abcaf2><h2>Cryptobot View Page</h2>
<br><b>Logs</b><br>";


echo "<table border='1'>
<tr>
<th>Date</th>
<th>Log entry</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['log_entry'] . "</td>";
echo "</tr>";
}
echo "</table>";

///mysqli_close($con);

//////////////


$result2 = mysqli_query($con,"SELECT * FROM symbols where active = 1");
echo "<br><b>Current orders</b><br>";

echo "<table border='1'>
<tr>
<th>Stock name</th>
<th>Current price</th>
<th>Positive sentiments %</th>
<th>Negative sentiments %</th>
<th>Predicted price</th>
<th>Heikin_ashi direction</th>
<th>Daily candle direction</th>
<th>News</th>
</tr>";

while($row = mysqli_fetch_array($result2))
{
echo "<tr>";
echo "<td>" . $row['name'] . "</td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td>" . $row['positive_sentiments'] . "</td>";
echo "<td>" . $row['negative_sentiments'] . "</td>";
echo "<td><b>" . $row['predicted_price'] . "</b></td>";
echo "<td>" . $row['heikin_ashi'] . "</td>";
echo "<td>" . $row['candle_direction'] . "</td>";
echo "<td><pre>" . $row['news'] . "</pre></td>";
echo "</tr>";
}
echo "</table>";

/////

echo "<br><b>AI charts for stocks</b><br>";

////


$dir = "images/";
$url = "";
$images = glob($dir.'*.{JPG,jpg,gif,png,bmp}', GLOB_BRACE);
foreach ($images as $image) {
    echo "<img src='{$url}{$image}' />";
}






mysqli_close($con);
?>



