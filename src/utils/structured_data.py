def build_skeleton():
    skeleton = []
    for base in range(1, 22, 3):
        left, mid, right = f"point{base}", f"point{base+1}", f"point{base+2}"
        skeleton += [[left, mid], [mid, right]]

    for top in (2, 5, 8, 11, 14, 17):
        skeleton.append([f"point{top}", f"point{top+3}"])

    return skeleton