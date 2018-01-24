<html lang="en">
 <head>
  <meta charset="utf-8">
</head>
<?php
$servername = "localhost";
$username = "root";
$password = "12345";
$dbname = "farsnet";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
$result = $conn->query("SET NAMES utf8;");
$sql = "SELECT id, example, senses_snapshot FROM `synset` where reviseResult = \"ACCEPTED\" and length(example)>50 ";
$result = $conn->query($sql);
$r=[];
//echo $result->num_rows;
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $r[] =  $row;
    }
} else {
    echo "0 results";
}

$j = json_encode($r, JSON_UNESCAPED_UNICODE);
//print_r($r);
file_put_contents("/tmp/farsnetWSDDataset.json", $j);
$conn->close();
?>
