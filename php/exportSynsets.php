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
mysqli_set_charset($conn,"utf8");
$sql = "SELECT id,senses_snapshot FROM  `synset`";
$result = $conn->query($sql);
$r = "*Vertices      9\r\n";
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $r.= "   " . $row["id"]. " \"" . $row["senses_snapshot"]. "\"\r\n";
		echo $row["senses_snapshot"];
    }
} else {
    echo "0 results";
}
$r .= "*Arcs\r\n";
$sql = "SELECT  synset, synset2, type FROM synset_relation";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $r.= "    " . $row["synset"]. "      " . $row["synset2"]. "       \"" . $row["type"]. "\"\r\n";
    }
} else {
    echo "0 results";
}
file_put_contents("synset_relation.txt", $r);
$conn->close();
?>
