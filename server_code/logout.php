<?php
    session_start();
    session_destroy();
    unset($_SESSION['username']);
    echo '<script>location.replace("login.php")</script>'
?>