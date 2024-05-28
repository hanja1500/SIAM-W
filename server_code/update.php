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
        $parameter = $_GET["ID"];
        $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');
        $connect->setAttribute(PDO::ATTR_ERRMODE, POO::ERRMODE_EXCEPTION);

        $sql = $connect->query("SELECT * from board where ID='$parameter'");
        $result = $sql->fetch();
    ?>
    <form method="GET" action="update_action.php">
        <div id="in_title">
            <textarea name="title" id="utitle" rows="1" cols="55" placeholder="제목" maxlength="100" required><?php echo $board['title']; ?></textarea>
        </div>
        <div id="in_name">
            <textarea name="name" id="uname" rows="1" cols="55" placeholder="글쓴이" maxlength="100" required><?php echo $board['name']; ?></textarea>
        </div>
        <div id="in_content">
            <textarea name="content" id="ucontent" placeholder="내용" required><?php echo $board['content']; ?></textarea>
        </div>
    <button type="submit" class="btn btn-primary btn-sm">수정</button>
    <a href='view.php?ID= <?= $parameter ?>' class="btn btn-primary btn-sm" >취소</a>
    </form>
</body>
</html>