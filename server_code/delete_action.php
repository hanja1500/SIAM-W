<?php
    session_start();
    if (!isset($_SESSION['username'])){
        echo '<script>alert("Go back");</script>';
        echo '<script>location.replace("logout.php")</script>';
        exit();
    }
    $parameter = $_GET['ID'];
    $connect = new PDO('mysql:host=localhost; dbname=serverDB', 'root', '1234');
    $connect->setAttribute(PDO::ATTR_ERRMODE, PDO:: ERRMODE_EXCEPTION);

    $sql = $connect->query("DELETE FROM board WHERE ID='$parameter'");
    $result = $sql->fetch();

    echo "<script>alert('success to delete content!')</script>";
    echo "<script>location.replace('list.php')</script>";
?>