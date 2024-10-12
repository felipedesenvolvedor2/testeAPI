import requests
import tkinter as tk
from tkinter import ttk, messagebox

def test_api_get(url, expected_status=200, expected_keys=None):
    """
    Testa um endpoint GET de uma API e verifica se o status e a estrutura do JSON retornado estão corretos.
    """
    try:
        response = requests.get(url)
        status_code = response.status_code
        
        # Verificar se o status code é o esperado
        if status_code == int(expected_status):
            status_msg = f"✅ Status {status_code} correto!"
        else:
            status_msg = f"❌ Status {status_code} incorreto! Esperado: {expected_status}"
        
        # Verificar as chaves esperadas, se forem fornecidas
        key_msg = ""
        if expected_keys:
            json_data = response.json()
            missing_keys = [key.strip() for key in expected_keys.split(",") if key.strip() not in json_data]
            if not missing_keys:
                key_msg = f"✅ Todas as chaves esperadas estão presentes: {expected_keys}"
            else:
                key_msg = f"❌ Chaves faltantes no JSON de resposta: {missing_keys}"
        
        # Atualizar o campo de saída com os resultados
        result_text.set(f"{status_msg}\n{key_msg}")
    except Exception as e:
        result_text.set(f"❌ Erro ao testar a API: {e}")

# Função acionada quando o botão de teste é clicado
def on_test_button_click():
    url = url_entry.get()
    expected_status = status_entry.get()
    expected_keys = keys_entry.get()
    
    if url:
        test_api_get(url, expected_status, expected_keys)
    else:
        messagebox.showerror("Erro", "A URL é obrigatória.")

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Testador de API")

# Criando os campos e botões
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label e Entry para a URL
ttk.Label(frame, text="URL da API:").grid(row=0, column=0, sticky=tk.W)
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, sticky=tk.W)

# Label e Entry para o Status esperado
ttk.Label(frame, text="Status esperado:").grid(row=1, column=0, sticky=tk.W)
status_entry = ttk.Entry(frame, width=10)
status_entry.grid(row=1, column=1, sticky=tk.W)
status_entry.insert(0, "200")  # Valor padrão 200

# Label e Entry para as chaves esperadas
ttk.Label(frame, text="Chaves esperadas (separadas por vírgula):").grid(row=2, column=0, sticky=tk.W)
keys_entry = ttk.Entry(frame, width=50)
keys_entry.grid(row=2, column=1, sticky=tk.W)

# Botão para executar o teste
test_button = ttk.Button(frame, text="Testar API", command=on_test_button_click)
test_button.grid(row=3, column=1, sticky=tk.W)

# Campo de texto para mostrar os resultados
result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, relief="sunken", padding=5, wraplength=400)
result_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

root.minsize(500, 200)

root.mainloop()
