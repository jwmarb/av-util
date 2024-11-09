import os


class Config:
    BASE_URL_PATH = "assets/"
    WAVE_COMPLETED = "wave_completed.png"
    FREE_ROAM_BTN = "free_roam.png"
    VOTE_START = "vote_start.png"
    REWARD_GEM_ICON = "gem.png"
    STRONG_MODIFIER = "strong.png"
    THRICE_MODIFIER = "thrice.png"
    REGEN_MODIFIER = "regen.png"
    REVITALIZE_MODIFIER = "revitalize.png"
    VICTORY = "victory.png"
    REWARD_TROPHY_ICON = "trophy.png"

    def join_paths(*args) -> str:
        return os.path.join(Config.BASE_URL_PATH, *args)
