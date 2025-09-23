# -----------------------------------------------------------------------------------------
# Max Rocamora / maxirocamora@gmail.com / https://github.com/MaxRocamora
# -----------------------------------------------------------------------------------------

# column order, label and width
MODEL_DATA = [
    (0, "Layer", 170),  # name of the render layer
    (1, "In Scripts", 80),  # scene layer version
    (2, "On disk", 80),  # on disk version
    (3, "Range", 80),  # current nuke read range
    (4, "Frames", 80),  # frames count
    (5, "Aovs", 60),  # aovs count
    (6, "Status", 105),  # icon/scene status
]

# empty dict with text blocks for displayRole in modelview
MODEL_DISPLAYROLE = {i: "---" for i in range(len(MODEL_DATA))}


if __name__ == "__main__":
    print(MODEL_DISPLAYROLE)
