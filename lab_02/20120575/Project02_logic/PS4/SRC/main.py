from typing import List, Tuple
import os

# ok
def extract_literals(clause):
    if isinstance(clause, list):
        clause = ' OR '.join(clause)
    literals = clause.split(" OR ")
    return literals

# Hàm này lấy hai literal, và trả về True nếu chúng bổ sung cho nhau
def is_complementary(literal_1: str, literal_2: str) -> bool:
    if literal_1[0] == "-" and literal_1[1:] == literal_2:
        return True
    elif literal_2[0] == "-" and literal_2[1:] == literal_1:
        return True
    else:
        return False

def literals_sorter(literals: List[str]) -> List[str]:
    # literals.sort(key = lambda x: x.replace('-',''))
    literals = sorted(literals, key=lambda x: (not x.startswith('-'), x.lstrip('-')))
    return literals

# Xoa trung nhau
def remove_duplicates(literals: List[str]) -> List[str]:
    return list(set(literals))

# gop hai clause
def create_clause(literals_1: List[str], literals_2: List[str]) -> List[str]:
    new_literals = literals_1 + literals_2
    sorted_literals = literals_sorter(new_literals)
    sorted_literals = remove_duplicates(sorted_literals)
    return sorted_literals

# lấy một clause và trả về true nếu mệnh đề chứa một cặp bổ sung
def is_always_true(clause: List[str]) -> bool:
    literals = extract_literals(clause)
    for lit1 in literals:
        for lit2 in literals:
            if is_complementary(lit1, lit2):
                return True
    return False

# Lấy hai danh sách và trả về True nếu tất cả các mệnh đề trong danh sách 1 xuất hiện trong danh sách 2
def is_subset(clauses1: List[List[str]], clauses2: List[List[str]]) -> bool:
    for clause in clauses1:
        if clause not in clauses2:
            return False
    return True
# lấy literal và trả về phủ định
def negate_literal(literal: str) -> str:
    if literal[0] == "-":
        return literal[1:]
    else:
        return f"-{literal}"

# Dọc file input
def read_input(input_file: str) -> Tuple[str, List[str]]:
    with open(input_file, 'r') as f:
        alpha = f.readline().strip()
        num_clauses = int(f.readline().strip())
        clauses = [f.readline().strip() for _ in range(num_clauses)]
    return alpha, clauses

#  ghi ra output
def write_output(output_file: str, generated_clauses: List[List[str]], entails_alpha: bool):
    with open(output_file, 'w') as f:
        for i, clauses in enumerate(generated_clauses):
            f.write(f"{len(clauses)}\n")
            for clause in clauses:
                for i,clause1 in enumerate(clause):
                    f.write(f"{clause1}")
                    if i != len(clause) - 1 and clause != "{}":
                        f.write(f" OR ")
                f.write("\n")
            f.write("\n")
        f.write("{}\n".format("YES" if entails_alpha else "NO"))
# Dung
def pl_resolve(ci: List[str], cj: List[str]) -> List[str]:
    resolvents = []
    literals1 = ci[:]
    literals2 =  cj[:]
    note = 0
    for lit1 in literals1:
        for lit2 in literals2:
            if is_complementary(lit1,lit2):
                note = 1
                literals1.remove(lit1)
                literals2.remove(lit2)
                break
        if note == 1: 
            break
    if note == 1:
        if (len(literals1) == 0 and len(literals2) == 0):
            resolvents.append("{}")
            return resolvents
        literals1 = literals_sorter(literals1)
        literals2 = literals_sorter(literals2)
        new_clause = create_clause(literals1, literals2)
        resolvents.append(new_clause)
        return resolvents
    resolvents.append(literals1)
    del literals1
    resolvents.append(literals2)
    del literals2
    return resolvents
        
def pl_resolution(kb: List[str], alpha: str) -> Tuple[List[str], bool]:
    clauses = [extract_literals(x) for x in kb]
    clauses.append([negate_literal(alpha)])
    new_clauses = []
    generated_clauses = []
    while True:
        record =[]
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            for resolvent in resolvents:
                if not is_always_true(resolvent):
                    if resolvent not in new_clauses:
                        new_clauses.append(resolvent)

        if is_subset(new_clauses, clauses):
            generated_clauses.append(record) 
            return generated_clauses, False
        
        for clause in new_clauses:
            if clause not in clauses:
                if not is_always_true (clause):
                    clauses.append(clause)
                    record.append(clause)      
                        
        generated_clauses.append(record)
        
        if "{}" in record:
            return generated_clauses, True
        
# hàm main chương trình
def main():
    path = "Input"
    temp = os.listdir(path)
    for i in range(len(temp)):
        alpha, kb = read_input(f"Input/input{i+1}.txt")
        generated_clauses, entails_alpha = pl_resolution(kb, alpha)
        write_output(f"Output/output{i+1}.txt", generated_clauses, entails_alpha)
        del kb, generated_clauses

if __name__ == "__main__":
    main()