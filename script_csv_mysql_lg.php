<?php

$connect = mysql_connect('localhost','lgarcia','19184113');

if (!$connect) {
 die('No se pudo conectar con la BDD: ' . mysql_error());
}
else{
  print "conexion satisfactoria";
}



$cid =mysql_select_db('cmsseo',$connect);


define('CSV_PATH','C:/wamp64/www/');


$csv_file = CSV_PATH . "contactos.csv"; 


if (($handle = fopen($csv_file, "r")) !== FALSE) {
   fgetcsv($handle);   
   while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
       /* for ($c=0; $c < $num; $c++) {
          $col[$c] = $data[$c];
        }*/

 #$col1 = $col[0];
 print $data[0]." <- NAME ";
 /*
 $col2 = $col[1];
 print $col2." <- PHONE ";
 $col3 = $col[2];
 print $col3." <- EMAIL ";
 $col4 = $col[3];
 print $col4." <- STATUS \n";
 $col5 = $col[4];
   */

#$query = "INSERT INTO pedidos (name,phone,email,status,created_at) VALUES('".$col1."','".$col2."','".$col3."','".$col4."','".$col5."')";
$query = "INSERT INTO pedidos (name) VALUES ('".$col1."')";

mysql_query($query, $connect);

 }
    fclose($handle);
}

echo "Archivo importado satisfactoriamente a la BDD!";
mysql_close($connect);
?>