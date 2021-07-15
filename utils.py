def list2mat(adj_list):
    """
    converts adjacency list of worlds to adjacency matrix of worlds
    """
    n = len(adj_list)
    mat = [[0 for i in range(n)] for i in range(n)]
    for i in adj_list.keys():
        for j in adj_list[i]:
            mat[i][j] = 1
    return mat


def mat2list(mat):
    """
    converts adjacency matrix of worlds to adjacency list of worlds
    """
    n = mat.shape[0]
    adj = {}
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                if i not in adj.keys():
                    adj[i] = []
                adj[i].append(j)
    return adj


def get_sub(x):
    """
    function to convert to subscript
    """
	normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
	sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
	res = x.maketrans(''.join(normal), ''.join(sub_s))
	return x.translate(res)
