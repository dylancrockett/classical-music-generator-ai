If you would like to generate songs with this program you need to use the generate.py file rather than the UI provided in the main.py file due to problems with threading and Tk.

In order to generate songs you can just run the generate.py file and songs will show up in the songs folder, if no such folder exists an error will be thrown, feel free to modify this to make it go to a different directory etc. I apologize for the jank but if you have the wearwithall to deal with it the generator actually makes some decent classical music so feel free to sit back and enjoy!

For those who want to toy with values to get different songs there are a couple of variables that will make a big difference. The first one is tempo, this changes well, the tempo of the song. There are also a couple of variables in the actual SongGenerator class so feel free to mess around and get different results! 