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
    $parameter= $_SESSION['username'];
    if (!isset($parameter)) {
        echo '<script>alert("You don`t have any access authority!")</script>';
        echo '<script>location.href="login.php"</script>';
        exit();
    }
    ?>
    <div class="board_wrap">
        <div class="board_title">
            <strong><a href="list.php" class="on">메인 페이지로 가기</a></strong>
            <p>글쓰기 페이지</p>
        </div>
        <div class="board_write_wrap">
            <form method="get" action="write_action.php">
                <div class="board_write">
                    <div class="title">
                        <dl>
                            <dt>제목</dt>
                            <dd><input type="text" name="title" placeholder=""></dd>
                        </dl>
                    </div>
                    <div class="info">
                        <dl>
                            <dt>글쓴이</dt>
                            <dd><input type="text" name="writer" value="<?= $parameter ?>" readonly></dd>
                        </dl>
                    </div>
                    <div class="cont">
                        <textarea name="content" placeholder="480"></textarea>
                    </div>
                </div>
                    <div class="bt_wrap">
                        <button type="submit">등록</button>
                        <a href="list.php">취소</a>
                    </div>
            </form>
        </div>
    </div>
</body>
</html>