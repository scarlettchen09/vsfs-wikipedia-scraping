# vsfs-wikipedia-scraping
 Web Scraping Project for VSFS - US Embassy London application

# How to use:
Run from the command line using `python main.py` to run with default URL and settings. 

# Arguments 
Optional arguments:
`python main.py arg1 arg2 arg3`

arg1: optional, full Wikipedia URL: (example/default: https://en.wikipedia.org/wiki/Embassy_of_the_United_States,_London)

arg2: optional, modifies the program to only the nth most common words 

(example/default: 10) Will cause the program to only print out the top 10 most commmon words for each section.  

arg3: optional, determines if the program will ignore empty sections it cannot find text associated with for. 
(default: true/yes) Inputting 'no' or 'false' will cause the program to print out empty sections. 