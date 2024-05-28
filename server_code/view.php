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
        $id=$_GET['ID'];
        if (!isset($_SESSION['username'])){
            echo '<script>location.replace("login.php")</script>';
        }

        $connect = new PDO ('mysql:host=localhost; dbname=serverDB', 'root', '1234');
        $connect->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
        $sql = $connect->query("SELECT * from board WHERE ID='$id'");
        $result = $sql->fetch();
    ?>
    <div class="mb-3 row">
        <label for="Title" class="col-sm-2 col-form-label"><strong>Title</strong></label>
        <div class="col-sm-10">
            <input type="text" readonly class="form-control-plaintext" id="Title" value="<?= $result['Title'] ?>">
    </div>
    
    <div class="mb-3 row">
        <label for="Writer" class="col-sm-2 col-form-label"><strong>Writer</strong></label>
        <div class="col-sm-10">
            <input type="text" readonly class="form-control-plaintext" id="Writer" value="<?= $result['Writer'] ?>">
    </div>
    
    <div class="mb-3">
        <br>
        <label for="Content" class="form-label"><strong>Content</strong></label>
        <input type="text" readonly class="form-control-plaintext" id="Content" rows="10" value="<?= $result['Content'] ?>"></textarea>
    </div>

    <button type="button" class="btn btn-primary btn-sm" onclick="location.href='update.php?ID=<?= $id ?>'" >수정</button>
    <button type="button" class="btn btn-secondary btn-sm" onclick="location.href='delete_action.php?ID=<?= $id ?>'" >삭제</button>
    <button type="button" class="btn btn-third btn-sm" onclick="location.href='list.php'" >돌아가기</button>
</body>
    