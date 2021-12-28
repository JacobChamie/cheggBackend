<?php
foreach (glob("web/*") as $filename) {
    include $filename;
}
?>