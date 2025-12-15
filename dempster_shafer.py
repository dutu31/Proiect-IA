from itertools import product

class DempsterShafer:
    def __init__(self):
        pass

    def combina_doua_surse(self, m1, m2):
        rezultat_temp = {} 
        K = 0.0

        for h1, v1 in m1.items():
            for h2, v2 in m2.items():
                
                intersectia = h1.intersection(h2)
                produs = v1 * v2

                # Daca intersectia e vida, inseamna ca sursele se contrazic (Conflict)
                if not intersectia:
                    K = K + produs
                else:
                    if intersectia not in rezultat_temp:
                        rezultat_temp[intersectia] = 0.0
                    rezultat_temp[intersectia] = rezultat_temp[intersectia] + produs

        if K >= 0.999:
             raise ValueError("Conflict total intre surse!")

        m_final = {}
        factor = 1.0 - K

        for ipoteza, val in rezultat_temp.items():
            m_final[ipoteza] = val / factor

        return m_final, K

    def combinare(self, lista_surse):
        if not lista_surse:
            return {}, 0.0
        
        m_curent = lista_surse[0]
        conflict_final = 0.0
        
        for i in range(1, len(lista_surse)):
            m_noua = lista_surse[i]
            m_curent, k = self.combina_doua_surse(m_curent, m_noua)
            conflict_final = k
            
        return m_curent, conflict_final

    def calculeaza_bel_pl(self, m_final):
        rezultate = {}
        
        for ipoteza_A in m_final.keys():
            bel = 0.0
            pl = 0.0
            
            for ipoteza_B, val_B in m_final.items():
                if ipoteza_B.issubset(ipoteza_A):
                    bel = bel + val_B
                
                if ipoteza_B.intersection(ipoteza_A):
                    pl = pl + val_B
            
            rezultate[ipoteza_A] = {
                "mass": m_final[ipoteza_A],
                "bel": bel,
                "pl": pl,
                "incertitudine": pl - bel
            }
            
        rez_sortat = dict(sorted(rezultate.items(), key=lambda x: x[1]['mass'], reverse=True))
        return rez_sortat