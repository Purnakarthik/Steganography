import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(b, 2)) for b in chars])

def embed_data(image_path, message, output_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    binary = text_to_bin(message) + '1111111111111110'
    data = list(img.getdata())
    new_data = []
    bin_index = 0
    for pixel in data:
        r, g, b = pixel
        if bin_index < len(binary):
            r = (r & ~1) | int(binary[bin_index])
            bin_index += 1
        if bin_index < len(binary):
            g = (g & ~1) | int(binary[bin_index])
            bin_index += 1
        if bin_index < len(binary):
            b = (b & ~1) | int(binary[bin_index])
            bin_index += 1
        new_data.append((r, g, b))
    img.putdata(new_data)
    img.save(output_path)
    return output_path

def extract_data(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    data = list(img.getdata())
    binary = ''
    for pixel in data:
        for color in pixel:
            binary += str(color & 1)
        if binary.endswith('1111111111111110'):
            break
    return bin_to_text(binary[:-16])

def browse_image(entry):
    path = filedialog.askopenfilename(filetypes=[('Image files', '*.png *.bmp')])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def save_output(entry):
    path = filedialog.asksaveasfilename(defaultextension='.png')
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def encode():
    path = image_path_entry.get()
    message = message_entry.get('1.0', tk.END).strip()
    output = output_path_entry.get()
    if not path or not message or not output:
        messagebox.showwarning('Input Error', 'Please fill all fields.')
        return
    try:
        embed_data(path, message, output)
        messagebox.showinfo('Success', f'Message hidden and saved to {output}')
    except Exception as e:
        messagebox.showerror('Error', str(e))

def decode():
    path = extract_image_entry.get()
    if not path:
        messagebox.showwarning('Input Error', 'Please select an image.')
        return
    try:
        hidden_msg = extract_data(path)
        messagebox.showinfo('Hidden Message', hidden_msg)
    except Exception as e:
        messagebox.showerror('Error', str(e))

root = tk.Tk()
root.title('Image Steganography Tool')
root.geometry('600x400')

tk.Label(root, text='Embed Message into Image', font=('Arial', 14)).pack(pady=10)
image_path_entry = tk.Entry(root, width=60)
image_path_entry.pack()
tk.Button(root, text='Browse Image', command=lambda: browse_image(image_path_entry)).pack(pady=2)
message_entry = tk.Text(root, height=4, width=60)
message_entry.pack()
output_path_entry = tk.Entry(root, width=60)
output_path_entry.pack()
tk.Button(root, text='Save As', command=lambda: save_output(output_path_entry)).pack(pady=2)
tk.Button(root, text='Encode Message', command=encode).pack(pady=5)

tk.Label(root, text='\nExtract Message from Image', font=('Arial', 14)).pack(pady=10)
extract_image_entry = tk.Entry(root, width=60)
extract_image_entry.pack()
tk.Button(root, text='Browse Image', command=lambda: browse_image(extract_image_entry)).pack(pady=2)
tk.Button(root, text='Decode Message', command=decode).pack(pady=5)

root.mainloop()
