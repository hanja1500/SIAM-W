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
        <button type="submit" class="btn" onclick="button()">
            Login
        </button>
        <div class="bottomText"></div>
    </form>
</body>
</html>