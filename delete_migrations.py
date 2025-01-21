import os


def delete_migrations(project_root):
    for root, dirs, files in os.walk(project_root):
        if "migrations" in dirs:
            migration_dir = os.path.join(root, "migrations")
            for file in os.listdir(migration_dir):
                if file != "__init__.py" and file.endswith(".py"):
                    os.remove(os.path.join(migration_dir, file))
                    print(f"Удален файл: {os.path.join(migration_dir, file)}")


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    delete_migrations(project_root)
    print("Удаление миграций завершено.")
