import instaloader
from rich.console import Console
from src.instagram_reel_analyser import console_styles
import concurrent.futures

insta_loader = instaloader.Instaloader()
console = Console(force_terminal=True)


def download_reel(url):
    try:
        console.print(f"[INFO] Downloading reel from URL: {url}", style=console_styles.console_blue_styles)
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(insta_loader.context, shortcode)
        insta_loader.download_post(post, target=post.owner_username)
        video_path = f"{post.owner_username}/{shortcode}.mp4"
        result = {"path": video_path, "instagram_username": post.owner_username}
        console.print(f"[SUCCESS] Downloaded reel for user '{post.owner_username}' at '{video_path}'", style=console_styles.console_green_styles)
        return result
    except instaloader.InstaloaderException as e:
        console.print(f"[ERROR] Failed to download reel: {e}", style=console_styles.console_red_styles)
        return None
    except Exception as e:
        console.print(f"[ERROR] Unexpected error: {e}", style=console_styles.console_red_styles)
        return None


def download_instagram_reel(reel_url, compare_url):
    console.print("[INFO] Starting download of both reels...", style=console_styles.console_blue_styles)
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(download_reel, reel_url)
            future2 = executor.submit(download_reel, compare_url)
            result1 = future1.result()
            result2 = future2.result()
            if result1 and result2:
                console.print("[SUCCESS] Both reels downloaded successfully.", style=console_styles.console_green_styles)
            else:
                console.print("[WARNING] One or both reels failed to download.", style=console_styles.console_yellow_styles)
            return {"reel": result1, "compare": result2}
    except instaloader.InstaloaderException as ie:
        console.print(f"[ERROR] Instaloader error: {ie}", style=console_styles.console_red_styles)
        return None
    except Exception as e:
        console.print(f"[ERROR] An error occurred: {e}", style=console_styles.console_red_styles)
        return None
