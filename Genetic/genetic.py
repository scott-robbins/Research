import random


def generate_parent(length, gene_set):
    genes = []
    while len(genes) < length:
        sample_size = min(length - len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sample_size))
    return ''.join(genes)


def mutate(parent, gene_set):
    index = random.randrange(0, len(parent))
    children_genes = list(parent)
    new_gene, alt = random.sample(gene_set, 2)
    children_genes[index] = alt if new_gene == children_genes[index] else new_gene
    return ''.join(children_genes)


def get_best(get_fitness, target_len, optimal_fit, gene_set, display):
    random.seed()
    best_parent = generate_parent(target_len, gene_set)
    best_fit = get_fitness(best_parent)
    display(best_parent)
    if best_fit >= optimal_fit:
        return best_parent

    while True:
        child = mutate(best_parent, gene_set)
        child_fit = get_fitness(child)
        if best_fit >= child_fit:
            continue
        display(child)
        if child_fit >= optimal_fit:
            return child
        best_fit = child_fit
        best_parent = child
