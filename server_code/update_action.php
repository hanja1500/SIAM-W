<?php
    session_start();
    if (!isset($_SESSION['username'])){
        echo '<script>alert("Go back");</script>';
        echo '<script>location.replace("logout.php")</script>';
        exit();
    }

    $title = $_GET['title'];
    $content = $_GET['content'];
    $ID = $_GET['ID'];
    $writer = $_SESSION['username'];

    if ($title == NULL || $content == NULL || $ID == NULL){
        echo '<script>alert("Plz enter the content! or Title!!!")</script>';
        echo '<script>location.href="update.php?ID='.$ID.'"</script>';
        exit;
    }

    $connect = new PDO('mysql:host=localhost; dbname=serverDB', 'root', '1234');
    $connect->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $sql = $connect->
    query("UPDATE board SET Title='$title', Content='$content' WHERE ID='$ID'");
    
    $result = $sql->fetch();

    echo "<script>alert('success to update content!')</script>";
    echo "<script>location.replace('list.php')</script>";
?>