<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>공지사항</title>
    <link rel="stylesheet" href="css.css">
</head>
<body>
    <?php
    session_start();
    if (!isset($_SESSION['username'])){
    echo '<script>location.replace("login.php")</script>';
    }
    $connect = new PDO('mysql:host=localhost; dbname=serverDB', 'root','root');
    $connect->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
    $sql = "SELECT ID, Writer, Title, Date from board";
    $result = $connect->query( $sql);
    ?>
</body>