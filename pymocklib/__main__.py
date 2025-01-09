
from pymocklib import styles
from pymocklib.styles import style_doc


if __name__ == "__main__":
    print(
        "\n".join(
            ["Here's what I can do:", ""]
            + [f"{name}: {style_doc(name)}" for (name, _) in styles]
        )
    )
