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
    

def afisare_rezultate_detaliate(metrics, conflict_val):
    print("\nREZULTATE DETALIATE ALE COMBINARII EVIDENTELOR")
    print("-" * 90)
    print(f"{'IPOTEZA':<30} | {'MASA (m)':<10} | {'BEL (Sigur)':<10} | {'PL (Posibil)':<10} | {'INCERTITUDINE':<13}")
    print("-" * 90)

    for subset, vals in metrics.items():
        subset_str = format_set(subset)
        print(f"{subset_str:<30} | {vals['mass']:.4f}     | {vals['bel']:.4f}     | {vals['pl']:.4f}     | {vals['incertitudine']:.4f}")
        print("-" * 90)

def afisare_interpretare_decizie(metrics):
    print("INTERPRETARE DECIZIE:")
    if not metrics:
        print("Nu exista date pentru interpretare.")
        return
    items = list(metrics.items())
    best_bel = items[0][1]['bel']

    winners = []
    for hyp, vals in items:
        if abs(vals['bel'] - best_bel) < 0.0001:  
            winners.append(hyp)

    if len(winners) > 1:
        nume_winners = []
        for w in winners:
            nume_winners.append(", ".join(sorted(list(w))).upper())
            
        print(f"CONFLICT DE DECIZIE: Sistemul nu poate diferentia intre: {' si '.join(nume_winners)}")
        print(f"Ambele au un grad de certitudine egal de {best_bel*100:.1f}%.")
        print("Se recomanda investigatii suplimentare pentru a departaja.")
        
    else:
        top_hyp_set = winners[0]
        hyp_list = sorted(list(top_hyp_set))
        
        if len(hyp_list) == 1:
            print(f"Sistemul indica {hyp_list[0].upper()} cu un grad de certitudine de {best_bel*100:.1f}%")
        
        elif len(hyp_list) >= 3: 
            print("Sistemul NU poate lua o decizie clara (Incertitudine ridicata - Ignoranta).")
            print("Sunt necesare investigatii suplimentare.")
            
        else:
            print(f"Sistemul indica o zona probabila intre: {', '.join(hyp_list).upper()} ({best_bel*100:.1f}%)")
            print("Diagnosticul exact nu a putut fi izolat complet.")
            
    print("-" * 60)

def caz_medical_complex():
    ds = DempsterShafer()
    print("\nSUITA TESTE: DIAGNOSTIC MEDICAL COMPLET")

    # Universul discursului: Posibile diagnostice
    theta = frozenset({"Gripa", "Raceala", "Pneumonie"})

    print("\n SCENARIUL 1: CONSENS (Simptome clare + Test Rapid Pozitiv)")
    print("Descriere: Medicul suspecteaza Gripa (0.8), Testul rapid confirma Gripa (0.9).")
    
    m_medic = {frozenset({"Gripa"}): 0.8, theta: 0.2}
    m_test  = {frozenset({"Gripa"}): 0.9, theta: 0.1}
    
    afisare_tabel_stil_curs(m_medic, m_test, titlu="Calcul Consens: Medic vs Test")
    
    rezultat_1, k1 = ds.combinare([m_medic, m_test])
    metrics_1 = ds.calculeaza_bel_pl(rezultat_1)
    afisare_rezultate_detaliate(metrics_1, k1)
    afisare_interpretare_decizie(metrics_1)
    
    print("\n SCENARIUL 2: RAFINARE (Excluderea prin intersectie)")
    print("Descriere: \nSursa 1 (Simptome Generale): Poate fi Gripa sau Pneumonie (febra mare).\nSursa 2 (Radiografie): Plamanii sunt curati (Exclude Pneumonia).")
    
    m_simptome = {frozenset({"Gripa", "Pneumonie"}): 0.8, theta: 0.2}
    m_radio = {frozenset({"Gripa", "Raceala"}): 0.9, theta: 0.1}
    
    afisare_tabel_stil_curs(m_simptome, m_radio, titlu="Calcul Rafinare: Simptome vs Radiografie")
    
    rezultat_2, k2 = ds.combinare([m_simptome, m_radio])
    metrics_2 = ds.calculeaza_bel_pl(rezultat_2)
    afisare_rezultate_detaliate(metrics_2, k2)
    afisare_interpretare_decizie(metrics_2)
    
    print("\n SCENARIUL 3: IGNORANTA (Incertitudine ridicata)")
    print("Descriere: Pacient atipic. Medicul e nesigur, Analizele sunt neconcludente.")
    
    # Masa mare pe Theta inseamna "Nu stiu"
    m_nesigur1 = {frozenset({"Raceala"}): 0.1, theta: 0.9}
    m_nesigur2 = {theta: 1.0} # A doua sursa nu stie nimic
    
    afisare_tabel_stil_curs(m_nesigur1, m_nesigur2, titlu="Calcul Ignoranta: Medic vs Analize")

    rezultat_3, k3 = ds.combinare([m_nesigur1, m_nesigur2])
    metrics_3 = ds.calculeaza_bel_pl(rezultat_3)
    afisare_rezultate_detaliate(metrics_3, k3)
    afisare_interpretare_decizie(metrics_3)

    print("\n SCENARIUL 4: CONFLICT MODERAT (Opinie divergenta)")
    print("Descriere: \nSpecialist 1 zice Pneumonie (0.7).\nSpecialist 2 zice Raceala (0.7).\nAmandoi accepta o marja de eroare (Theta).")
    
    m_spec1 = {frozenset({"Pneumonie"}): 0.7, theta: 0.3}
    m_spec2 = {frozenset({"Raceala"}): 0.7, theta: 0.3}
    
    afisare_tabel_stil_curs(m_spec1, m_spec2, titlu="Calcul Conflict: Pneumonie vs Raceala")
    
    rezultat_4, k4 = ds.combinare([m_spec1, m_spec2])
    metrics_4 = ds.calculeaza_bel_pl(rezultat_4)
    afisare_rezultate_detaliate(metrics_4, k4)
    afisare_interpretare_decizie(metrics_4)
    
    print(f" Conflictul K este {k4:.2f}. Masa conflictuala a fost redistribuita proportional catre ipotezele ramase.")

    print("\n SCENARIUL 5: CONFLICT TOTAL (Eroare/Paradox)")
    print("Descriere: Doua surse sigure se contrazic complet (K ~ 1.0).")
    
    m_paradox1 = {frozenset({"Gripa"}): 0.99, frozenset({"Pneumonie"}): 0.01}
    m_paradox2 = {frozenset({"Raceala"}): 0.99, frozenset({"Pneumonie"}): 0.01}
    
    try:
        afisare_tabel_stil_curs(m_paradox1, m_paradox2, titlu="Tentativa Combinare Paradoxala")
        rezultat_5, k5 = ds.combinare([m_paradox1, m_paradox2])
        afisare_rezultate_detaliate(ds.calculeaza_bel_pl(rezultat_5), k5)
    except ValueError as e:
        print(f"\n SISTEMUL A DETECTAT O EROARE CRITICA: {e}")

def caz_bancar_complex():
    ds = DempsterShafer()
    print(" STUDIU DE CAZ 2: DETECTAREA FRAUDELOR BANCARE ")
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
        print(f"\n\n ANALIZA: {caz['nume']}")
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
        

