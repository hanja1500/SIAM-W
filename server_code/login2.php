<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/css/bootstrap.css">
    <title>Document</title>

</head>
<body>
    <form method="get" action="check_login.php" class="loginForm">
    <h2>Login</h2>
        <div class="idForm">
            <input type="text" name="id" class="id" placeholder="Username">
        </div>
        <div class="passForm">
            <input type="password" name="pw" class="pw" placeholder="Password">
        </div>
        <?php
            session_start();
            $username = $_GET['id'];
            $userpass = $_GET['pw'];

            $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');

            $sql = $connect->query("SELECT * from member WHERE ID='$username'");
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
        <div class="bottomText"></div>
    </form>
</body>
</html>