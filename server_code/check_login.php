<?php
    session_start();
    $username = $_GET['id'];
    $userpass = $_GET['pw'];
    
    $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');
    
    $sql = $connect->query("SELECT * from member WHERE ID='$username' OR PW='$userpass'");
    $result = $sql->fetch();

    if( !$result ) {
        echo "<script>alert('Invalid username or password')</script>";
        echo "<script>location.replace('login.php')</script>";
        exit;
    }
    else if( $result == null ) {
        echo "<script>alert('Input the ID and password!')</script>";
        echo "<script>location.replace('login.php')</script>";
        exit;
    }

    $_SESSION['username'] = $username;
    echo "<script>location.replace('list.php')</script>";
?>
