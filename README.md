# What Is This?

This is a project designed to help me set up quake II from a retail CD archive quickly on my linux machine.
I couldn't find instructions anywhere that described
exactly how you were supposed to take a bin/cue archive of retail quake II
and play it on linux.

this script downloads Quake II.zip from archive.org and converts the bin/cue files to an ISO image containing the game's data track, and .cdr files
containing the audio soundtrack. The script then takes these .cdr files, converts them each to .ogg and names them according to track number.

# Where Does It Put The Goods?

The output of the script is a folder called generated_qbase2 containing
the game's data assets extracted from the ISO and its CD-audio music in
.ogg format. The generated_qbase2 directory can be renamed to qbase2 and dropped into a quake II client such as yamagi quake!