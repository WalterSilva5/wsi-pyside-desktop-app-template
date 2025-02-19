# PySide6 App Template (Whitelabel)

Este repositório é um **template whitelabel** para aplicações desktop desenvolvidas com **PySide6**. Ele oferece uma estrutura escalável e modular, permitindo a criação de projetos reutilizáveis e facilmente adaptáveis.

## Recursos
✅ Estrutura modular com **MVC**
✅ **Navegação entre telas** via `QStackedWidget`
✅ **Componentes reutilizáveis** (header, sidebar, etc.)
✅ **Fácil expansão** para novos módulos e funcionalidades

---

## Estrutura do Projeto
```
meu_projeto/src/
│── main.py              # Ponto de entrada do app
│── views/
│   │── home.py          # Tela principal
│   │── settings.py      # Tela de configurações
|   │── main_window.py   # Gerencia as telas
|   |
│   └── components/
│       ├── sidebar.py   # Barra lateral comum
│       ├── header.py    # Cabeçalho comum
│── controllers/
│   ├── home_controller.py
│   └── settings_controller.py
└── models/
    ├── config_model.py
    └── user_model.py
```

---

## Instalação e Execução
### 1. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Execute o aplicativo:
```bash
python main.py
```

---

## Como Adicionar uma Nova Tela?
1. Crie um novo arquivo em `views/`, por exemplo: `views/about.py`.
2. Defina uma classe que herda `QWidget`, como `AboutPage(QWidget)`.
3. Adicione a nova tela ao `main_window.py` no `QStackedWidget`.
4. Configure a navegação na sidebar ou em botões das telas existentes.

---

## Como Personalizar?
- **Alterar estilos**: Modifique as folhas de estilo dentro das `views/components/`.
- **Adicionar novas funcionalidades**: Crie arquivos dentro de `controllers/` e `models/`.
- **Reaproveitar componentes**: Utilize os widgets dentro de `views/components/`.

---

## Licença
Este projeto é distribuído sob a licença **MIT**, permitindo uso, modificação e distribuição livremente.

---

💡 **Dúvidas ou Sugestões?** Abra uma issue ou contribua com um pull request! 🚀

