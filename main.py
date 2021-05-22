import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont, UnidentifiedImageError


class WatermarkingApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('Watermarking')
        self.geometry('900x700')
        self.config(pady=50)

        self.frame = tkinter.Frame(self, width=600, height=400)
        self.frame.grid(column=0, row=2, columnspan=3, padx=20, pady=20)
        self.canvas = tkinter.Canvas(self.frame, width=600, height=400)
        self.canvas.grid(column=0, row=0)
        self.h_bar = tkinter.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.canvas.xview)
        self.h_bar.grid(row=1, column=0, sticky=tkinter.EW)
        self.v_bar = tkinter.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.v_bar.grid(row=0, column=1, sticky=tkinter.NS)
        self.canvas.config(xscrollcommand=self.h_bar.set, yscrollcommand=self.v_bar.set)

        self.label_file_explorer = tkinter.Label(self, text='Choose an image file for watermarking.', width=100,
                                                 font=('Courier', 15, 'bold'))
        self.label_file_explorer.grid(column=0, row=0, columnspan=3)

        self.label_text = tkinter.Label(self, text='Name')
        self.label_text.grid(column=0, row=3)

        self.entry_text = tkinter.Entry(self, width=50)
        self.entry_text.grid(column=1, row=3, columnspan=2)

        self.button_explore = tkinter.Button(self, text='Choose file', command=self.choose_file)
        self.button_explore.grid(column=1, row=1, pady=10)

        self.button_watermark = tkinter.Button(self, text='Add watermark', command=self.watermarking)
        self.button_watermark.grid(column=0, row=4, pady=20)

        self.button_save = tkinter.Button(self, text='Save image file', command=self.save_image)
        self.button_save.grid(column=1, row=4, pady=20)

        self.button_exit = tkinter.Button(self, text='Exit', command=exit)
        self. button_exit.grid(column=2, row=4, pady=20)

        self.pil_img = None
        self.img = None
        self.filename = None

    def choose_file(self):
        self.filename = tkinter.filedialog.askopenfilename(initialdir='/', title='Choose a file')
        try:
            self.pil_img = Image.open(self.filename)
            self.img = ImageTk.PhotoImage(self.pil_img)
            self.canvas.create_image(0, 0, image=self.img, anchor='nw')
            self.update()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            self.label_file_explorer.configure(text=f'File opened: {self.filename}')
        except UnidentifiedImageError:
            self.label_file_explorer.configure(text='The file cannot be opened.')

    def watermarking(self):
        if self.img is None:
            self.label_file_explorer.configure(text='Choose a file first.')
        else:
            width, height = self.pil_img.size
            draw = ImageDraw.Draw(self.pil_img)
            text = f'© {self.entry_text.get()}'
            font = ImageFont.truetype('Arial.ttf', 15)
            text_width, text_height = draw.textsize(text, font=font)
            x = width - text_width - 10
            y = height - text_height - 10
            draw.rectangle((x - 5, y, x + text_width + 5, y + text_height), fill='white')
            draw.text((x, y), text, fill='black', font=font)
            self.img = ImageTk.PhotoImage(self.pil_img)
            self.canvas.create_image(0, 0, image=self.img, anchor='nw')
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def save_image(self):
        new_filename_list = self.filename.split('.')
        new_filename_list[-2] = new_filename_list[-2] + '_wm'
        new_filename = '.'.join(new_filename_list)
        self.pil_img.save(new_filename)
        self.label_file_explorer.configure(text=f'File saved: {new_filename}')


if __name__ == '__main__':
    app = WatermarkingApp()
    app.mainloop()
