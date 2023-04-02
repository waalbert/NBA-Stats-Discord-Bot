from bs4 import BeautifulSoup

def get_roster(url: str) -> dict:
    roster = {}
    with open(url, "r") as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, "html.parser")
        roster_details = soup.select_one("#div_roster").find_all(["td", "th"])
        current_player = None
        player_order = 1
        for element in roster_details:
            text = remove_extra_whitespace(element.text)
            if element["data-stat"] == "number" and element["data-stat"] not in roster:
                if not text:
                    current_player = player_order
                else:
                    current_player = text
                roster[current_player] = {}
                player_order += 1
            if element["data-stat"] in ("number", "player", "pos", "height", "weight", "birth_date", "birth_country", "years_experience", "college"):
                roster[current_player][element["data-stat"]] = text
    return roster

def get_schedule(url: str) -> dict:
    schedule = {}
    with open(url, "r") as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, "html.parser")
        schedule_details = soup.select_one("#div_games").find_all(["td", "th"])
        current_game = None
        for element in schedule_details:
            text = remove_extra_whitespace(element.text)
            if element["data-stat"] == "g":
                current_game = text
                schedule[current_game] = {}
            elif element["data-stat"] in ("date_game", "game_start_time", "network", "box_score_text", "game_location", "opp_name", "game_result", "overtimes", "pts", "opp_pts", "wins", "losses", "game_streak", "game_remarks"):
                schedule[current_game][element["data-stat"]] = text
    return schedule

def remove_extra_whitespace(text: str) -> str:
    return " ".join(text.split())

def _print_data(roster: dict) -> None:
    for player_name, player_info in roster.items():
        print(player_name)
        for key, info in player_info.items():
            print(key, info)
        print()

# _print_data(get_roster("lakers.html"))
# _print_data(get_schedule("lakers_schedule.html"))