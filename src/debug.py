from datetime import datetime, timedelta
import time
import colored


class console:
    def log(*args):
        print(
            f"{colored.fore_rgb(128, 128, 128)}{datetime.now().strftime(r'%m-%d %H:%M:%S')} | {colored.Fore.BLUE}[LOG]{colored.Style.reset} {''.join(args)}"
        )

    def warn(*args):
        print(
            f"{colored.fore_rgb(128, 128, 128)}{datetime.now().strftime(r'%m-%d %H:%M:%S')} | {colored.Fore.YELLOW}[WARNING]{colored.Style.reset} {''.join(args)}"
        )

    def error(*args):
        print(
            f"{colored.fore_rgb(128, 128, 128)}{datetime.now().strftime(r'%m-%d %H:%M:%S')} | {colored.Fore.RED}[ERROR]{colored.Style.reset} {''.join(args)}"
        )

    def stats(games, wins, losses):
        print(
            f"{colored.fore_rgb(128, 128, 128)}{datetime.now().strftime(r'%m-%d %H:%M:%S')} | {colored.fore_rgb(255,0,255)}[STATS] {colored.Fore.YELLOW}{games} game{'s' if games != 1 else ''} {colored.Style.reset}({colored.Fore.GREEN}{wins}W{colored.Style.reset}:{colored.Fore.RED}{losses}L{colored.Style.reset})"
        )

    def time(games, start_time):
        print(
            f"{colored.fore_rgb(128, 128, 128)}{datetime.now().strftime(r'%m-%d %H:%M:%S')} | {colored.fore_rgb(255,0,255)}[STATS] {colored.fore_rgb(255,165,0)}Game AVG Time:{colored.Style.reset} {timedelta(seconds=time.time() - (start_time if start_time != None else time.time()))}"
        )
