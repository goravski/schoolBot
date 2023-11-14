dict = {
    "Day of week, 13": [
        ["1.Item1", " ", "10"],
        ["2.Item2", " ", " "],
        ["3.Item3", "theme 9, ex.2, # 2.184-2.188", "7"],
        ["4.Item4", " ", " "],
        ["5.Item5", " ", " "],
        ["6.Item6", "Text. 1-5, 8-9", " "],
        ["7.", " ", " "],
    ],
}


def transform_dict_to_text(dict) -> str:
    text = ""
    for key, values in dict.items():
        text += "".join(f"\n{key}\n")
        for value in values:
            str = ""
            for index, item in enumerate(value):
                if index == 0:
                    str += f"{item}/n"
                if index == 1:
                    str += f"        д/з: {item}/n"
                if index == 2:
                    str += f"        оц.= {item}/n"
            text += "".join(f"{str}\n")
    return text


text = transform_dict_to_text(dict=dict)

print(text)
