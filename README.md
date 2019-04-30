# GridWiz

[![GridWiz Demo](https://video-to-markdown.netlify.com/.netlify/functions/image?url=https%3A%2F%2Fyoutu.be%2F25B4mrCk-18)](https://youtu.be/25B4mrCk-18 "GridWiz Demo")

**By Ace Centre**

This small app creates a simple one target per page gridset with your desired image search. Simply run it, selecting your gridset. The examples are "Original.gridset" (one target that gets smaller), OriginalFixed.gridset (one target that is the same size but moves around on a 6x6 grid) and OriginalMulti.gridset (3 activities - one in a row, one in a square and then the same as Original.gridset). Feel free to modify the gridsets if you so wish and re-run the application. Enter your search terms to find the motivating images for your individual, then press the "Start" button. When done it will create a new gridset in the same directory - named the same as your search term. Double click it and it will add it to your Grid 3 programme. 

## How does it work

It only works on gridsets with a single image on each page. So it looks for the image on the page and replaces it with the results from a google search. It then replaces the single image in the page n win/ directory for each page. Simples! 

## I want to modify the gridsets. What do I need to know?

This script is very basic. It simply looks for pages that are labelled "Something n" and "Something n win" where n = a number. Dont change the syntax of "win" or add any more spaces. You can add more pages and add sounds etc - but it has to be this structure. 

## Future plans / to-do

- More than one item per page
- A forced order spelling activity of someones name
- Ability to use own images
- Embed in the Gridset and run from the Grid

## Like it? 

Why not donate a little something to us. [Choose your value](https://donate.justgiving.com/donation-amount?uri=aHR0cHM6Ly9kb25hdGUtYXBpLmp1c3RnaXZpbmcuY29tL2FwaS9kb25hdGlvbnMvNmM2ODNlNzFlMTczNGJhZmJlMDIyODY3MmZlMjUzN2Q=) ;) 


## Want something else? 

Why don't you [consider hiring us](https://acecentre.org.uk/services/engineering/)! 


## How do I know this isn't doing anything malicious? I want to develop this myself 

For full source code please see it [here](https://github.com/acecentre/GridWiz)