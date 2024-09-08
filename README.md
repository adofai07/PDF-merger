# PDF merger

This Python program can merge, split, and rotate multiple pdfs with a minimalistic interface.

## How to use

Put the pdfs you want to merge, split and rotate in the `inputs` folder. Then run `main.py`.

The program will print all the pdfs in the `inputs` folder, labeled and sorted:

```txt
[0] example1
[1] example2
[2] example3
[3] example4
[4] example5
```

When the program asks you to input files, (`File: `) you can input your desired files like the following.

### Simply merging multiple pdfs

Input `201` and the program will merge `example3.pdf`, `example1.pdf`, `example2.pdf` into `merged.pdf`.

### Splitting pdfs

You can specify pages of a certain pdf file. For example, `(3;1-3)` means pages 1 to 3 of `example4.pdf`. The pages start at 1 and are inclusive.

The input `0(1;4-5)` will merge `example1.pdf` and pages 4-5 of `example2.pdf` into `merged.pdf`.

### Rotating pdfs

Rotating pdfs is also pretty simple: you just put `+` in front of a character to tell the program to rotate it 90° clockwise. `-` means 90° counterclockwise, and `=` means 180°.

You can also rotate and split pdf files at once; `(+4;1-2)` means pages 1-2 of `example5.pdf`, rotated 90° clockwise.