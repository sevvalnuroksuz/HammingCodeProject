import tkinter as tk
from tkinter import messagebox
import math

original_code = ""

def calculate_hamming():
    data = input_entry.get().strip()
    if not all(bit in "01" for bit in data) or len(data) not in (8, 16, 32):
        messagebox.showerror("Hata", "Lütfen sadece 8, 16 veya 32 bitlik ikili veri girin.")
        return

    m = len(data)
    r = 0
    while (2**r) < (m + r + 1):
        r += 1

    total_len = m + r
    hamming = ['0'] * (total_len + 1)  # 1-based index kullanılıyor

    j = 0    #veri yerleştirme
    for i in range(1, total_len + 1):
        if math.log2(i).is_integer():   
            continue
        hamming[i] = data[j]
        j += 1

    for i in range(r):
        idx = 2**i
        parity = 0
        for k in range(1, total_len + 1):
            if k & idx:
                parity ^= int(hamming[k])
        hamming[idx] = str(parity)

    global original_code
    original_code = ''.join(hamming[1:])  # index 0 kullanılmıyor
    result_code_var.set(original_code)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "Hamming kodu oluşturuldu.")

def inject_and_check():
    global original_code
    if not original_code:
        messagebox.showwarning("Uyarı", "Önce Hamming kodunu oluşturmalısınız.")
        return

    try:
        pos = int(error_entry.get())
        if pos < 0 or pos >= len(original_code):
            raise ValueError
    except ValueError:
        messagebox.showerror("Hata", f"Pozisyon 0-{len(original_code) - 1} aralığında olmalı.")
        return

    errored = list("0" + original_code)  # 1-based index için başa boş bit
    bit_pos = pos + 1  # kullanıcı 0-based giriyor

    errored[bit_pos] = '1' if errored[bit_pos] == '0' else '0'

    r = 0
    while 2**r <= len(errored) - 1:
        r += 1

    syndrome = 0
    syndrome_bits = ""
    for i in range(r):
        idx = 2**i
        parity = 0
        for k in range(1, len(errored)):
            if k & idx:
                parity ^= int(errored[k])
        syndrome_bits = str(parity) + syndrome_bits
        if parity != 0:
            syndrome += idx

    message = f"Hatalı Kod: {''.join(errored[1:])}\n"
    message += f"Sendrom word: {syndrome_bits}\n"

    if syndrome == 0:
        message += "Hata algılanmadı."
    else:
        message += f"Bit hatası tespit edildi. Hatalı bit pozisyonu: {syndrome}\n"
        errored[syndrome] = '1' if errored[syndrome] == '0' else '0'
        message += f"Düzeltilmiş Kod: {''.join(errored[1:])}"

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, message)

def clear_all():
    input_entry.delete(0, tk.END)
    error_entry.delete(0, tk.END)
    result_code_var.set("")
    result_box.delete("1.0", tk.END)
    global original_code
    original_code = ""

# GUI
root = tk.Tk()
root.title("Hamming SEC Uygulaması")
root.geometry("700x500")
root.config(bg="#1F1F1F")

tk.Label(root, text="Hamming SEC-DED Code Simülatörü", font=("Helvetica", 20, "bold"), bg="#C2F5E7").pack(pady=10)

tk.Label(root, text="Veri Girişi (8, 16, 32 bit):", bg="#D9FFB8", font=("Arial", 12)).pack()
input_entry = tk.Entry(root, font=("Consolas", 14), bg="#E8F5E9", width=40)
input_entry.pack(pady=5)

tk.Button(root, text="Hamming Kodunu Hesapla", font=("Arial", 12), command=calculate_hamming, bg="#F9F6AB").pack(pady=5)

result_code_var = tk.StringVar()
tk.Label(root, textvariable=result_code_var, bg="#E5DFDF", font=("Courier", 12)).pack(pady=5)

tk.Label(root, text="Hata Pozisyonu Giriniz:", bg="#FFDCF9", font=("Arial", 12)).pack()
error_entry = tk.Entry(root, font=("Consolas", 14), bg="#FAD9DE", width=10)
error_entry.pack(pady=5)

tk.Button(root, text="Hata Ekle ve Kontrol Et", font=("Arial", 12), command=inject_and_check, bg="#FAF4BA").pack(pady=5)

result_box = tk.Text(root, height=10, font=("Consolas", 12), width=70, bg="#D2F1F9")
result_box.pack(pady=10)

tk.Button(root, text="Temizle", font=("Arial", 12), command=clear_all, bg="#F2926D").pack(pady=5)

root.mainloop()
