def trypsin_cleave(ply_pep):
    ply_pep = ply_pep.upper()
    segs = []
    start = 0
    for i in range(len(ply_pep)):
        if (ply_pep[i] == "R" or ply_pep[i] == "K") and (i+1 == len(ply_pep) or ply_pep[i+1] != "P"):
            segs.append(ply_pep[start:i+1])
            start = i+1
    if start < len(ply_pep):
        segs.append(ply_pep[start:])
    return segs

def main():
    print(trypsin_cleave("KMKAFLRGYV"))
if __name__ == "__main__":
    main()