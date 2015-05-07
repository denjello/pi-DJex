
<?php
	function writeLevelsFile ($newLevel = 100)
	{
		$levelFile = fopen("levels.txt", "W") or die ("can`t open file levels.txt");
		$levelValue = $newLevel;
		fwrite($levelFile, $levelValue);
		echo "new maximum Volume has been set to: $newLevel";
				
	}
?>

<?php 
	function printsomething()
	{
		echo "print something function";
	}
	
?>

<html>
<head>
	<meta charset="utf-8" />
	<link href="main.css" rel="stylesheet" media="all" />
	<title>DJex</title>	



</head>



<body>

<div id="mainFrame">

	<div id="header">
		<h1><head>DJex - der direkte Weg</head></h1>
	</div>
	<div id="main">
	 		<p> 
	 		<!--
	 		<textarea cols="20" rows="4" name="textfeld"></textarea>
	 			    
	 			<textarea cols="20" rows="4" name="textfeld"value="<?php echo $name;?>"></textarea>
	 			
	   			<input type="button" name="Boot" value="Boot PC" 
	   								onclick="this.form.textfeld.value= <?php	echo "Hi Ther PHP in here !"; ?>">
	    		<input type="button" name="shutdown" value="Shutdown" 
	    							onclick="this.form.textfeld.value='Ich bin Text 2 - ganz normal'">
	    							
	    					
	    		    <form method="post" action="script.php">
	   					<input type="submit" name="sent">
	   				</form>
	   		-->	
	      </p>
	 	<?php
			echo "Setzen des maximalen Lautstärkepegels, der Wert ab dem die Warnleuchte angeht befindet sich immer 10db drunter ";
		?>
	 		
	 	 <form method="post" action="50db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 50 db">
	 	</form>
	 	
	 	<form method="post" action="70db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 70 db">
	 	</form>
	 	
	 	 <form method="post" action="75db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 75 db">
	 	</form>
	 	 <form method="post" action="80db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 80 db">
	 	</form>
	 	 <form method="post" action="85db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 85 db">
	 	</form>
	 	 <form method="post" action="90db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 90 db">
	 	</form>
	 	 <form method="post" action="95db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 95 db">
	 	</form>
	 	 <form method="post" action="98db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 98 db">
	 	</form>
	 	 <form method="post" action="99db.php">
	 		<input type="submit" name="button_bootup" value="set max Vol to 99 db">
	 	</form>
			
			
	</div>	

</div>	
		
		
		

</body></html>
