<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "cz_pid";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

#$now_time = '22:30:00';   # TEST
#$now_date = '2021-06-11';   # TEST
#$tomorrow_date = '2021-06-12';   # TEST

$now_time = date("H:i:s");
$now_date = date("Y-m-d");
$tomorrow_date = date("Y-m-d", time()+86400);   # + 24 h

$sql = "
	SELECT DISTINCT day, 
		departure_clock_time, 
		stop_name, 
		route_short_name, 
		last_stop_name
	FROM xtra_departures_days_praha_hln
	WHERE departure_clock_time > '$now_time' 
		AND stop_name != last_stop_name
		AND day = '$now_date'
		OR day = '$tomorrow_date'
	ORDER BY day, departure_clock_time, last_stop_name
	LIMIT 10;
	";
	
// echo "<pre>".$sql."</pre>";   # TEST

$result = @$conn->query($sql);

?><!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
}
</style>
</head>
<body>

<h2>Praha h.n. - Next Departures</h2>
<?php
if (@$result->num_rows > 0) {
  echo "<table>
  <tr>
  <th>Day</th>
  <th>Departure</th>
  <th>Stop</th>  
  <th>Route</th>
  <th>Destination</th>
  </tr>";
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo " 
    <tr>
    <td>".$row["day"]."</td>
    <td>".$row["departure_clock_time"]."</td>
    <td>".$row["stop_name"]."</td>    
    <td>".$row["route_short_name"]."</td>
    <td>".$row["last_stop_name"]."</td>
    </tr>";
  }
  echo "</table>";
} else {
  echo "0 results";
}
$conn->close();
?>
<body>
