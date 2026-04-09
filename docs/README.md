# Documentação — PySide6 Desktop Template

Bem-vindo à documentação do template. Todos os documentos aqui estão em **português brasileiro**. Se você é novo no projeto, comece pelo [Início Rápido](01-inicio-rapido.md).

## Índice

### Começando
1. [Início Rápido](01-inicio-rapido.md) — instalação, rodar a aplicação, primeiros passos
2. [Arquitetura](02-arquitetura.md) — visão geral das camadas e dos padrões usados
3. [Estrutura do Projeto](03-estrutura-do-projeto.md) — árvore de pastas comentada

### Criando coisas novas
4. [Criando uma Feature](04-criando-uma-feature.md) — **passo a passo** para adicionar uma tela nova
5. [Criando um Componente](05-criando-um-componente.md) — como criar um componente reutilizável
6. [Biblioteca de Componentes](06-biblioteca-de-componentes.md) — catálogo com todos os componentes disponíveis

### Serviços e infraestrutura
7. [Serviços](07-servicos.md) — Config, Logger, Navigation, Theme, Storage
8. [Navegação](08-navegacao.md) — `PageId`, rotas, histórico, guards, parâmetros
9. [Tema e Estilos](09-tema-e-estilos.md) — light/dark, QSS, `ThemeService`
10. [Layout Responsivo](10-layout-responsivo.md) — Grid de 12 colunas e FlowLayout
11. [Modelos e Repositórios](11-modelos-e-repositorios.md) — `BaseModel`, Repository, persistência
12. [Event Bus](12-event-bus.md) — sinais globais para comunicação desacoplada

### Qualidade e distribuição
13. [Testes](13-testes.md) — pytest, pytest-qt, fixtures, exemplos
14. [Build e Empacotamento](14-build-e-empacotamento.md) — PyInstaller para gerar `.exe`

---

## Convenções da documentação

- **Nomes de arquivos** aparecem como `src/core/application.py:42` (path + linha) para você poder clicar e ir direto ao código.
- **Blocos de código** em Python assumem Python 3.10+.
- **Termos técnicos** ficam em inglês (ex.: "singleton", "repository") porque é como aparecem no código.
- **Comandos** são apresentados para `uv` (recomendado) e `pip` quando diferentes.

## Filosofia do template

Este template foi construído para que **criar uma feature nova seja copiar uma pasta e editar três arquivos**. Se você precisar fazer muito mais que isso, abra uma issue — pode ser sinal de que a estrutura está no caminho errado.

Os princípios que o norteiam:

- **Feature-based**: cada tela é uma pasta em `src/features/`, com tudo o que ela precisa próximo (page, controller, models, repositories). Nada de `src/views/X.py` + `src/controllers/X.py` + `src/models/X.py` espalhados por três diretórios.
- **Componentes são burros**: componentes em `src/components/` não conhecem features. A sidebar recebe os itens de menu via `set_items(...)`.
- **Core é mínimo**: `src/core/` só contém infraestrutura (DI container, event bus, types base). Nunca importe nada de `src/features/` dentro de `src/core/`.
- **Services são singletons resolvidos via container**: nunca instancie `ConfigService()` — sempre `container.resolve(ConfigService)`.
