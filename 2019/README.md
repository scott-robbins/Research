# Research

## Visual 
* Using Cellular Automata to Generate 'Art'

![CellularArtist](https://raw.githubusercontent.com/scott-robbins/Research/master/Visual/example_output.png)

![MoreArt](https://raw.githubusercontent.com/scott-robbins/Research/master/Visual/example_2.png)

A Video of how this image was made (essentially using random walks in blue channel, where the
cumulative density of points slowly adds color in the green and red channels). 

![HowItsMade](https://raw.githubusercontent.com/scott-robbins/Research/master/Visual/pattern_generator_0.mp4)

![HowItsMade2](https://raw.githubusercontent.com/scott-robbins/Research/master/Visual/pattern_generator_1.mp4)

# Audio 

## Audio Style Transfer 
Starting with some tensorflow code I found, I used isolated tracks from various
well known artists and experimented with style transfer code to create some weird
mixes. I think my favorite so far is the cross of a drum track (Lateralus - Tool)
and the isolated guitar from "Whole Lotta Love" by Led Zepplin.

[ledzeptool](https://github.com/scott-robbins/Research/blob/master/Audio/AST/outputs/ledzeptool.wav) 

This is still a work in progress. I would like to be able to output longer samples. 
I also want to do some post processing on the outputs, because there's very clearly
some strange mirroring of frequencies (probably meant to capture harmonics) but some 
uneven stacks are clearly in the mix which is causing this sort of rhythmic static in
many resulting style combos (the output titled guit.wav is a good example of this). 

[More on Audio Style Transfer Here](https://github.com/scott-robbins/Research/tree/master/Audio/AST)
