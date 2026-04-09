"""
Módulo de features.

Cada feature é uma pasta auto-contida que agrupa tudo relacionado
a uma área funcional da aplicação: página (view), controlador
(business logic) e, quando necessário, modelos e repositórios
específicos daquela feature.

Estrutura de uma feature:

    src/features/<minha_feature>/
        __init__.py
        page.py          # Widget principal (herda de BasePage)
        controller.py    # Regras de negócio (herda de BaseController)
        models/          # Opcional — modelos específicos da feature
        repositories/    # Opcional — repositórios específicos

Para adicionar uma feature nova, consulte `docs/04-criando-uma-feature.md`.
"""
