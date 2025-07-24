import toml
import os

CONFIG_LOCATIONS = ["./config.toml", "~/.config/mangareadpuller/config.toml"]

class MangaConfig:
    def __init__(
            self,
            mangaread_name: str,
            folder_name: str,
            start_chapter: int,
            end_chapter: int
            ) -> None:
        self.mangaread_name = mangaread_name
        self.folder_name = folder_name
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter

class ConfigurationType:
    def __init__(
            self,
            scale_threads_with_entries: bool,
            download_type: str,
            manga_configs: list[MangaConfig]
            ) -> None:
        self.scale_threads_with_entries = scale_threads_with_entries
        self.download_type = download_type
        self.manga_configs = manga_configs

    

def find_config_location() -> str | None:
    for location in CONFIG_LOCATIONS:
        if os.path.exists(location):
            return location
    return None; 

def load_config(config_path: str) -> ConfigurationType:
    parsed_toml = toml.load(config_path)

    # threaded = parsed_toml["grabber-config"]["scale-threads"]
    threaded = True # I will add single-core support later.
    download_type = parsed_toml["grabber-config"]["download-type"]

    if download_type != "image_dir" and download_type != "cbz":
        raise Exception("Invalid download type! set to 'image_dir' or 'cbz'!")
    
    manga_configs: list[MangaConfig] = []

    for key in parsed_toml:
        print(key)
        if key == "grabber-config":
            continue

        manga_configs.append(MangaConfig(
            mangaread_name = key,
            folder_name = parsed_toml[key]['folder-name'],
            start_chapter = parsed_toml[key]['start-chapter'],
            end_chapter = parsed_toml[key]['end-chapter']
        ))


    return ConfigurationType(
        scale_threads_with_entries = threaded,
        download_type = download_type,
        manga_configs = manga_configs
    )

def set_config_variables() -> ConfigurationType:
    location = find_config_location()
    if location:
        return load_config(location)
    else:
        raise Exception("No configuration file found!")
