class Node:
    """Класс, представляющий узел бинарного дерева."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def parse_bracket_notation(s: str) -> Node:
    """
    Парсер линейно-скобочной записи бинарного дерева.
    Поддерживает форматы вида: root (left, right)
    Если какой-то из потомков отсутствует, позиция остается пустой, например: 10 (, 14)
    """
    # Удаляем лишние пробелы для удобства парсинга
    s = s.replace(" ", "")
    if not s:
        return None

    def parse_node(string: str):
        if not string:
            return None, 0
        
        # Считываем значение текущего узла (оно может быть многозначным числом)
        i = 0
        while i < len(string) and (string[i].isalnum() or string[i] == '-'):
            i += 1
        
        node_val = string[:i]
        if not node_val:
            return None, 0
            
        root = Node(node_val)
        
        # Если далее идут скобки с поддеревьями
        if i < len(string) and string[i] == '(':
            i += 1  # Пропускаем открывающую скобку '('
            
            # Ищем левого потомка
            left_str = ""
            bracket_count = 0
            while i < len(string):
                char = string[i]
                if char == '(':
                    bracket_count += 1
                elif char == ')':
                    bracket_count -= 1
                elif char == ',' and bracket_count == 0:
                    i += 1  # Пропускаем запятую
                    break
                left_str += char
                i += 1
                
            # Ищем правого потомка
            right_str = ""
            bracket_count = 0
            while i < len(string):
                char = string[i]
                if char == '(':
                    bracket_count += 1
                elif char == ')':
                    if bracket_count == 0:
                        i += 1  # Пропускаем закрывающую скобку дерева ')'
                        break
                    bracket_count -= 1
                right_str += char
                i += 1
                
            # Рекурсивно строим левое и правое поддеревья
            root.left, _ = parse_node(left_str)
            root.right, _ = parse_node(right_str)
            
        return root, i

    root, _ = parse_node(s)
    return root


# =====================================================================
# РЕКУРСИВНЫЕ ОБХОДЫ ДЕРЕВА
# =====================================================================

def pre_order(node: Node, result: list):
    """Прямой обход: Корень -> Левое поддерево -> Правое поддерево"""
    if node is not None:
        result.append(str(node.value))
        pre_order(node.left, result)
        pre_order(node.right, result)

def in_order(node: Node, result: list):
    """Центральный (симметричный) обход: Левое поддерево -> Корень -> Правое поддерево"""
    if node is not None:
        in_order(node.left, result)
        result.append(str(node.value))
        in_order(node.right, result)

def post_order(node: Node, result: list):
    """Концевой (обратный) обход: Левое поддерево -> Правое поддерево -> Корень"""
    if node is not None:
        post_order(node.left, result)
        post_order(node.right, result)
        result.append(str(node.value))


# =====================================================================
# ДЕМОНСТРАЦИЯ И ТЕСТИРОВАНИЕ
# =====================================================================
if __name__ == "__main__":
    print("Лабораторная работа №15: Рекурсивные обходы дерева")
    print("-" * 50)
    
    # Тест 1: Дерево из верхнего примера на картинке
    tree_str_1 = "8 (3 (1, 6 (4, 7)), 10 (, 14 (13, )))"
    print(f"Входная строка 1: {tree_str_1}")
    root1 = parse_bracket_notation(tree_str_1)
    
    res_pre1, res_in1, res_post1 = [], [], []
    pre_order(root1, res_pre1)
    in_order(root1, res_in1)
    post_order(root1, res_post1)
    
    print("Результаты для дерева 1:")
    print(f"  Прямой обход:      {' '.join(res_pre1)}")
    print(f"  Центральный обход: {' '.join(res_in1)}")
    print(f"  Концевой обход:    {' '.join(res_post1)}")
    print("-" * 50)

    # Тест 2: Дерево из нижнего примера (схемы) на картинке
    # Запись схемы: 1 имеет левое поддерево у узла 2 (у которого левого нет, правый 4...), и правое у 3...
    tree_str_2 = "1 (2 (, 4 (7, 8)), 3 (5 (, 9 (11, )), 6 (10, )))"
    print(f"Входная строка 2 (из нижней схемы): {tree_str_2}")
    root2 = parse_bracket_notation(tree_str_2)
    
    res_pre2, res_in2, res_post2 = [], [], []
    pre_order(root2, res_pre2)
    in_order(root2, res_in2)
    post_order(root2, res_post2)
    
    print("Результаты для дерева 2:")
    print(f"  Прямой обход (совпадает с картинкой): {' '.join(res_pre2)}")
    print(f"  Центральный обход:                    {' '.join(res_in2)}")
    print(f"  Концевой обход:                      {' '.join(res_post2)}")
