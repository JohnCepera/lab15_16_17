import re

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def parse_tree(s: str):
    """Парсер линейно-скобочной записи дерева в структуру из объектов Node."""
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

def iterative_preorder(root):
    """Нерекурсивный прямой обход дерева с использованием стека."""
    if not root:
        return []
        
    stack = [root]
    result = []
    
    while stack:
        node = stack.pop()
        result.append(node.value)
        
        # Сначала правого, чтобы левый оказался наверху стека
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
            
    return result

if __name__ == "__main__":
    input_str = "8 (3 (1, 6 (4,7)), 10 ( , 14(13,)))"
    print(f"Входная строка дерева: {input_str}")
    
    tree_root = parse_tree(input_str)
    traversal_order = iterative_preorder(tree_root)
    
    output_str = " ".join(traversal_order)
    print(f"Строка прямого обхода: {output_str}")
