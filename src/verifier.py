import sys

"""
(a)  Checks validity: each hospital and each student is matched to exactly one partner, 
with no duplicates. 

And 

(b) Checks stability: confirms there is no blocking pair.

""" 

def parse_input(filename):
    # read input file and get preferences
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        raise ValueError("Input file is empty")
    n = int(lines[0])

    if len(lines) != 2 * n + 1:
        raise ValueError(f"Expected {2 * n + 1} lines, got {len(lines)}")
        
    h_prefs = []
    s_prefs = []

    for i in range(1, n + 1):
        prefs = [int(x) for x in lines[i].split()]
        h_prefs.append(prefs)
    for i in range(n + 1, 2 * n + 1):
        prefs = [int(x) for x in lines[i].split()]
        s_prefs.append(prefs)
    return n, h_prefs, s_prefs

def parse_output(filename):
    # read the matching from output file
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    h_to_s = {}
    s_to_h = {}
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid output format: expected 'hospital student', got '{line}'")
        h = int(parts[0])
        s = int(parts[1])
        h_to_s[h] = s
        s_to_h[s] = h
    return h_to_s, s_to_h

def check_validity(n, h_to_s, s_to_h):
    # make sure every hospital has a match
    for i in range(1, n + 1):
        if i not in h_to_s:
            return False, f"Hospital {i} is not matched"
    
    # make sure every student has a match
    for i in range(1, n + 1):
        if i not in s_to_h:
            return False, f"Student {i} is not matched"
    
    # check for duplicate students
    seen_students = []
    for h, s in h_to_s.items():
        if s in seen_students:
            return False, f"Student {s} is matched to multiple hospitals"
        seen_students.append(s)
    
    # check consistency
    for h, s in h_to_s.items():
        if s_to_h[s] != h:
            return False, f"Inconsistent matching: Hospital {h} matched to student {s}, but student {s} matched to hospital {s_to_h[s]}"
    
    # should have n matches
    if len(h_to_s) != n or len(s_to_h) != n:
        return False, f"Expected {n} matches, got {len(h_to_s)}"
    
    return True, ""

def check_stability(n, h_prefs, s_prefs, h_to_s, s_to_h):
    # look for blocking pairs
    for hospital in range(1, n + 1):
        current_s = h_to_s[hospital]
        hospital_pref_list = h_prefs[hospital - 1]
        
        # where is current student in hospital's list
        curr_rank = hospital_pref_list.index(current_s)
        
        # check students hospital likes more
        for i in range(curr_rank):
            better_student = hospital_pref_list[i]
            student_curr_h = s_to_h[better_student]
            student_pref_list = s_prefs[better_student - 1]
            
            # check if student likes this hospital more
            student_curr_rank = student_pref_list.index(student_curr_h)
            hospital_rank = student_pref_list.index(hospital)
            
            if hospital_rank < student_curr_rank:
                return False, f"Blocking pair: Hospital {hospital} and Student {better_student} prefer each other over their current matches"
    
    return True, ""

def main():
    if len(sys.argv) != 3:
        print("Usage: python verifier.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        n, h_prefs, s_prefs = parse_input(input_file)
        h_to_s, s_to_h = parse_output(output_file)
        
        valid, msg = check_validity(n, h_to_s, s_to_h)
        if not valid:
            print(f"INVALID: {msg}", file=sys.stderr)
            sys.exit(1)
        
        stable, msg = check_stability(n, h_prefs, s_prefs, h_to_s, s_to_h)
        if not stable:
            print(f"UNSTABLE: {msg}", file=sys.stderr)
            sys.exit(1)
        
        print("VALID and STABLE")
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
