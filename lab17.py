import re

class Node:
    def __init__(self, value):
        self.value = int(value)  # Для БДП преобразуем значения в числа
        self.left = None
        self.right = None

# ==========================================
# 1. ПАРСЕР ЛИНЕЙНО-СКОБОЧНОЙ ЗАПИСИ
# ==========================================
def parse_tree(s: str):
    s = s.replace(" ", "")
    if not s:
        return None
        
    root_match = re.match(r'^([^(),]+)', s)
    if not root_match:
        return None
        
    root_val = root_match.group(1)
    root = Node(root_val)
    
    remainder = s[len(root_val):]
    if remainder.startswith('(') and remainder.endswith(')'):
        content = remainder[1:-1]
        
        balance = 0
        comma_idx = -1
        for i, char in enumerate(content):
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            elif char == ',' and balance == 0:
                comma_idx = i
                break
                
        if comma_idx != -1:
            left_str = content[:comma_idx]
            right_str = content[comma_idx+1:]
            root.left = parse_tree(left_str)
            root.right = parse_tree(right_str)
        else:
            root.left = parse_tree(content)
            
    return root

# ==========================================
# 2. ОПЕРАЦИИ НАД БДП (Поиск, Добавление, Удаление)
# ==========================================
def search_bst(root, key):
    """Поиск ключа в дереве. Возвращает True, если найден, иначе False."""
    if root is None:
        return False
    if root.value == key:
        return True
    if key < root.value:
        return search_bst(root.left, key)
    return search_bst(root.right, key)

def insert_bst(root, key):
    """Вставка нового ключа в БДП."""
    if root is None:
        return Node(key)
    
    if key < root.value:
        root.left = insert_bst(root.left, key)
    elif key > root.value:
        root.right = insert_bst(root.right, key)
    else:
        print(f"Узел со значением {key} уже существует в дереве.")
    return root

def _min_value_node(node):
    """Вспомогательная функция для поиска минимального узла в правом поддереве."""
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete_bst(root, key):
    """Удаление ключа из БДП."""
    if root is None:
        print(f"Узел со значением {key} не найден.")
        return None

    if key < root.value:
        root.left = delete_bst(root.left, key)
    elif key > root.value:
        root.right = delete_bst(root.right, key)
    else:
        # Узел с одним потомком или без потомков
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Узел с двумя потомками: получаем инфиксного преемника (наименьший в правом поддереве)
        temp = _min_value_node(root.right)
        root.value = temp.value
        # Удаляем преемника
        root.right = delete_bst(root.right, temp.value)
        
    return root

# ==========================================
# 3. ФОРМАТЫ ВЫВОДА ДЕРЕВА
# ==========================================
def tree_to_string(root):
    """Преобразование дерева обратно в линейно-скобочную запись."""
    if root is None:
        return ""
    if root.left is None and root.right is None:
        return str(root.value)
    
    left_str = tree_to_string(root.left)
    right_str = tree_to_string(root.right)
    
    if right_str:
        return f"{root.value}({left_str},{right_str})"
    else:
        return f"{root.value}({left_str})"

def print_tree_graphical(node, prefix="", is_left=True):
    """Псевдографический вывод структуры дерева на экран."""
    if node is not None:
        print(prefix + ("├── " if is_left else "└── ") + str(node.value))
        new_prefix = prefix + ("│   " if is_left else "    ")
        if node.left or node.right:
            print_tree_graphical(node.left, new_prefix, True)
            print_tree_graphical(node.right, new_prefix, False)

# ==========================================
# 4. ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ (МЕНЮ)
# ==========================================
def main():
    print("Лабораторная работа №17: Операции над БДП")
    input_str = input("Введите дерево в линейно-скобочной записи (например, 8(3(1,6),10)): ")
    
    root = parse_tree(input_str)
    if not root:
        print("Ошибка парсинга дерева. Создано пустое дерево.")
    
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Поиск вершины")
        print("2. Добавление вершины")
        print("3. Удаление вершины")
        print("4. Выйти из программы")
        
        choice = input("Выберите действие (1-4): ").strip()
        
        if choice == '1':
            try:
                val = int(input("Введите значение для поиска: "))
                found = search_bst(root, val)
                if found:
                    print(f"Результат: Узел {val} НАЙДЕН в дереве.")
                else:
                    print(f"Результат: Узел {val} НЕ НАЙДЕН.")
            except ValueError:
                print("Пожалуйста, введите корректное целое число.")
                
        elif choice == '2':
            try:
                val = int(input("Введите значение для добавления: "))
                root = insert_bst(root, val)
                print(f"Узел {val} успешно добавлен (если не существовал ранее).")
            except ValueError:
                print("Пожалуйста, введите корректное целое число.")
                
        elif choice == '3':
            try:
                val = int(input("Введите значение для удаления: "))
                if search_bst(root, val):
                    root = delete_bst(root, val)
                    print(f"Узел {val} успешно удален.")
                else:
                    print(f"Узел {val} отсутствует в дереве.")
            except ValueError:
                print("Пожалуйста, введите корректное целое число.")
                
        elif choice == '4':
            print("\nВыход из меню.")
            print("\n=== ИТОГОВОЕ ДЕРЕВО ===")
            print("Линейно-скобочная запись:")
            print(tree_to_string(root) if root else "Дерево пустое")
            print("\nГрафическое представление дерева:")
            if root:
                print_tree_graphical(root, is_left=False)
            else:
                print("[Пустое дерево]")
            print("\nПрограмма завершена.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
