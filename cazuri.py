from dempster_shafer import DempsterShafer

def format_set(s):
    if not s: return "Ø"
    return "{" + ", ".join(sorted(list(s))) + "}"

def afisare_tabel_stil_curs(m1, m2, titlu="TABEL COMBINARE EVIDENTE (Stil Curs)"):
    print(f"\n{titlu}")
    print("-" * 105)
    print(f"{'m1 BBA':<25} {'m2 BBA':<25} {'intersectie':<25} {'produs':<10}")
    print("-" * 105)
    conflict_sum=0.0
    for h1, val1 in m1.items():
        for h2, val2 in m2.items():
            intersect = h1.intersection(h2)
            prod = val1 * val2
            s1_str = f"{format_set(h1)} {val1:.2g}"
            s2_str = f"{format_set(h2)} {val2:.2g}"
            inters_str = format_set(intersect)
            if not intersect:
                conflict_sum += prod
                inters_str="Multime Vida (Conflict)"
            print(f"{s1_str:<25} {s2_str:<25} {inters_str:<25} {prod:.4f}")
    print("-" * 105)
    if conflict_sum > 0:
        print(f"Conflict total K = {conflict_sum:.4f}")
        print(f"Factor de normalizare = (1 / (1 - K)): 1 / (1 - {conflict_sum:.4f}) = {1/(1-conflict_sum):.4f}")
    else:
        print("Nu exista conflict intre surse.")
    print("-" * 105)

def afisare_rezultate_detaliate(metrics, conflict_val):
    print("\nREZULTATE DETALIATE ALE COMBINARII EVIDENTELOR")
    print("-" * 90)
    print(f"{'IPOTEZA':<30} | {'MASA (m)':<10} | {'BEL (Sigur)':<10} | {'PL (Posibil)':<10} | {'INCERTITUDINE':<13}")
    print("-" * 90)

    for subset, vals in metrics.items():
        subset_str = format_set(subset)
        print(f"{subset_str:<30} | {vals['mass']:.4f}     | {vals['bel']:.4f}     | {vals['pl']:.4f}     | {vals['incertitudine']:.4f}")
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

    print("Scenariu: Pacient cu Febra, Pete si Analize ce indica infectie grava.")
    print("Combinam opiniile celor 3 surse...")

    afisare_tabel_stil_curs(m1, m2, titlu="COMBINARE: Simptome (m1) + Analize (m2)")

    final_m, k = ds.combinare([m1, m2, m3])
    
    metrics = ds.calculeaza_bel_pl(final_m)
    afisare_rezultate_detaliate(metrics, k)
    
    best_hyp = list(metrics.keys())[0]
    best_bel = metrics[best_hyp]['bel']
    
    print(f"\nCONCLUZIE MEDICALA:")
    print(f"Sistemul a identificat diagnosticul: {list(best_hyp)}")
    print(f"Gradul minim de certitudine (Belief): {best_bel*100:.1f}%")

def caz_bancar_complex():
    ds = DempsterShafer()
    print("\n\n" + "="*60)
    print("=== STUDIU DE CAZ 2: DETECTAREA FRAUDELOR BANCARE ===")
    print("="*60)

    theta = frozenset({"ClientBun", "ClientRiscant", "Frauda"})
        
    scenarii=[
        {
            "nume": "CLIENT 1: PROFIL IDEAL",
            "m_venit": {frozenset({"ClientBun"}): 0.8, theta: 0.2},
            "m_istoric": {frozenset({"ClientBun"}): 0.9, theta: 0.1},
            "m_comp": {frozenset({"ClientBun"}): 0.7, theta: 0.3}
        },
        {
            "nume": "CLIENT 2: RISC RIDICAT (Istoric negativ)",
            "m_venit": {frozenset({"ClientBun"}): 0.7, theta: 0.3},
            "m_istoric": {frozenset({"ClientRiscant"}): 0.8, theta: 0.2},
            "m_comp": {theta: 1.0}
        },
        {
            "nume": "CLIENT 3: SUSPICIUNE DE FRAUDA",
            "m_venit": {frozenset({"ClientBun"}): 0.6, theta: 0.4},
            "m_istoric": {theta: 1.0},
            "m_comp": {frozenset({"Frauda"}): 0.7, frozenset({"ClientRiscant"}): 0.2, theta: 0.1}
        }
    ]

    for caz in scenarii:
        print(f"\n\n>>> ANALIZA: {caz['nume']}")
        afisare_tabel_stil_curs(caz['m_venit'], caz['m_istoric'], titlu=f"DETALIU CALCUL (Venit vs Istoric) pentru {caz['nume']}")
        surse=[caz['m_venit'], caz['m_istoric'], caz['m_comp']]
        result, k = ds.combinare(surse)
        metrics = ds.calculeaza_bel_pl(result)
        afisare_rezultate_detaliate(metrics, k)
        top_hyp = list(metrics.keys())[0] #ipoteza cu cel mai mare belief
        print(f"INTERPRETARE DECIZIE:")
        if "Frauda" in top_hyp:
            print(f"Sistemul indica FRAUDA cu un grad de certitudine de {metrics[top_hyp]['bel']*100:.1f}%")
        elif "ClientRiscant" in top_hyp:
            print(f"Sistemul indica CLIENT RISCANT cu un grad de certitudine de {metrics[top_hyp]['bel']*100:.1f}%")
        elif "ClientBun" in top_hyp and len(top_hyp)==1:
            print(f"Sistemul indica CLIENT BUN cu un grad de certitudine de {metrics[top_hyp]['bel']*100:.1f}%")
        else:
            print(f"Sistemul nu poate lua o decizie clara, ipoteza principala este {list(top_hyp)} cu un grad de certitudine de {metrics[top_hyp]['bel']*100:.1f}%")
        print("-"*60)

