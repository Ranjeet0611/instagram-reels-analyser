import instaloader
from rich.console import Console
import console_styles

insta_loader = instaloader.Instaloader()
console = Console(force_terminal=True)
def download_instagram_reel(reel_url):
   try:
       shortcode = reel_url.split("/")[-2]
       post = instaloader.Post.from_shortcode(insta_loader.context, shortcode)
       insta_loader.download_post(post, target=post.owner_username)
       console.print("Download Successfully", style=console_styles.console_green_styles)
   except:
         console.print("Failed to download reel. Please check the URL and try again.", style=console_styles.console_red_styles)

