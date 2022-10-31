from pytube import YouTube
link = input("Enter Link of Youtube Video: ")
yt = YouTube(link)
# To print title
print("Title :", yt.title)
# To get number of views
print("Views :", yt.views)
# To get the length of video
print("Duration :", yt.length)
# To get description
print("Description :", yt.description)
# To get ratings
print("Ratings :", yt.rating)
stream = yt.streams.get_highest_resolution()
stream.download()
print("Download completed!!")
