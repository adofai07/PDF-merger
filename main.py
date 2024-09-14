import PyPDF2
import glob
import tqdm
import string
import shutil
import os

def is_good_string(s: str) -> bool:
    if s.count("(") != s.count(")"):
        return False
    
    cnt = 0

    for i in s:
        if i == "(":
            cnt += 1

        if i == ")":
            cnt -= 1

        if cnt != 0 and cnt != 1:
            return False
        
    return True


def merge_pdfs(file_names: list[str], output_file: str="merged"):
    merger = PyPDF2.PdfWriter()
    l = len(file_names)

    print("\nReading...")

    for cnt, f in enumerate(file_names):
        # r = random.randrange(0, 100_000_000_000)
        r = cnt

        shutil.copyfile(
            f"inputs/{f}.pdf",
            f"cache/{r :012.0f}.pdf",
        )

        merger.append(f"cache/{r :012.0f}.pdf")

        print(f"{cnt + 1} / {l}, {len(merger.pages)} pages")

    # print(merger.pages[0].mediabox.width, merger.pages[0].mediabox.height)
    # print(merger.pages[2].mediabox.width, merger.pages[2].mediabox.height)

    print("Writing...")
    merger.write(f"{output_file}.pdf")

    merger.close()

files = [i[7:-4] for i in glob.glob("inputs/*.pdf")]
mapstr = string.digits + string.ascii_lowercase + string.ascii_uppercase
filename = "merged"

files.sort()

assert len(files) <= len(mapstr)

print()
for i in range(len(files)):
    print(f"[{mapstr[i]}]", files[i])

print()

s = input("Files: ")
sl = []

assert is_good_string(s)

idx = 0
l = len(s)

while idx < l:
    sl.append("")

    if   s[idx] == "(":
        idx += 1

        while s[idx] != ")":
            sl[-1] += s[idx]
            idx += 1

    elif s[idx] in "+-=":
        sl[-1] += s[idx]
        idx += 1
        sl[-1] += s[idx]

    else:
        sl[-1] += s[idx]

    idx += 1

for i in range(len(sl)):
    if   ";" in sl[i] and "-" in sl[i]:
        sl[i] = [sl[i].split(";")[0], int(sl[i].split(";")[1].split("-")[0]), int(sl[i].split(";")[1].split("-")[1])]

    # elif sl[i].startswith("+"):
    #     sl[i] = [sl[i][1:], 90]

    # elif sl[i].startswith("-"):
    #     sl[i] = [sl[i][1:], -90]

print(sl)
# input()

l = []

print(f"\nMerging {len(sl)} pdfs -> {filename}.pdf:\n")

for i in sl:
    if type(i) == str:
        if len(i) == 1:
            print(files[mapstr.index(i)])
            l.append(files[mapstr.index(i)])
        
        if len(i) == 2:
            if i[0] == "+":
                with open(f"inputs/{files[mapstr.index(i[1])]}.pdf", "rb") as infile:

                    reader = PyPDF2.PdfReader(infile)
                    writer = PyPDF2.PdfWriter()

                    for j in range(len(reader.pages)):
                        writer.add_page(reader.pages[j].rotate(90))

                    with open(f"inputs/c/{files[mapstr.index(i[1])]}_90_0_{len(reader.pages)}.pdf", "wb") as outfile:
                        writer.write(outfile)

                print(files[mapstr.index(i[1])], "(90° clockwise)")
                l.append(f"c/{files[mapstr.index(i[1])]}_90_0_{len(reader.pages)}")
                
            if i[0] == "-":
                with open(f"inputs/{files[mapstr.index(i[1])]}.pdf", "rb") as infile:

                    reader = PyPDF2.PdfReader(infile)
                    writer = PyPDF2.PdfWriter()

                    for j in range(len(reader.pages)):
                        writer.add_page(reader.pages[j].rotate(-90))

                    with open(f"inputs/c/{files[mapstr.index(i[1])]}_-90_0_{len(reader.pages)}.pdf", "wb") as outfile:
                        writer.write(outfile)

                print(files[mapstr.index(i[1])], "(90° counterclockwise)")
                l.append(f"c/{files[mapstr.index(i[1])]}_-90_0_{len(reader.pages)}")
                
            if i[0] == "=":
                with open(f"inputs/{files[mapstr.index(i[1])]}.pdf", "rb") as infile:

                    reader = PyPDF2.PdfReader(infile)
                    writer = PyPDF2.PdfWriter()

                    for j in range(len(reader.pages)):
                        writer.add_page(reader.pages[j].rotate(180))

                    with open(f"inputs/c/{files[mapstr.index(i[1])]}_-90_0_{len(reader.pages)}.pdf", "wb") as outfile:
                        writer.write(outfile)

                print(files[mapstr.index(i[1])], "(90° counterclockwise)")
                l.append(f"c/{files[mapstr.index(i[1])]}_-90_0_{len(reader.pages)}")

    if type(i) == list:
        if len(i) == 3:
            if len(i[0]) == 1:
                with open(f"inputs/{files[mapstr.index(i[0])]}.pdf", "rb") as infile:

                    reader = PyPDF2.PdfReader(infile)
                    writer = PyPDF2.PdfWriter()

                    for j in range(i[1] - 1, i[2]):
                        writer.add_page(reader.pages[j])

                    with open(f"inputs/c/{files[mapstr.index(i[0])]}_0_{i[1]}_{i[2]}.pdf", "wb") as outfile:
                        writer.write(outfile)

                print(f"{files[mapstr.index(i[0])]} (pages {i[1]}-{i[2]})")
                l.append(f"c/{files[mapstr.index(i[0])]}_0_{i[1]}_{i[2]}")

            if len(i[0]) == 2:
                if i[0][0] == "+":
                    with open(f"inputs/{files[mapstr.index(i[0][1])]}.pdf", "rb") as infile:

                        reader = PyPDF2.PdfReader(infile)
                        writer = PyPDF2.PdfWriter()

                        for j in range(i[1] - 1, i[2]):
                            writer.add_page(reader.pages[j].rotate(90))

                        with open(f"inputs/c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}.pdf", "wb") as outfile:
                            writer.write(outfile)

                    print(f"{files[mapstr.index(i[0][1])]} (90° clockwise, pages {i[1]}-{i[2]})")
                    l.append(f"c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}")
                    
                if i[0][0] == "-":
                    with open(f"inputs/{files[mapstr.index(i[0][1])]}.pdf", "rb") as infile:

                        reader = PyPDF2.PdfReader(infile)
                        writer = PyPDF2.PdfWriter()

                        for j in range(i[1] - 1, i[2]):
                            writer.add_page(reader.pages[j].rotate(-90))

                        with open(f"inputs/c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}.pdf", "wb") as outfile:
                            writer.write(outfile)

                    print(f"{files[mapstr.index(i[0][1])]} (90° counterclockwise, pages {i[1]}-{i[2]})")
                    l.append(f"c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}")
                    
                if i[0][0] == "=":
                    with open(f"inputs/{files[mapstr.index(i[0][1])]}.pdf", "rb") as infile:

                        reader = PyPDF2.PdfReader(infile)
                        writer = PyPDF2.PdfWriter()

                        for j in range(i[1] - 1, i[2]):
                            writer.add_page(reader.pages[j].rotate(180))

                        with open(f"inputs/c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}.pdf", "wb") as outfile:
                            writer.write(outfile)

                    print(f"{files[mapstr.index(i[0][1])]} (90° clockwise, pages {i[1]}-{i[2]})")
                    l.append(f"c/{files[mapstr.index(i[0][1])]}_90_{i[1]}_{i[2]}")



merge_pdfs(l, filename)

print("Merged")

for i in glob.glob("inputs/c/*.pdf"):
    print(f"Deleting {i}")
    os.remove(i)

for i in glob.glob("cache/*.pdf"):
    print(f"Deleting {i}")
    os.remove(i)