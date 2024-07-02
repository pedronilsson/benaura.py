Benaura.py is a command line python script built to perform a simple geoparsing task in texts files locally. It was built as part of my PhD thesis entitled "Mapping the Works of Manuel de Pedrolo in Relation to the Post-civil War Catalan Landscape" found here: https://cora.ucc.ie/items/28dca192-daa9-4bf8-948f-652b4abed42b

It is ideal for localised and very specific placename text-mining, when existing geoparsing techniques (linked to online gazeteers) produce too many inacurate results (due to issues such as ambiguiity of placenames, linguistic or localised differences).

Benaura.py needs to be provided with an existing placenames.csv file that includes the locations and coordinates that you want to extract from the text. See "placenames_template.csv" for an example of the format needed for that csv file to work.

In order for the script to work, the files "benaura.py", "placenames.csv" and "texfile.txt" file you want to geoparse need to be put in the same folder.

With terminal or equivalent, run the following command: python3 benaura.py textfile.txt 

The script will produce the following outputs:
- a .csv file (stats.csv) with a list of placenames found on the text, including coordenates and frequency (number of times the place appears in the given text).
- a .png file ("count_hist.png") containing a bar graph with the 10 most frequent places found in the text.
- a stopword text file ("stoplist.txt") that can be modified to exclude words from the analysis.

  
