import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import datetime
import re
from fpdf import FPDF

class RPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de RPS - SP")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        self.setup_validations()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        
        # Abas
        self.tab_prestador = ttk.Frame(self.notebook)
        self.tab_tomador = ttk.Frame(self.notebook)
        self.tab_servico = ttk.Frame(self.notebook)
        
        self.create_prestador_tab()
        self.create_tomador_tab()
        self.create_servico_tab()
        
        self.notebook.add(self.tab_prestador, text="Prestador")
        self.notebook.add(self.tab_tomador, text="Tomador")
        self.notebook.add(self.tab_servico, text="Serviço")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Botões
        self.btn_frame = ttk.Frame(self.root)
        ttk.Button(self.btn_frame, text="Gerar PDF", command=self.gerar_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Sair", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        self.btn_frame.pack(pady=10)

    def create_prestador_tab(self):
        fields = [
            ('CNPJ/CPF:', 'prestador_cnpj'),
            ('Razão Social:', 'prestador_razao'),
            ('Inscrição Municipal:', 'prestador_im'),
            ('Endereço:', 'prestador_endereco')
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(self.tab_prestador, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(self.tab_prestador, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, var, entry)

    def create_tomador_tab(self):
        fields = [
            ('CNPJ/CPF Tomador:', 'tomador_cnpj'),
            ('Nome/Razão Social:', 'tomador_nome'),
            ('Inscrição Municipal:', 'tomador_im'),
            ('Endereço:', 'tomador_endereco')
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(self.tab_tomador, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(self.tab_tomador, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, var, entry)

    def create_servico_tab(self):
        ttk.Label(self.tab_servico, text="Tipo RPS:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tipo_rps = ttk.Combobox(self.tab_servico, values=["1 - RPS", "2 - Nota Fiscal"], state="readonly")
        self.tipo_rps.current(0)
        self.tipo_rps.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.tab_servico, text="Data Emissão:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.data_emissao = DateEntry(self.tab_servico, date_pattern='dd/mm/yyyy')
        self.data_emissao.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        numeric_fields = [
            ('Série:', 'serie'),
            ('Número RPS:', 'numero'),
            ('Valor Serviço (R$):', 'valor_servico'),
            ('ISS (R$):', 'iss')
        ]
        
        for i, (label, var) in enumerate(numeric_fields, start=2):
            ttk.Label(self.tab_servico, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(self.tab_servico, width=20)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
            setattr(self, var, entry)
            
        ttk.Label(self.tab_servico, text="Descrição Serviço:").grid(row=6, column=0, sticky=tk.NW, padx=5, pady=5)
        self.descricao = tk.Text(self.tab_servico, width=50, height=5)
        self.descricao.grid(row=6, column=1, padx=5, pady=5)

    def setup_validations(self):
        self.valor_servico.bind('<KeyRelease>', self.formatar_moeda)
        self.iss.bind('<KeyRelease>', self.formatar_moeda)
        self.prestador_cnpj.bind('<FocusOut>', self.validar_cnpj_cpf)
        self.tomador_cnpj.bind('<FocusOut>', self.validar_cnpj_cpf)

    def validar_cnpj_cpf(self, event):
        widget = event.widget
        valor = widget.get().strip()
        cleaned = re.sub(r'[^0-9]', '', valor)
        
        if len(cleaned) not in (11, 14):
            widget.config(foreground='red')
            return False
        widget.config(foreground='black')
        return True

    def formatar_moeda(self, event):
        widget = event.widget
        valor = widget.get().replace('R$', '').replace('.', '').replace(',', '').strip()
        
        try:
            if valor:
                valor_float = float(valor) / 100
                formatted = f"R$ {valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                widget.delete(0, tk.END)
                widget.insert(0, formatted)
                widget.config(foreground='black')
        except:
            widget.config(foreground='red')

    def validar_dados(self):
        required = [
            (self.prestador_cnpj, 'CNPJ/CPF Prestador'),
            (self.prestador_razao, 'Razão Social Prestador'),
            (self.tomador_cnpj, 'CNPJ/CPF Tomador'),
            (self.valor_servico, 'Valor do Serviço')
        ]
        
        for field, name in required:
            if not field.get().strip():
                messagebox.showerror("Erro", f"Campo obrigatório: {name}")
                field.config(foreground='red')
                return False
            field.config(foreground='black')
        
        try:
            datetime.datetime.strptime(self.data_emissao.get(), '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "Data de emissão inválida!")
            self.data_emissao.config(foreground='red')
            return False
        
        try:
            float(self.valor_servico.get().replace('R$', '').replace('.', '').replace(',', '.'))
            float(self.iss.get().replace('R$', '').replace('.', '').replace(',', '.'))
        except:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
            return False
        
        return True

    def criar_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Recibo Provisório de Serviços (RPS)", 0, 1, 'C')
        pdf.set_font("Arial", '', 12)
        
        # Dados Prestador
        pdf.cell(0, 10, "Prestador:", 0, 1)
        pdf.cell(0, 8, f"CNPJ/CPF: {self.prestador_cnpj.get()}", 0, 1)
        pdf.cell(0, 8, f"Razão Social: {self.prestador_razao.get()}", 0, 1)
        pdf.ln(5)
        
        # Dados Tomador
        pdf.cell(0, 10, "Tomador:", 0, 1)
        pdf.cell(0, 8, f"CNPJ/CPF: {self.tomador_cnpj.get()}", 0, 1)
        pdf.cell(0, 8, f"Nome/Razão Social: {self.tomador_nome.get()}", 0, 1)
        pdf.ln(10)
        
        # Detalhes Serviço
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Detalhes do Serviço", 0, 1)
        pdf.set_font("Arial", '', 12)
        
        dados = [
            ("Tipo RPS", self.tipo_rps.get()),
            ("Série", self.serie.get()),
            ("Número", self.numero.get()),
            ("Data Emissão", self.data_emissao.get()),
            ("Valor Serviço", f"R$ {self.valor_servico.get()}"),
            ("ISS", f"R$ {self.iss.get()}"),
            ("Descrição", self.descricao.get('1.0', tk.END).strip())
        ]
        
        for label, valor in dados:
            pdf.cell(50, 8, f"{label}:", 0, 0)
            pdf.multi_cell(0, 8, str(valor), 0, 1)
            pdf.ln(2)
        
        pdf.ln(10)
        pdf.cell(0, 8, f"Emitido em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'R')
        return pdf

    def gerar_pdf(self):
        if not self.validar_dados():
            return
        
        nome_arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"RPS_{self.numero.get()}.pdf"
        )
        
        if nome_arquivo:
            try:
                pdf = self.criar_pdf()
                pdf.output(nome_arquivo)
                messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar PDF:\n{str(e)}")

    def limpar_campos(self):
        for tab in [self.tab_prestador, self.tab_tomador, self.tab_servico]:
            for widget in tab.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)
                    widget.config(foreground='black')
                elif isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
        self.tipo_rps.current(0)
        self.data_emissao.set_date(datetime.date.today())

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSApp(root)
    root.mainloop()