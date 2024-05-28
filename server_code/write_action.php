<?php
    session_start();
    $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');
    $connect->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );

    $title = $_GET['title'];
    $content = $_GET['content'];
    $writer = $_GET['writer'];
    $date = date('Y-m-d');

    if (empty($title) || empty($content)){
        echo '<script>alert("Plz enter the content! or Title!!!")</script>';
        echo '<script>location.href="write.php"</script>';
        exit;
    }
    $sql = $connect->query("INSERT INTO board (Writer, Title, Content, Date) VALUE('$writer','$title', '$content', '$date')");
    
    $result = $sql->fetch();

    echo '<script>alert("Success to write in board!")</script>';
    echo '<script>location.href="list.php"</script>';
?>