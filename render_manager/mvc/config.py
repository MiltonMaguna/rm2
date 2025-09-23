# -----------------------------------------------------------------------------------------
# Max Rocamora / maxirocamora@gmail.com / https://github.com/MaxRocamora
# -----------------------------------------------------------------------------------------

# column order, label and width
MODEL_DATA = [
    (0, "layer", 170),  # name of the render layer
    (1, "version", 80),  # scene layer, version
    (2, "range", 80),  # current nuke read range
    (3, "frames", 80),  # frames count
    (4, "aovs", 60),  # aovs count
    (5, "status", 105),  # icon/scene status
]

# empty dict with text blocks for displayRole in modelview
MODEL_DISPLAYROLE = {i: "---" for i in range(len(MODEL_DATA))}


if __name__ == "__main__":
    print(MODEL_DISPLAYROLE)
