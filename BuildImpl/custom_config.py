from BeyondCV.config import custom_config

config: dict[str, str | float | bool] = {
    "paper_size": "A4",
    "margin_top_cm": 1,
    "margin_bottom_cm": 1,
    "margin_right_cm": 1,
    "margin_left_cm": 1,
    "header_from_top_cm": 0.5,
    "default_font": "Times New Roman",
    "use_cache": True,
}

def update():
    custom_config(config)
    print("Updated")
