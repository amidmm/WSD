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
$sql = "SELECT id FROM  `synset`";
$result = $conn->query($sql);
$r = "*Vertices      9\r\n";
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $r.= "   " . $row["id"]. " \"" . $row["id"]. "\"\r\n";
    }
} else {
    echo "0 results";
}
$r .= "*Arcs\r\n";
$allowed_types = ['Related-to'];
$allowed_types = ['Hypernym', 'Instance Hypernym'];
$sql = "SELECT  synset, synset2, type FROM synset_relation where type in ('" . join("','", $allowed_types) . "') and reviseResult='ACCEPTED'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        $r.= "    " . $row["synset"]. "      " . $row["synset2"]. "       \"" . $row["type"]. "\"\r\n";
    }
} else {
    echo "0 results";
}
file_put_contents("/tmp/synset_hypernyms.paj", $r);
$conn->close();
?>