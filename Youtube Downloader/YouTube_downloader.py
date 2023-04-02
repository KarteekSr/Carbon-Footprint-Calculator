import urllib.error
import pytube
import tkinter
import pytube.exceptions


class YouTubeVideoDownloader:
    """The class that represents the main downloader.

    Attributes:
        _screen (tkinter.Tk): The main screen of tkinter.
        _label_frame (tkinter.LabelFrame): The label frame that contains the entry for entering the link.
        _link (tkinter.StringVar): The string variable that stores the input of the user (link).
        _link_entry (tkinter.Entry): The entry in which the user has to type the link.
        _image_label (tkinter.Label): Label that has the image of The Youtube icon.
        _download (tkinter.Button): The button for downloading the video.
        _message (tkinter.Label): The label for showing different messages.
    Methods:
        run: Runs the main program
        _download_: Downloads the url.
    """
    def __init__(self) -> None:
        """Declare all the components of the screen."""
        # Declare the screen.
        self._screen = tkinter.Tk()
        self._screen.title('Youtube Video Downloader')
        self._screen.geometry('500x500-430-150')
        self._screen.resizable(False, False)

        # Configure rows
        self._screen.rowconfigure(0, weight=2)
        for i in range(4):
            self._screen.rowconfigure(i, weight=1)

        # Configure columns
        self._screen.columnconfigure(0, weight=1)
        self._screen.columnconfigure(1, weight=3)
        self._screen.columnconfigure(2, weight=1)

        # Declare components of the screen.
        self._label_frame = tkinter.LabelFrame(self._screen, text='Enter link')
        self._label_frame.columnconfigure(0, weight=1)
        self._link = tkinter.StringVar()
        self._link_entry = tkinter.Entry(self._label_frame, textvariable=self._link)
        self._download = tkinter.Button(self._screen, text='Download', height=2, width=10,
                                        bg='red', fg='white', activeforeground='white', activebackground='red',
                                        command=lambda: self._download_(self._link.get()))
        image = tkinter.PhotoImage(file='E:\\KARTEEK\\document space\\school\\Class-7\\My Python Projects'
                                   '\\Tkinter gui\\YouTube icon.png')
        self._message = tkinter.Label(self._screen, text='', wraplength=480)

        # Make a label to show the screen.
        self._image_label = tkinter.Label(self._screen, image=image)
        self._image_label.image = image

    def _download_(self, url: str) -> None:
        """Get a url of youtube video ,download it and set the `_message` accordingly

        :param url: The url of the video to be downloaded."""
        def download(url_: str) -> None:
            """Get a url and download the video.

            :param url_: The url of the video to be downloaded."""
            try:
                # Make a YouTube object.
                youtube_video = pytube.YouTube(url_)

                # Get the video in highest resolution.
                main_video = youtube_video.streams.get_highest_resolution()

                # Download the video in the `Downloads` folder.
                main_video.download(output_path='C:\\Users\\Lenovo\\Downloads')

                # Change the message.
                self._message.config(text=f"Your video '{youtube_video.title}' has been downloaded successfully in "
                                          f'the downloads folder')
            except pytube.exceptions.RegexMatchError:
                # If there is no such video the change the message.
                self._message.config(text='No such video')
            except urllib.error.URLError:
                self._message.config(text='No Internet Connection')

        # Set the message to 'downloading...'
        self._message.config(text='Downloading...')

        # Update the screen after changing the message or else it will not change.
        self._screen.update()

        # Download
        download(url)

    def run(self) -> None:
        """Run the main youtube video downloader program."""
        # Grid the items
        self._image_label.grid(row=0, column=1, sticky='nsew')
        self._label_frame.grid(row=1, column=1, sticky='new')
        self._link_entry.grid(row=0, column=0, sticky='ew')
        self._download.grid(row=2, column=1)
        self._message.grid(row=3, column=0, sticky='nsew', columnspan=3)

        # The main loop.
        self._screen.mainloop()


if __name__ == '__main__':
    # Declare an instance variable and run the `run` method.
    youtube_downloader = YouTubeVideoDownloader()
    youtube_downloader.run()
