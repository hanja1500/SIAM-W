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
        $parameter = $_SESSION['username'];
        if (!isset($parameter)){
            echo '<script>alert("You don`t have any access authority!")</script>';
            echo '<script>location.replace("login.php")</script>';
            exit();
        }

        $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');
        $connect->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
        $sql = $connect->query("SELECT ID, Writer, Title, Date from board");
    ?>
    <div class="board_wrap">
        <input type="button" value="Logout" style="float: right;" onclick="location.href='logout.php'"></a>
        <!-- <p><?= $_SESSION['username'] ?></p> -->
        <div class="board_title">
            <strong>게시판</strong>
            <p>리스트 페이지</p>
        </div>
        <div class="board_list_wrap">
            <div class="board_list">
                <div class="top">
                    <div class="num">번호</div>
                    <div class="title">제목</div>
                    <div class="writer">글쓴이</div>
                    <div class="date">작성일</div>
                    <div class="count">조회</div>
                </div>
            <div>
                <?php
                    while( $result = $sql->fetch())
                    {
                        echo '<div class="num">'.$result['ID'].'</div>';
                        echo '<div class="title"><a href="view.php?ID='.$result['ID'].'">'.$result['Title'].'</a></div>';
                        echo '<div class="writer">'.$result['Writer'].'</div>';
                        echo '<div class="date">'.$result['Date'].'</div>';
                        echo '<div class="count">0</div>';
                    }
                ?>
            </div>
            <div class="bt_wrap">
                <a href="write.php" class="on">등록</a>
            </div>
        </div>
    </div>
</body>

