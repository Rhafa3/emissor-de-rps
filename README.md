# Gerador de RPS - São Paulo 📄

Aplicativo desktop para geração de Recibos Provisórios de Serviços (RPS) conforme especificações da Prefeitura de São Paulo.


## Funcionalidades ⚙️
- Cadastro completo de dados do prestador e tomador
- Validação automática de CNPJ/CPF
- Formatação de valores monetários
- Geração de PDF profissional com:
  - Layout em colunas
  - Tabela de serviços detalhada
  - Cálculos automáticos
  - Carimbo de data/hora
- Sistema de limpeza de dados

## Pré-requisitos 📦
- Python 3.8+
- Sistema operacional Windows/Linux/Mac

## Instalação 🔧
```bash
# Clonar repositório
git clone https://github.com/Rhafa3/emissor-rps-sp.git

# Acessar diretório
cd emissor-rps-sp.git

# Instalar dependências
pip install -r requirements.txt


Como Usar 🖱️
Preencha todas as abas sequencialmente

Validações automáticas irão:

Formatar valores monetários

Verificar documentos

Alertar sobre campos obrigatórios

Clique em "Gerar PDF" para:

Escolher local de salvamento

Receber confirmação de sucesso

Use "Limpar" para novo recibo

Estrutura do PDF Gerado 📑
Exemplo de PDF
(Exemplo do documento gerado com layout profissional)

Tecnologias Utilizadas 💻
Interface Gráfica: Tkinter

Geração de PDF: FPDF

Validações: Regex

Gerenciamento de Data: tkcalendar
