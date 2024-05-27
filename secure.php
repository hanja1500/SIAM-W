<?php
    #session_start();
    $username = $_GET['id'];
    $userpass = $_GET['pw'];

    $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');

    $match = '/^[a-zA-Z0-9]+$/';

    if(!preg_match($match, $username)){
        echo '<script>alert("use only alphabet and numbers")</script>';
        exit;
    }

    $statement = $connect->prepare('SELECT * FROM member WHERE ID = :id AND PW = :pw');
    $statement->bindValue(':id', $username, PDO::PARAM_STR);
    $statement->bindValue(':pw', $userpass, PDO::PARAM_STR);
    $statement->execute();
    $result = $statement->fetch();

    if( !$result ) {
        echo "<script>alert('Invalid ID or Password')</script>";
        echo "<script>location.replace('login.php')</script>";
        exit;
    }
    else if( $result == null ) {
        echo "<script>alert('Input the ID and password!')</script>";
        echo "<script>location.replace('login.php')</script>";
        exit;
    }
    else if( $result["PW"] != $userpass ){
        echo "<script>alert('Invalid ID or Passward!')</script>";
        echo "<script>location.replace('login.php')</script>";
        exit;
    }
    $_SESSION['username'] = $username;
    echo "<script>location.replace('list.php')</script>";
?>