# Деловой Тиндер

## Разработка

* Запустить локально
    * Create venv and install deps
      ```
      python3 -m venv .venv
      pip3 install -r ./requirements.txt
      ```
    * Run
      ```
      make run
      ```
* [Установить pre-commit](https://pre-commit.com/)
    * Install pre-commit
      ```
      pip install pre-commit
      ```
    * Init
      ```
      pre-commit install
      ```

  * Работа с зависимостями:
      * Все зависимости описываются в `requirements.in`, из них будет автоматически сгенерирован `requirements.txt` (при
        помощи pre-commit).
      * Аналогичный файл `requirements-lint.in` для линтеров
      * Установить lint зависимости:
        ```bash
        pip install -r ./requirements-lint.txt
        ```
      * Собрать зависимости вручную:
        1) Ставим сборщик
        ```bash
        python -m pip install pip-tools
        ```
        2) Собираем
        ```bash
        pip-compile -o requirements.txt
        ```
