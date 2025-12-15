from dempster_shafer import DempsterShafer

def print_detailed_results(metrics, conflict_val):
    print("-" * 90)
    print(f"Conflict Global (K): {conflict_val:.4f}  (Sursele se contrazic in proportie de {conflict_val*100:.1f}%)")
    print("-" * 90)
    print(f"{'IPOTEZA':<30} | {'MASA (m)':<10} | {'BEL (Sigur)':<10} | {'PL (Posibil)':<10} | {'INCERTITUDINE':<13}")
    print("-" * 90)
    
    for subset, vals in metrics.items():
        subset_str = "{" + ", ".join(list(subset)) + "}"
        print(f"{subset_str:<30} | {vals['mass']:.4f}     | {vals['bel']:.4f}     | {vals['pl']:.4f}     | {vals['uncertainty']:.4f}")
    print("-" * 90)

def caz_medical_complex():
    ds = DempsterShafer()
    print("\n\n" + "="*50)
    print("=== STUDIU DE CAZ 1: DIAGNOSTIC MEDICAL ===")
    print("="*50)
    
    theta = frozenset({"Raceala", "Gripa", "Meningita"})

    m1 = {frozenset({"Raceala", "Gripa"}): 0.6, theta: 0.4}
    
    m2 = {frozenset({"Meningita"}): 0.7, theta: 0.3}

    m3 = {frozenset({"Gripa", "Meningita"}): 0.8, theta: 0.2}

    print("Scenariu: Pacient cu Febra, Pete și Analize ce indica infectie grava.")
    print("Combinam opiniile celor 3 surse...")

    final_m, k = ds.combine_multiple([m1, m2, m3])
    
    metrics = ds.calculate_metrics(final_m)
    ds.print_detailed_results(metrics, k)
    
    best_hyp = list(metrics.keys())[0]
    best_bel = metrics[best_hyp]['bel']
    
    print(f"\nCONCLUZIE MEDICALĂ:")
    print(f"Sistemul a identificat diagnosticul: {list(best_hyp)}")
    print(f"Gradul minim de certitudine (Belief): {best_bel*100:.1f}%")
