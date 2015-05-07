<?php
	function writeLevelsFile ($newLevel = 100)
	
	{
		ini_set('display_errors', 1); 
		error_reporting(E_ALL);
		$levelFile = fopen("/var/www/levels.txt", "w") or die ("can`t open file levels.txt");
		$levelValue = $newLevel;
		fwrite($levelFile, $levelValue);
		echo "new maximum Volume has been set to: $newLevel";
				
	}
?>


<?php 
	writeLevelsFile (98);
?>