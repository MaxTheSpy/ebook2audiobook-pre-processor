# ebook2audiobook-pre-processor
Pre-processor for ebook2audiobook
Main project: https://github.com/DrewThomasson/ebook2audiobook

ebook2audiobook converter has some issues with time delays for periods, question marks, ellipses, en and em dashes etc.

This pre-processor will edit your epub file to include a pound or pause (#) character after any of the following: .?!…–—!. This will also clean up double or triple pauses and or pauses inside and outside of quotations. This will also include a pause at the end of every paragraph to get a more natural reading cadence to the AI voice render. 

For best results, use properly formatted HTML EPUB files, you can fix or edit these files with Calibre.

USE: launch the python file, point it at an epub, hit enter. it will run for 1-5 seconds and output the epub with a "_Processed" added on the end of the title in the same directory as you ran it from. Then drag and drop it into your ebook2audiobook converter instance and let it run.
