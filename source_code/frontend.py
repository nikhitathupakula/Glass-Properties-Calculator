import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, ttk
from optical_properties import opt_prop, comp_split
from Batch_equation_splitting2 import eqtn_split
from Batch_calculation_gf3 import batch_calc
from mmsep_den_cn import M_M_sep, molar_volume, coord_num_avg
from pd_pf_opd import oxy_pack_density, effect_rem, optical_basicity

cn_entries = []


def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)
    for cn_entry in cn_entries:
        cn_entry.delete(0, tk.END)
        cn_entry.insert(0, 0)
    text_output1.delete(1.0, tk.END)
    text_output2.delete(1.0, tk.END)
    text_output3.delete(1.0, tk.END)


def ask_rem_selection(elements):
    global selected_rem_elements
    selected_rem_elements = []

    def on_confirm():
        selected_rem_elements.clear()
        for var, element in zip(checkbox_vars, elements):
            if var.get():
                selected_rem_elements.append(element)
        dialog.destroy()

    dialog = tk.Toplevel(root)
    dialog.title("Select Rare Earth Metals")
    dialog.geometry("400x200")

    checkbox_vars = []
    for element in elements:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(dialog, text=element, variable=var, font=("Times New Roman", 14))
        checkbox.pack(anchor="w", padx=20, pady=5)
        checkbox_vars.append(var)

    confirm_button = tk.Button(dialog, text="Confirm", command=on_confirm, font=("Times New Roman", 14))
    confirm_button.pack(pady=10)

    dialog.grab_set()
    dialog.wait_window()


def calculate():
    global cations, batch_wt, weightfractions, density, compounds

    # Clear previous outputs before starting new calculations
    text_output1.delete(1.0, tk.END)
    text_output2.delete(1.0, tk.END)
    text_output3.delete(1.0, tk.END)

    try:
        eqn = entries[0].get()
        info = eqtn_split(eqn)
        moles, compounds, derived, oxides = info[0], info[1], info[2], info[3]
    except Exception as e:
        text_output1.insert(tk.END, f"Error in equation splitting: {e}\n")
        return

    # Batch calculation
    try:
        batch_wt = float(entries[1].get())
        know = batch_calc(moles, compounds, derived, batch_wt)
        weightfractions, dermasses, total_compmass, grav_factors = know[0], know[1], know[2], know[3]
        org_mass = dermasses / 100
        text_output1.insert(tk.END,
                            f"Derived Mass: {round(total_compmass / 100, 4)}\nOriginal Mass: {round(org_mass, 4)}\n")
        text_output1.insert(tk.END, f"\nWeight Fractions: \n")
        for i, wf in enumerate(weightfractions):
            text_output1.insert(tk.END, f"{oxides[i]}:\t{wf}\n")
        text_output1.insert(tk.END, f"\nGravimetric Factors: \n")
        for i, gf in enumerate(grav_factors):
            text_output1.insert(tk.END, f"{oxides[i]}:\t{gf}\n")
    except Exception as e:
        text_output1.insert(tk.END, f"Error in batch calculation: {e}\n")
        return

    # Density calculation
    try:
        wt_air = float(entries[2].get())
        im_liq = entries[3].get().lower()
        wt_liq = float(entries[4].get())
        Vm_info = molar_volume(wt_air, wt_liq, im_liq, org_mass)
        density, Vm = Vm_info[0], Vm_info[1]
        text_output1.insert(tk.END, f"\nMolar Volume: {Vm}\n")
        text_output1.insert(tk.END, f"Density: {density}\n")

    except ValueError:
        try:
            # Ensure variables exist or prompt for missing ones
            if 'im_liq' not in locals():
                im_liq = simpledialog.askstring("Missing Value", "Enter immersion liquid name:", parent=root)
            if 'wt_air' not in locals():
                wt_air = simpledialog.askfloat("Missing Value", "Enter weight in air:", parent=root)
            if 'wt_liq' not in locals():
                wt_liq = simpledialog.askfloat("Missing Value", "Enter weight in immersion liquid:", parent=root)

            density = simpledialog.askfloat("Density Input", f"Enter density of {im_liq}:", parent=root)
            Vm_info = molar_volume(wt_air, wt_liq, im_liq, org_mass, density)
            density, Vm = Vm_info[0], Vm_info[1]
            text_output1.insert(tk.END, f"\nMolar Volume: {Vm}\n")
            text_output1.insert(tk.END, f"Density: {density}\n")

        except Exception as e:
            text_output1.insert(tk.END, f"Error in density calculation: {e}\n")

    # Metal-Metal separation
    try:
        sep_info = M_M_sep(moles, compounds, Vm)
        text_output2.insert(tk.END, "Metal-Metal Separation:\n")
        for oxd, m_m_sep in zip(oxides, sep_info[1]):
            text_output2.insert(tk.END, f"{oxd}: {m_m_sep:.4e}\n")
    except Exception as e:
        text_output2.insert(tk.END, f"Error in Metal-Metal separation: {e}\n")
        return

    # Packing factor calculation
    try:
        lists = comp_split(info[3])
        cations, cat_occ, ox_occ = lists[0], lists[1], lists[2]

        opd_info = oxy_pack_density(cations, ox_occ, sep_info[0], Vm)
        text_output2.insert(tk.END, f"\nOxygen Packing Density: {opd_info[1]}\n")
    except Exception as e:
        text_output2.insert(tk.END, f"Error in packing factor calculation: {e}\n")
        return

    # Coordination number calculation
    try:
        if cn_entries:
            # Process each CN entry, if empty treat it as None
            cn_values = [float(cn_entry.get()) if cn_entry.get() else None for cn_entry in cn_entries]
        else:
            cn_values = None
        cn_info = coord_num_avg(sep_info[0], Vm, cn_values)
        text_output3.insert(tk.END, f"{cn_info}\n")
    except Exception as e:
        text_output3.insert(tk.END, f"Error in coordination number calculation: {e}\n")
        return

    # Dopant Effect Calculation
    try:
        rem_infos = effect_rem(cations, batch_wt, weightfractions, density, compounds)
        z = rem_infos[0]
        rem_info = rem_infos[1]

        if z == 0:
            # Ask user for dopant manually
            dopant_element = simpledialog.askstring(
                "Dopant Input",
                "No dopant detected automatically.\nEnter dopant element symbol (e.g., W, Ti, Fe) or leave blank to skip:",
                parent=root
            )

            if dopant_element:
                dopant_charge = simpledialog.askinteger(
                    "Dopant Charge",
                    f"Enter the charge (valency) for {dopant_element}:",
                    minvalue=1,
                    maxvalue=10,
                    parent=root
                )

                if dopant_charge:
                    rem_infos = effect_rem(
                        cations, batch_wt, weightfractions, density, compounds,
                        dopant_element=dopant_element, dopant_charge=dopant_charge
                    )
                    z = rem_infos[0]
                    rem_info = rem_infos[1]

                    if z != 0:
                        for item in rem_info:
                            text_output2.insert(tk.END, f"\n{item}\n")
                    else:
                        text_output2.insert(tk.END,
                                            f"\nCould not match dopant {dopant_element} with cations list. Skipping dopant calculations.\n")
                else:
                    text_output2.insert(tk.END,
                                        f"\nNo charge entered for {dopant_element}. Skipping dopant-based calculations.\n")
                    z = 0
            else:
                text_output2.insert(tk.END, "\nNo dopant specified. Skipping dopant-based calculations.\n")
                z = 0
        else:
            text_output2.insert(tk.END, "\nDetected Dopant Effect:\n")
            for item in rem_info:
                text_output2.insert(tk.END, f"\n{item}\n")

    except Exception as e:
        text_output2.insert(tk.END, f"Error in dopant effect calculation: {e}\n")

    # Optical Basicity calculation
    try:
        r_i = float(entries[5].get())
        ob_info = optical_basicity(cations, sep_info[0], Vm, r_i, opd_info[0], info[3])
        text_output3.insert(tk.END, f"{ob_info}\n")
    except Exception as e:
        text_output3.insert(tk.END, f"Error in optical basicity calculation: {e}\n")
        return

    # Optical properties
    try:
        results = opt_prop(r_i, z, Vm)
        text_output3.insert(tk.END, f"\n{results}")
    except Exception as e:
        text_output3.insert(tk.END, f"Error in optical properties calculation: {e}\n")
        return


def generate_cn_entries():
    response = messagebox.askyesno("Coordination Number Entry", "Do you want to enter coordination numbers?")
    if not response:
        return
    else:
        eqn = entries[0].get()
        info = eqtn_split(eqn)
        oxides = info[3]

        for widget in cn_frame.winfo_children():
            widget.destroy()

        global cn_entries
        cn_entries = []
        for i, oxide in enumerate(oxides):
            lbl = tk.Label(cn_frame, text=f"CN for {oxide}:", font=('Times New Roman', 14))
            lbl.grid(row=0, column=i * 2, padx=5, pady=5, sticky='e')

            entry = tk.Entry(cn_frame, width=5, font=('Times New Roman', 14))
            entry.grid(row=0, column=i * 2 + 1, padx=5, pady=5, sticky='w')

            cn_entries.append(entry)


def update_font_size(event=None):
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    base_size = max(12, int(min(window_width, window_height) / 50))

    label.config(font=("Times New Roman", base_size))
    for lbl, entry in zip(labels, entries):
        lbl.config(font=("Times New Roman", base_size))
        entry.config(font=("Times New Roman", base_size))

    button_generate_cn.config(font=("Times New Roman", base_size))
    button_calculate.config(font=("Times New Roman", base_size))
    button_clear.config(font=("Times New Roman", base_size))
    text_output1.config(font=("Times New Roman", base_size))
    text_output2.config(font=("Times New Roman", base_size))
    text_output3.config(font=("Times New Roman", base_size))


root = tk.Tk()
root.geometry("1900x1080")
root.title("PhysicalParameters_v1.21")

label = tk.Label(root, text="PhysicalParameters", font=('Times New Roman', 18))
label.pack()

labels_text = [
    "Equation:",
    "Batch Weight:",
    "Weight of Comp in air:",
    "Immersion Liquid:",
    "Wt of Comp in Imm Liq:",
    "Refractive index:",
]

labels = []
entries = []

for text in labels_text:
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=5, fill=tk.X)

    lbl = tk.Label(frame, text=text, font=('Times New Roman', 14), width=20, anchor='w')
    lbl.pack(side=tk.LEFT, padx=(5, 10))

    entry = tk.Entry(frame, width=100, font=('Times New Roman', 14))
    entry.pack(side=tk.LEFT, padx=(0, 10))

    labels.append(lbl)
    entries.append(entry)

button_generate_cn = tk.Button(root, text="Enter Coordination Numbers", width=50, command=generate_cn_entries)
button_generate_cn.pack(padx=20, pady=10)

cn_frame = tk.Frame(root)
cn_frame.pack(padx=20, pady=(0, 10))

button_frame = tk.Frame(root)
button_frame.pack(padx=20, pady=10)

button_calculate = tk.Button(button_frame, text="Calculate", width=25, command=calculate)
button_calculate.pack(side=tk.LEFT, padx=10)

button_clear = tk.Button(button_frame, text="Clear", width=25, command=clear_fields)
button_clear.pack(side=tk.LEFT, padx=10)

text_output1 = scrolledtext.ScrolledText(root, width=33, height=20, font=('Times New Roman', 16), padx=20, pady=20)
text_output1.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

text_output2 = scrolledtext.ScrolledText(root, width=33, height=20, font=('Times New Roman', 16), padx=20, pady=20)
text_output2.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

text_output3 = scrolledtext.ScrolledText(root, width=33, height=20, font=('Times New Roman', 16), padx=20, pady=20)
text_output3.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

root.bind('<Configure>', update_font_size)

root.mainloop()
