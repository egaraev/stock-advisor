<html>
<head>
<title>
Eldar's great page
</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css" />
</head>
<body>


<?php
$con=mysqli_connect("localhost", "stockuser", "123456", "stock_advisor");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}



$result = mysqli_query($con,"SELECT * FROM logs order by log_id desc limit 10");
echo "<html><head><title>Stock advisor</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Stock Advisor`s View Page</h2>
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
echo "<br><b>Current stocks</b><br>";

echo "<table border='1'>
<tr>
<th>Stock name</th>
<th>Current price</th>
<th>Positive sentiments %</th>
<th>Negative sentiments %</th>
<th>Predicted price</th>
<th>Predicted chart</th>
<th>Heikin_ashi direction</th>
<th>Daily candle direction</th>
<th>News</th>
<th></th>
</tr>";

while($row = mysqli_fetch_array($result2))
{
echo "<tr>";
echo "<td>" . $row['name'] . "</td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td>" . $row['positive_sentiments'] . "</td>";
echo "<td>" . $row['negative_sentiments'] . "</td>";
echo "<td><b>" . $row['predicted_price'] . "</b></td>";
echo "<td><a href='images/". $row['symbol'] ."_result.png'><img src='images/". $row['symbol'] ."_result.png' width='250px' height='250px'></td>";
echo "<td>" . $row['heikin_ashi'] . "</td>";
echo "<td>" . $row['candle_direction'] . "</td>";
echo "<td><pre>" . $row['news'] . "</pre></td>";
echo "<td><pre><p><a href='#". $row['name'] ."' rel='modal:open'>Open details</a></p></pre></td>";
echo "</tr>";
}
echo "</table>";
$result2 = mysqli_query($con,"SELECT * FROM symbols where active = 1");
while($row = mysqli_fetch_array($result2))
{
	echo'<div id="'.$row['name'].'" class="modal">'.
  $row['news_text'].'
  <a href="#" rel="modal:close">Close</a>
</div>';
}











mysqli_close($con);
?>

<!-- Remember to include jQuery :) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js"></script>

<!-- jQuery Modal -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js"></script>
</body>

</html>


