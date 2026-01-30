import sys

def parse_input(filename):
   #parse the input file and return the number of hospitals and students, and their preferences
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        raise ValueError("Input file is empty")
    n = int(lines[0])
    if len(lines) != 2 * n + 1:
        raise ValueError(f"Expected {2 * n + 1} lines, got {len(lines)}")
    hospital_prefs = []
    student_prefs = []
    for i in range(1, n + 1):
        prefs = [int(x) for x in lines[i].split()]
        hospital_prefs.append(prefs)
    for i in range(n + 1, 2 * n + 1):
        prefs = [int(x) for x in lines[i].split()]
        student_prefs.append(prefs)
    return n, hospital_prefs, student_prefs

def gale_shapley(hospital_prefs, student_prefs, n):
    matches = {}  
    proposal_index = [0] * n  
    # while some hospital is free and hasn't been matched/assigned to every applicant
    while True:
        free_hospital = None
        for h in range(n):  
            is_matched = any(matches.get(s) == h + 1 for s in matches)
            has_more_applicants = proposal_index[h] < n
            if not is_matched and has_more_applicants:
                free_hospital = h
                break
        # If no free hospital found it terminates
        if free_hospital is None:
            break
        h = free_hospital 
        student_index = proposal_index[h]
        a = hospital_prefs[h][student_index]  
        proposal_index[h] += 1  
        if a not in matches:
            matches[a] = h + 1  
        #trade up
        else: 
            current_hospital = matches[a] 
            h_num = h + 1  
            student_pref_list = student_prefs[a - 1]  
            h_rank = student_pref_list.index(h_num)
            current_rank = student_pref_list.index(current_hospital)
            if h_rank < current_rank:  #
                matches[a] = h_num
    #return stable matches
    result = {}
    for student, hospital in matches.items():
        result[hospital] = student
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python matcher.py <input_file>", file=sys.stderr)
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        n, hospital_prefs, student_prefs = parse_input(input_file)
        # Validate equal number of hospitals and students
        if len(hospital_prefs) != n or len(student_prefs) != n:
            print("ERROR: Number of hospitals and students must be equal", file=sys.stderr)
            sys.exit(1)
        # Run Gale-Shapley algorithm
        matching = gale_shapley(hospital_prefs, student_prefs, n)
        for hospital in sorted(matching.keys()):
            print(f"{hospital} {matching[hospital]}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
