from config_parser import set_config_variables
from get_chapters import get_chapters
from download_chapters import download_chapters
import os
from multiprocessing import Pool, cpu_count
import time

ROOT_URL = "https://www.mangaread.org/manga/"

def download_manga_worker(args):
    """Worker function to download a single manga"""
    manga_config, download_type = args
    
    try:
        os.makedirs(f"./Downloads/{manga_config.folder_name}", exist_ok=True)
        print(f"Process {os.getpid()}: Starting download of '{manga_config.mangaread_name}'...")
        
        start_time = time.time()
        
        chapters_list = get_chapters(url=f'{ROOT_URL}{manga_config.mangaread_name}')
        selected_chapters = chapters_list[manga_config.start_chapter - 1 : manga_config.end_chapter]
        
        print(f"Process {os.getpid()}: Found {len(selected_chapters)} chapters for '{manga_config.mangaread_name}'")
        
        download_chapters(
            chapters_list=selected_chapters,
            chapters_path=f"./Downloads/{manga_config.folder_name}",
            save_type=download_type
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Process {os.getpid()}: Completed download of '{manga_config.mangaread_name}' in {duration:.2f} seconds!")
        return f"Success: {manga_config.mangaread_name} ({len(selected_chapters)} chapters, {duration:.2f}s)"
        
    except Exception as e:
        print(f"Process {os.getpid()}: Error downloading '{manga_config.mangaread_name}': {str(e)}")
        return f"Error: {manga_config.mangaread_name} - {str(e)}"

def main():
    config = set_config_variables()

    if not config.manga_configs:
        print("No manga configurations found in config file!")
        return

    os.makedirs("./Downloads", exist_ok=True)

    if config.scale_threads_with_entries:
        num_processes = min(len(config.manga_configs), cpu_count())
    else:
        num_processes = min(4, len(config.manga_configs))  # 4 max processes
    
    print(f"Starting parallel downloads for {len(config.manga_configs)} manga using {num_processes} processes...")
    print(f"Available CPU cores: {cpu_count()}")
    start_time = time.time()
    
    worker_args = [(manga_config, config.download_type) for manga_config in config.manga_configs]
    try:
        with Pool(processes=num_processes) as pool:
            results = pool.map(download_manga_worker, worker_args)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user!")
        return
    except Exception as e:
        print(f"\nError during parallel processing: {str(e)}")
        return
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Print summary
    print("\n" + "="*60)
    print("Download Summary:")
    successful_downloads = 0
    failed_downloads = 0
    
    for result in results:
        print(f"  {result}")
        if result.startswith("Success"):
            successful_downloads += 1
        else:
            failed_downloads += 1
    
    print("-" * 60)
    print(f"Total time: {total_duration:.2f} seconds")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print("="*60)

if __name__ == "__main__":
    main()