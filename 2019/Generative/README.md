# Generative 

# Style Transfer
Using the pre-trained VGG-19 CNN Model, we can use this python code (found elsewhere
and modified. I did not write all of the ex.py!) to essentially create a hybrid image
of two input images. 

The standard example is a cross using the content of a Taipei skyline and overlaying 
with the style of Starry Night. 

But experimenting further you can try some interesting examples. Particularly, trying
to find interesting 'style' content (as not all style transfers the same in terms of 
distorting/enhancing the content). For example, the artist Alex Grey is known for a 
very particular style (much like Van Gogh and starry night), however his style is not
only a lot of interesting background textures, but there's also the way he highlights
the body of a subject. 

Taking the following image of Trey Anastasio (lead guitar and frontman of rock band Phish)
and a painting of Alex Grey's, the result is quite neat.

![ContentIm](https://github.com/scott-robbins/Research/blob/master/Generative/Seeds/young_trey.jpeg)
![StyleIm](https://raw.githubusercontent.com/scott-robbins/Research/master/Generative/Seeds/grey_tool.jpeg)


![greyTrey](https://github.com/scott-robbins/Research/blob/master/Generative/results/RESULTS/grey_trey_0.png)

The next thing I wanted to look at was less artistic style and more spatially repeated 
patterns like fractals, mandalas and mosaics. Images of these kind seem to transfer
style quite well because of the self-similar and spatially repeated nature of the style.
So taking a picture of a smilin' Bernie Sanders, and a mosaic with a fractal like style
we get the following:
![Bern](https://raw.githubusercontent.com/scott-robbins/Research/master/Generative/Seeds/bern.jpeg)
![Tiles](https://raw.githubusercontent.com/scott-robbins/Research/master/Generative/Seeds/mosaic.jpeg)

Result:
![TileBern](https://github.com/scott-robbins/Research/blob/master/Generative/results/RESULTS/tiled_bern.png)

