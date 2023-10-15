import numpy as np

def evaluate_coeff(p_coeff, x):
    a = p_coeff[0]
    b = p_coeff[1]

    return a + b * x


def get_intersection_point(coeff_1, coeff_2):
    a = coeff_1[0]
    b = coeff_1[1]
    c = coeff_2[0]
    d = coeff_2[1]
    if b != d:
        intersection_point = (c - a) / (b - d)

        return intersection_point, evaluate_coeff(coeff_1, intersection_point)
    return None

def check_saddle(A):
    m,n = A.shape
    p = np.zeros(m)
    q = np.zeros(n)

    row_mins  = np.amin(A, axis=1)
    col_maxes = np.amax(A, axis=0)

    v, p_index, q_index = np.intersect1d(row_mins, col_maxes, return_indices=True)

    if v.size > 0:
        p[p_index[0]] = 1
        q[q_index[0]] = 1
        return p, q, v[0]
    
    return None

def solve_2x2(A):
    a = A[0,0]
    b = A[0,1]
    c = A[1,1]
    d = A[1,0]

    p = (c - d) / (a - b + c - d)
    q = (c - b) / (a - b + c - d)
    v = a * p + d * (1 - p)

    return np.array([p, 1-p]), np.array([q, 1-q]), v

def solve_2xn(A):
    n = A.shape[1]
    p_coeffs = np.zeros((2,n))
    
    # Extract coefficients from A matrix
    for i in range(n):
        p_coeffs[0,i] = A[1,i]
        p_coeffs[1,i] = A[0,i] - A[1,i]
    
    # Find line intersections
    intersections = []
    for i in range(n-1):
        for j in range(i+1, n):
            a = p_coeffs[0,i]
            b = p_coeffs[1,i]
            c = p_coeffs[0,j]
            d = p_coeffs[1,j]
            out = get_intersection_point(p_coeffs[:,i], p_coeffs[:,j])
            if out:
                intersect_point = out[0]
                if intersect_point > 0 and intersect_point < 1:
                    intersections.append(intersect_point)
    
    # Order intersections
    intersections = sorted(intersections)
    
    # Find minimum line on each side of intersection
    test_vals = []
    epsilon = .001
    for i in intersections:
        test_vals.append(i-epsilon)
        test_vals.append(i+epsilon)

    function_vals = np.zeros((n, len(test_vals)))
    for v in range(len(test_vals)):
        for p in range(n):
            function_vals[p, v] = evaluate_coeff(p_coeffs[:,p], test_vals[v])

    min_functions = np.argmin(function_vals, axis=0)
    unique_min_functions = []
    
    # Unique functions are used since intersection points may be above minimum line
    for i in range(len(min_functions)):
        if i == 0 or min_functions[i-1] != min_functions[i]:
            unique_min_functions.append(min_functions[i])
    
    # Get P and v for intersections and take the max
    point_values = np.zeros((2,len(unique_min_functions)-1))

    for i in range(len(unique_min_functions)-1):
        point_values[0,i], point_values[1,i] = get_intersection_point(p_coeffs[:, unique_min_functions[i]], p_coeffs[:, unique_min_functions[i+1]])

    max_intersection = np.argmax(point_values[1,:])
    
    # Find columns with max intersection
    used_columns = unique_min_functions[max_intersection:max_intersection+2]

    # Populate p, q, and v
    p, q_prime, v = solve_2x2(A[:,used_columns])
    
    q = np.zeros(n)
    q[used_columns] = q_prime

    return p, q, v

def solve_mx2(A):
    m = A.shape[0]
    p_coeffs = np.zeros((2,m))
    
    # Extract coefficients from A matrix
    for i in range(m):
        p_coeffs[0,i] = A[i,1]
        p_coeffs[1,i] = A[i,0] - A[i,1]
    
    # Find line intersections
    intersections = []
    for i in range(m-1):
        for j in range(i+1, m):
            a = p_coeffs[0,i]
            b = p_coeffs[1,i]
            c = p_coeffs[0,j]
            d = p_coeffs[1,j]
            out = get_intersection_point(p_coeffs[:,i], p_coeffs[:,j])
            if out:
                intersect_point = out[0]
                if intersect_point > 0 and intersect_point < 1:
                    intersections.append(intersect_point)
    
    # Order intersections
    intersections = sorted(intersections)
    
    # Find maximum line on each side of intersection
    test_vals = []
    epsilon = .001
    for i in intersections:
        test_vals.append(i-epsilon)
        test_vals.append(i+epsilon)

    function_vals = np.zeros((m, len(test_vals)))
    for v in range(len(test_vals)):
        for p in range(m):
            function_vals[p, v] = evaluate_coeff(p_coeffs[:,p], test_vals[v])

    max_functions = np.argmax(function_vals, axis=0)
    unique_max_functions = []

    # Unique functions are used since intersection points may be below maximum line
    for i in range(len(max_functions)):
        if i == 0 or max_functions[i-1] != max_functions[i]:
            unique_max_functions.append(max_functions[i])
    
    # Get P and v for intersections and take the min 
    point_values = np.zeros((2,len(unique_max_functions)-1))

    for i in range(len(unique_max_functions)-1):
        point_values[0,i], point_values[1,i] = get_intersection_point(p_coeffs[:, unique_max_functions[i]], p_coeffs[:, unique_max_functions[i+1]])

    min_intersection = np.argmin(point_values[1,:])
    
    # Find columns with max intersection
    used_rows = unique_max_functions[min_intersection:min_intersection+2]

    # Populate p, q, and v
    p_prime, q, v = solve_2x2(A[used_rows,:])
    
    p = np.zeros(m)
    p[used_rows] = p_prime

    return p, q, v

def solve_poi(A):
    # Get size
    n = A.shape[1]
    
    # Form POI matrices
    A_prime = np.concatenate((A, -1*np.ones((n,1))), axis=1)
    bottom = np.concatenate((np.ones((1,n)), np.zeros((1,1))), axis=1)
    A_prime = np.concatenate((A_prime,bottom), axis=0)
    b = np.concatenate((np.zeros((n,1)), np.ones((1,1))), axis=0)
    
    # Solve system of equations
    out = np.linalg.solve(A_prime,b)
    
    # Extract p and q and v
    p = out[0:n].flatten()
    v = out[n]
    q = np.linalg.solve(np.transpose(A), v * np.ones((n,1))).flatten()

    return p,q,v

def solve_pivot(A):
    # Get size
    m,n = A.shape
    
    # Make sure v does not equal 0
    added_v = np.min(A)
    if added_v < 0:
        added_v *= -1
        A = A + np.ones((m,n))*added_v
    else:
        added_v = 0
    
    # Form tableau
    tableau_top = np.concatenate((A, np.ones((m,1))), axis=1)
    tableau_bottom = np.concatenate((-np.ones((1,n)), np.zeros((1,1))), axis=1)
    tableau = np.concatenate((tableau_top, tableau_bottom), axis=0)
    
    # Trackers store pivots
    row_tracker = np.ones(n)
    col_tracker = np.ones(m)
    
    # Pivot method
    while np.any(tableau[m,:-1] < 0):
        used_row = -1
        used_col = -1
        for i in range(n):
            if tableau[m, i] < 0:
                ratios = np.zeros(m)
                ratios.fill(np.inf)
                for j in range(m):
                    if tableau[j,i] > 0:
                        ratios[j] = tableau[j,n] / tableau[j,i]
                sorted_indices = np.argsort(ratios)

                found_valid = False
                used_index = 0

                while used_index < len(sorted_indices) and not found_valid:
                    if tableau[sorted_indices[used_index],i] > 0:
                        found_valid = True
                        break;
                    else:
                        used_index += 1

                if found_valid:
                    used_row = sorted_indices[used_index]
                    used_col = i
                    break;

        assert used_row != -1 and used_col != -1

        pivot = tableau[used_row, used_col]

        new_tableau = tableau.copy()

        for i in range(m+1):
            for j in range(n+1):
                if i != used_row and j != used_col:
                    new_tableau[i,j] -= tableau[used_row,j] * tableau[i,used_col] / pivot
                elif i != used_row:
                    new_tableau[i,j] /= -pivot
                elif j != used_col:
                    new_tableau[i,j] /= pivot
                else:
                    new_tableau[i,j] = 1/pivot
        tableau = new_tableau.copy() 
        row_tracker[used_row] *= -1
        col_tracker[used_col] *= -1
    

    inv_v_prime = tableau[m,n]
    v = 1/inv_v_prime - added_v
    
    p = np.zeros(m)
    q = np.zeros(n)
    for i in range(m):
        if row_tracker[i] < 0:
            p[i] = tableau[m, i] / inv_v_prime

    for j in range(n):
        if col_tracker[j] < 0:
            q[j] = tableau[j,n] / inv_v_prime

    return p, q, v



def solve_game(A):
    # i) Saddle Point
    out = check_saddle(A)
    if out:
        return out
    # ii) 2x2 case
    if A.shape == (2,2):
        return solve_2x2(A)
    
    # iii) 2xn case
    if A.shape[0] == 2:
        return solve_2xn(A)
    
    # iii) mx2 case
    if A.shape[1] == 2:
        return solve_mx2(A)

    # iv) Principle of indifference
    if A.shape[0] == A.shape[1]:
        if np.linalg.det(A) != 0:
            out = solve_poi(A)

            if not(np.any(out[0] <= 0) or np.any(out[1] <= 0)):
                return out

    # v) Invariance
    #if check_invariance(A):
    #    return solve_invariant(A)

    # vi) nxn formula (how is this different from indifference?

    # vii) Linear Programming
    return solve_pivot(A)

if __name__ == "__main__":
    A = np.array([[4,1,8],[2,3,1],[0,4,3]])

    print(solve_game(A))
