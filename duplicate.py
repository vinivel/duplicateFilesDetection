import os
import shutil
import xxhash  # Instale com pip install xxhash
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox
from multiprocessing.pool import ThreadPool


def calcular_xxhash_completo(file_path):
    """Calcula o hash completo xxHash de um arquivo."""
    BUFFER_SIZE = 65536  # Tamanho do bloco de leitura
    hash_xx = xxhash.xxh64()

    try:
        with open(file_path, "rb") as file:
            for byte_block in iter(lambda: file.read(BUFFER_SIZE), b""):
                hash_xx.update(byte_block)
        return hash_xx.hexdigest()
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")
        return None


def obter_data_criacao_pasta(filepath):
    """Obtém a data de criação da pasta do arquivo."""
    try:
        pasta = os.path.dirname(filepath)  # Obter a pasta onde o arquivo está
        return os.path.getctime(pasta)  # Data de criação da pasta
    except Exception as e:
        print(f"Erro ao obter data de criação da pasta: {e}")
        return float("inf")  # Caso de erro, tratamos como data futura


class AppDuplicados(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Arquivos Duplicados")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.pasta_selecionada = None
        self.checkbox_vars = []  # Variáveis dos checkboxes
        self.total_arquivos = 0  # Total de arquivos a serem processados
        self.arquivos_analisados = 0  # Número de arquivos já verificados
        self.duplicados = defaultdict(list)  # Apenas arquivos duplicados

        # Paginação
        self.resultados_pagina = []  # Lista atual de duplicados na página
        self.itens_por_pagina = 100  # Exibir no máximo 100 duplicados por página
        self.pagina_atual = 0

        self.criar_interface()

    def criar_interface(self):
        """Cria a interface gráfica do programa."""
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", pady=10)

        label = ttk.Label(frame_top, text="Selecione uma pasta para verificar duplicados:")
        label.pack(side="left", padx=10)

        self.botao_selecionar = ttk.Button(frame_top, text="Selecionar Pasta", command=self.selecionar_pasta)
        self.botao_selecionar.pack(side="left", padx=10)

        self.label_pasta = ttk.Label(frame_top, text="", foreground="blue")
        self.label_pasta.pack(side="left", padx=10)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=10)

        self.status_label = ttk.Label(self, text="Status: Aguardando seleção da pasta.", anchor="w", foreground="green")
        self.status_label.pack(fill="x", padx=10)

        # Resultados
        self.resultados_frame = ttk.Frame(self)
        self.resultados_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.resultados_frame)
        self.scroll_y = ttk.Scrollbar(self.resultados_frame, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Botões de ação
        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill="x", pady=10)

        self.botao_anterior = ttk.Button(frame_botoes, text="<< Página Anterior", command=self.pagina_anterior,
                                         state=tk.DISABLED)
        self.botao_anterior.pack(side="left", padx=5)

        self.botao_proximo = ttk.Button(frame_botoes, text="Próxima Página >>", command=self.proxima_pagina,
                                        state=tk.DISABLED)
        self.botao_proximo.pack(side="right", padx=5)

        # Botão Mover Arquivos por Seleção
        self.botao_mover_arquivos = ttk.Button(self, text="Mover Arquivos Selecionados",
                                               command=self.mover_arquivos, state=tk.DISABLED)
        self.botao_mover_arquivos.pack(pady=5)

        # Botão Mover Automaticamente (Baseado em Pastas)
        self.botao_mover_automatico = ttk.Button(self, text="Mover Duplicados (Baseado em Pastas)",
                                                 command=self.mover_duplicados_por_pasta, state=tk.DISABLED)
        self.botao_mover_automatico.pack(pady=5)

    def selecionar_pasta(self):
        from tkinter import filedialog
        self.pasta_selecionada = filedialog.askdirectory(title="Selecione uma pasta")
        if self.pasta_selecionada:
            self.label_pasta.config(text=f"Pasta Selecionada: {self.pasta_selecionada}")
            self.status_label.config(text="Status: Processando arquivos...", foreground="orange")
            self.verificar_duplicados()

    def verificar_duplicados(self):
        """Inicia o processo de verificação de arquivos duplicados."""
        if not self.pasta_selecionada:
            messagebox.showinfo("Erro", "Selecione uma pasta primeiro.")
            return

        # Reset de estado
        self.duplicados.clear()
        self.arquivos_analisados = 0
        self.progress_bar["value"] = 0
        self.pagina_atual = 0

        # Contagem de arquivos
        self.total_arquivos = sum([len(files) for _, _, files in os.walk(self.pasta_selecionada)])

        # Processamento incremental
        arquivos_por_tamanho = defaultdict(list)
        for root, _, files in os.walk(self.pasta_selecionada):
            for file in files:
                caminho = os.path.join(root, file)
                try:
                    tamanho = os.stat(caminho).st_size
                    arquivos_por_tamanho[tamanho].append(caminho)
                except Exception as erro:
                    print(f"Erro ao acessar arquivo: {erro}")

        pool = ThreadPool(4)  # Utilizando 4 threads
        for tamanho, arquivos in arquivos_por_tamanho.items():
            if len(arquivos) > 1:  # Apenas para tamanhos repetidos
                resultados = pool.map(calcular_xxhash_completo, arquivos)
                for idx, hash_file in enumerate(resultados):
                    if hash_file:
                        self.duplicados[hash_file].append(arquivos[idx])

            self.arquivos_analisados += len(arquivos)
            self.atualizar_status()

        pool.close()
        pool.join()

        # Filtrar duplicados (apenas agrupamentos maiores que 1)
        self.duplicados = {hash_: paths for hash_, paths in self.duplicados.items() if len(paths) > 1}
        self.exibir_pagina()

        # Habilitar botões relevantes
        if self.duplicados:
            self.botao_mover_arquivos.config(state=tk.NORMAL)
            self.botao_mover_automatico.config(state=tk.NORMAL)

    def atualizar_status(self):
        """Atualiza status e barra de progresso."""
        porcentagem = (self.arquivos_analisados / self.total_arquivos) * 100
        self.progress_bar["value"] = porcentagem
        self.status_label.config(
            text=f"Status: {self.arquivos_analisados}/{self.total_arquivos} arquivos analisados...", foreground="blue"
        )
        self.update_idletasks()

    def mover_duplicados_por_pasta(self):
        """Move duplicatas que estão em pastas mais recentes."""
        pasta_destino = os.path.join(self.pasta_selecionada, "duplicados")
        os.makedirs(pasta_destino, exist_ok=True)

        arquivos_movidos = 0
        for hash_, arquivos in self.duplicados.items():
            # Ordenar arquivos com base na data da pasta
            arquivos.sort(key=obter_data_criacao_pasta)

            # Manter apenas o arquivo nas pastas mais antigas
            for arquivo in arquivos[1:]:
                try:
                    shutil.move(arquivo, os.path.join(pasta_destino, os.path.basename(arquivo)))
                    arquivos_movidos += 1
                except Exception as erro:
                    print(f"Erro ao mover arquivo {arquivo}: {erro}")

        messagebox.showinfo("Sucesso!", f"Arquivos movidos para '{pasta_destino}': {arquivos_movidos} duplicados.")

    def exibir_pagina(self):
        """Exibe uma parte (página) dos duplicados encontrados."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        hashes = list(self.duplicados.keys())
        inicio = self.pagina_atual * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        self.resultados_pagina = hashes[inicio:fim]

        for hash_ in self.resultados_pagina:
            frame = ttk.LabelFrame(self.scrollable_frame, text=f"Hash: {hash_}")
            frame.pack(fill="x", padx=10, pady=5)

            for arquivo in self.duplicados[hash_]:
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(frame, text=arquivo, variable=var)
                checkbox.pack(anchor="w", padx=5, pady=2)
                self.checkbox_vars.append((var, arquivo))

        self.botao_anterior.config(state=tk.NORMAL if self.pagina_atual > 0 else tk.DISABLED)
        self.botao_proximo.config(state=tk.NORMAL if fim < len(hashes) else tk.DISABLED)

    def mover_arquivos(self):
        """Move arquivos marcados no checkbox."""
        pasta_destino = os.path.join(self.pasta_selecionada, "duplicados")
        os.makedirs(pasta_destino, exist_ok=True)

        arquivos_para_mover = [arquivo for var, arquivo in self.checkbox_vars if var.get()]
        if not arquivos_para_mover:
            messagebox.showinfo("Erro", "Nenhum arquivo selecionado!")
            return

        for arquivo in arquivos_para_mover:
            try:
                shutil.move(arquivo, os.path.join(pasta_destino, os.path.basename(arquivo)))
            except Exception as erro:
                print(f"Erro ao mover arquivo {arquivo}: {erro}")

        messagebox.showinfo("Sucesso!", f"Arquivos movidos para '{pasta_destino}'.")
        self.verificar_duplicados()

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.exibir_pagina()

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.exibir_pagina()


# Execução do programa
if __name__ == "__main__":
    app = AppDuplicados()
    app.mainloop()
