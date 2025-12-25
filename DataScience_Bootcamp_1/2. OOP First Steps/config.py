import sys

data_file = sys.argv[1] if len(sys.argv) > 1 else '../ex00/data.csv'
num_of_steps = 3

report_template = """We made {num_observations} observations by tossing a coin: {num_tails} were tails and {num_heads} were heads. The probabilities are {tail_prob}% and {head_prob}%, respectively. Our forecast is that the next {num_steps} observations will be: {forecast}."""

telegram_bot_token = "8333509939:AAESbsP1BMHNxEUeluygomuJt9XrCM_uAN4"
telegram_chat_id = 1070769036