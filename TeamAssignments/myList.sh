#! /bin/bash

#The script below lists the full directories at the script's home folder and presents it
#in HTML format via default program

#Clear the console
clear 

#Create HTML file in working directory (Will override exsisting file in working directory
cat << newHTML.html | tee newHTML.html

<HTML>
<Head>
</Head>
	<TITLE>
	List of files in directory 
	</TITLE>

<Body>

These are the full directories at the scripts home folder: <br><br/>
<!--Recursive search through working directory (1)-->
$(for dir in *; do
  echo "$dir" "<br></br>"
done
)

</Body>

</HTML>
newHTML.html
#End HTML file formatting 

#Open HTML file in default program
xdg-open newHTML.html



#Acknowledgements 
#(1) Credit:Shawn J. Goff (http://superuser.com/questions/31464/looping-through-ls-results-in-bash-shell-script)
