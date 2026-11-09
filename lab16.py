class Node
    def __init__(self, value)
        self.value = value
        self.left = None
        self.right = None

def parse_tree(s str)
    Парсер линейно-скобочной записи дерева в структуру из объектов Node.
    s = s.replace( , )  # Удаляем лишние пробелы для удобства
    if not s
        return None
        
    import re
    # Находим значение корневого узла
    root_match = re.match(r'^([^(),]+)', s)
    if not root_match
        return None
        
    root_val = root_match.group(1)
    root = Node(root_val)
    
    # Отрезаем значение корня, оставляя только внутренности скобок
    remainder = s[len(root_val)]
    if remainder.startswith('(') and remainder.endswith(')')
        content = remainder[1-1]
        
        # Ищем разделяющую запятую верхнего уровня (между левым и правым поддеревом)
        balance = 0
        comma_idx = -1
        for i, char in enumerate(content)
            if char == '('
                balance += 1
            elif char == ')'
                balance -= 1
            elif char == ',' and balance == 0
                comma_idx = i
                break
                
        if comma_idx != -1
            left_str = content[comma_idx]
            right_str = content[comma_idx+1]
            root.left = parse_tree(left_str)
            root.right = parse_tree(right_str)
        else
            # Если запятой нет, то есть только один (левый) потомок
            root.left = parse_tree(content)
            
    return root

def iterative_preorder(root)
    Нерекурсивный прямой обход дерева с использованием стека.
    if not root
        return []
        
    stack = [root]
    result = []
    
    while stack
        node = stack.pop()
        result.append(node.value)
        
        # Сначала кладем в стек правого потомка, чтобы левый обработался раньше
        if node.right
            stack.append(node.right)
        if node.left
            stack.append(node.left)
            
    return result

# --- Пример работы программы ---
if __name__ == __main__
    # Пример строки из первого рисунка в задании
    input_str = 8 (3 (1, 6 (4,7)), 10 ( , 14(13,)))
    
    print(fВходная строка дерева {input_str})
    
    # Построение дерева
    tree_root = parse_tree(input_str)
    
    # Выполнение нерекурсивного прямого обхода
    traversal_order = iterative_preorder(tree_root)
    
    # Вывод результата в виде строки обхода
    output_str =  .join(traversal_order)
    print(fСтрока прямого обхода {output_str})
