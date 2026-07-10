import TkEasyGUI as eg

# define UI
layout = [[eg.Frame("Unit:",layout=[
                [eg.Radio("unit1", group_id="unit", key="unit1", enable_events=True),
                 eg.Radio("unit2", group_id="unit", key="unit2", enable_events=True)],
                [eg.Radio("unit3", group_id="unit", key="unit3", enable_events=True)],
            ],)],

    [eg.Button("Exit")],
]
window = eg.Window("Radio samples:", layout)
while window.is_running():
    event, values = window.read()
    print("values=", values)

    if event == "Exit":
        break
window.close()