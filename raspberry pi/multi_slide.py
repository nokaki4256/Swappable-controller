"""
### Slider Test
"""
import TkEasyGUI as eg

def slide_wiget(number1):
    wiget = [eg.Slider(key="slide" + str(number1),
            range=[-90, 90], size=[6, 1],
            orientation="h",
            default_value=0, resolution=0.1,
            enable_events=True, disable_number_display=True),
            eg.Text("0.0", key="text"+ str(number1)),eg.Button("def")]
    
    return wiget

i = 0
j = 0
all_wiget = []
pass_data = []
_wiget = 0
_test = []

wiget_part1 = []
wiget_part2 = []
wiget_part3 = []

list_length = 3
base_count = 6
change_flag = 0

#ボタンの場合ボタンがイベントとして返す キーを設定すればキーを返す
for i in range(base_count * list_length):
    _wiget = slide_wiget(i)
    pass_data.append(_wiget)
all_wiget = pass_data.copy()
    
for i in range(base_count):
    wiget_part1 += all_wiget[i]
    wiget_part2 += all_wiget[i + base_count]
    wiget_part3 += all_wiget[i + 2 * base_count]

layout = [[eg.Frame("Unit:",layout=[[eg.Text("unit1")],wiget_part1,
          [eg.Text("unit2")],wiget_part2,
          [eg.Text("unit3")],wiget_part3,
          [eg.Button("Exit")]])]]
# create a window
window = eg.Window("Test", layout)

while True:
    event, values = window.read()
    
    #print(values["slide1"])
    
    #print(f"event={event} || values={values}")
    if event in ["Exit", eg.WIN_CLOSED]:
        break

    for i in range(base_count * list_length):
        if event == "slide" + str(i):
            v = values["slide" + str(i)]
            window["text" + str(i)].update(str(v))
        if event == "def":
            window["slide" + str(i)].update(value=0)
            window["text" + str(i)].update("0.0")

