# Mangaread Grabber
*A multiprocessed downloader for* [***Mangaread***](https://www.mangaread.org/).

## Installation
- Ensure you have a (somewhat) modern version of `python3` installed.
- Clone this project, create a `venv`, and download the requirements:
``` bash
git clone https://github.com/ryannn2424/mangaread-grabber.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```
- You're now ready to [use the grabber!](#usage)

## Usage
- Manga downloads are done through the `config.toml` file. There are **four essential entries per manga you'd like to download:**
- `[manga-name]`: The 'title' mangaread uses to identify a manga. This can be obtained by grabbing the underline part in this example URL:

www.mangaread.org/manga/<u>chainsaw-man</u>/

- `folder-name`: the name that the downloaded files will be placed.
- `start-chapter`: The chapter # that you want to start downloading from
- `end-chapter`: The chapter # that you want to stop downloading at

>[!TIP]
>You can use `-1` to select the latest chapter

An example config can be seen below:
``` toml
[grabber-config] # This title is unique - you cannot download from it.
download-type = "cbz" # Available options: image_dir, cbz 

[chainsaw-man]
folder-name = "Chainsaw Man" 
start-chapter = 25 
end-chapter = 40 

[jujutsu-kaisen]
folder-name = "Jujutsu Kaisen"
start-chapter = 10
end-chapter = 50
```

>[!NOTE]
>All entries will be downloaded in parallel, speeding up your download times.

- After your config file is complete, simply run (whilst in your `venv`):
```
python main.py
```
- Your terminal will update you with the download status, and the resulting files will be placed inside of the `Downloads` folder.
