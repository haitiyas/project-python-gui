import tkinter as tk
import numpy
from tkinter.filedialog import askopenfilename
import shutil
import os
from PIL import Image, ImageTk

window = tk.Tk()
window.title(" ")

window.geometry("500x510")
window.configure(background ="black")
title = tk.Label(text="Click below to choose picture for ecryption/decryption", background = "black", fg="gray", font=("", 15))
title.grid()

def openphotoencrypt():

    ### this line makes the variables accessible everywhere
    global width,height, mean
    import numpy as np
    import random

    fileName = askopenfilename(initialdir='', title='Select image',
                filetypes=[('image files', '.jpg')])
    photo = Image.open(fileName)

    height = np.size(photo, 0)
    width = np.size(photo, 1)
    mean = np.mean(photo)

    row, col = photo.size
    pixels = photo.load()

    row1 = 1000003
    phi = [0 for x1 in range(row1)]
    occ = [0 for x1 in range(row1)]
    primes = []
    phi[1] = 1
    # phi[2] = 1
    # print (phi)
    for i in range(2, 1000001):
        # print (i)
        if (phi[i] == 0):
            phi[i] = i - 1
            # print (i)
            primes.append(i)
            # j = 2*i
            for j in range(2 * i, 1000001, i):
                # print("j ",j)
                # print(j)
                if (occ[j] == 0):
                    # print ("inside if2")
                    occ[j] = 1
                    phi[j] = j
                # print (phi[j])
                # print ((i-1)//i)
                phi[j] = (phi[j] * (i - 1)) // i
            # print(phi[j])
            # j = j + i
    # print (primes)
    p = primes[random.randrange(1, 167)]
    q = primes[random.randrange(1, 167)]
    print(p, " ", q)
    n = p * q
    mod = n
    phin1 = phi[n]
    phin2 = phi[phin1]
    e = primes[random.randrange(1, 9000)]
    mod1 = phin1

    def power1(x, y, m):
        ans = 1
        while (y > 0):
            if (y % 2 == 1):
                ans = (ans * x) % m
            y = y // 2
            x = (x * x) % m
        return ans

    d = power1(e, phin2 - 1, mod1)
    enc = [[0 for x in range(row)] for y in range(col)]
    dec = [[0 for x in range(row)] for y in range(col)]
    for i in range(col):
        for j in range(row):
            r, g, b = pixels[j, i]
            r1 = power1(r + 10, e, mod)
            g1 = power1(g + 10, e, mod)
            b1 = power1(b + 10, e, mod)
            enc[i][j] = [r1, g1, b1]
    print(pixels[row - 1, col - 1])
    img = np.array(enc, dtype=np.uint8)
    img1 = Image.fromarray(img, "RGB")
    img1.save("encryption.jpg")

    render = ImageTk.PhotoImage(photo)
    img = tk.Label(image=render, height="250", width="500")
    img.image = render
    img.place(x=0, y=0)
    img.grid(column=0, row=1, padx=10, pady=10)

    render = ImageTk.PhotoImage(img1)
    img = tk.Label(image=render, height="250", width="500")
    img.image = render
    img.place(x=0, y=0)
    img.grid(column=0, row=4, padx=10, pady=10)

    width_txt = tk.Text(window, height=2, width=30, fg="WHITE", background="black", relief="flat")
    width_txt.grid(column=5, row=1)
    width_txt.insert(tk.END, "public key(e): " + str(e))

    height_txt = tk.Text(window, height=2, width=30, fg="WHITE", background="black", relief="flat")
    height_txt.grid(column=5, row=4)
    height_txt.insert(tk.END, "public key(n): " + str(n))

    title.destroy()
    button1.destroy()

def openphotodecrypt():
    global width, height, mean
    import numpy as np
    import random

    fileName = askopenfilename(initialdir='', title='Select image',
                               filetypes=[('image files', '.jpg')])
    photo1 = Image.open(fileName)

    height = np.size(photo1, 0)
    width = np.size(photo1, 1)
    mean = np.mean(photo1)

    row, col = photo1.size
    pixels = photo1.load()

    e = tk.Entry(window)
    n = tk.Entry(window)
    d = e**(-1)%n
    for i in range(col):
        for j in range(row):
            r, g, b = pixels[j,i]
            r1 = power1(r, d, mod) - 10
            g1 = power1(g, d, mod) - 10
            b1 = power1(b, d, mod) - 10
            dec[i][j] = [r1, g1, b1]
    img2 = numpy.array(dec, dtype=numpy.uint8)
    img3 = Image.fromarray(img2, "RGB")
    img3.save("decryption.jpg")

    render = ImageTk.PhotoImage(photo1)
    img = tk.Label(image=render, height="250", width="500")
    img.image = render
    img.place(x=0, y=0)
    img.grid(column=0, row=1, padx=10, pady=10)

    render = ImageTk.PhotoImage(img3)
    img = tk.Label(image=render, height="250", width="500")
    img.image = render
    img.place(x=0, y=0)
    img.grid(column=0, row=4, padx=10, pady=10)
    title.destroy()
    button2.destroy()


button1 = tk.Button(text="Get Photo to Encrypt", command=openphotoencrypt)
button1.grid(column=0, row=1, padx=10, pady=10)

button2 = tk.Button(text="Get Photo to Decrypt", command=openphotodecrypt)
button2.grid(column=0, row=3, padx=10, pady=10)

window.mainloop()