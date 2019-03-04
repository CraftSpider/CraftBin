
import win10toast
import json
import sys
import pathlib
import datetime as dt


DATA_FILE = pathlib.Path(__file__).parent / "../data/"
TRANSFORM = {
    "M": 0, "T": 1, "W": 2, "Th": 3, "F": 4, "S": 5, "Su": 6, "NS": 7
}


def main():
    notifier = win10toast.ToastNotifier()

    with open(DATA_FILE / "comics.json", "a+") as file:
        if file.tell() == 0:
            file.write("[]")
            print("No comics file found, new file created")
            sys.exit(1)
        file.seek(0)
        try:
            comics = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Failed to load comics file: {e}")
            sys.exit(1)

    weekday = dt.date.today().weekday()

    for comic in comics:
        dates = comic["dates"]
        if dates[0] != "E":
            for date in dates:
                if weekday == TRANSFORM[date]:
                    break
            else:
                continue

        icon = DATA_FILE / "icons/default.ico"
        if comic.get("icon") is not None:
            icon = DATA_FILE / comic["icon"]

        if not icon.is_file():
            print("Can't find configured icon, using default")
            icon = None
        elif icon.suffix != ".ico":
            print("Provided icon of incompatible type, using default")
            icon = None

        notifier.show_toast("Comics Notifier", f"{comic['name']} updates today", icon)


if __name__ == "__main__":
    main()
