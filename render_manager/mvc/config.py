# -----------------------------------------------------------------------------------------
# Max Rocamora / maxirocamora@gmail.com / https://github.com/MaxRocamora
# -----------------------------------------------------------------------------------------

# column order, label and width
MODEL_DATA = [
    (0, 'layer', 140),  # name of the render layer
    (1, 'nuke version', 80),  # scene layer, version
    (2, 'nuke range', 80),  # current nuke read range
    (3, 'nuke frames', 80),  # frames count
    (4, 'status', 105),  # icon/scene status
    (5, 'version', 70),  # last layer, version
    (6, 'range', 80),  # current disk layer range
    (7, 'frames', 70),  # frames count
    (8, 'aov', 60),  # aovs count
]

# empty dict with text blocks for displayRole in modelview
MODEL_DISPLAYROLE = {i: '---' for i in range(len(MODEL_DATA))}


if __name__ == '__main__':
    print(MODEL_DISPLAYROLE)
