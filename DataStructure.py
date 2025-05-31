from numpy import exp

Min_value = 1
Max_value = 4

class Structure():

    @staticmethod
    def TextPolice(texte:str, size:int=12) -> str:
        return f"<span style='font-size:{size}px;'>{texte}</span>"

    @staticmethod
    def RealImpact_Sigmoide(x, Max=Max_value, k=1, x0=(Min_value+Max_value)/1.5) -> float:
            """
            Fonction sigmoïde pour calculer l'impact réel en fonction de l'impact inhérent.
            :param x: Valeur de l'impact inhérent.
            :param Max: Valeur maximale de l'échelle.
            :param k: Pente de la sigmoïde.
            :param x0: Point d'inflexion de la sigmoïde.
            :return: Valeur de l'impact réel.
            """
            return 1 + (Max - 1) / (1 + exp(-k * (x - x0)))

    def __init__(self):
        self.TypesMenaces: list = [
            "Humain",
            "Environnement",
            "Juridique",
            "Informatique",
            "Batiment",
            "Fraude",
            "Prestataire",
            "Communication", 
            "Données personnelles",
        ]   
        
        self.TypesMenaces_Couleur: dict = {
            "Humain": "#FF5733",
            "Environnement": "#33FF57",
            "Juridique": "#3357FF",
            "Informatique": "#FF33A1",
            "Batiment": "#FF8C33",
            "Fraude": "#33FFF5",
            "Prestataire": "#F5FF33",
            "Communication": "#FF33F5",
            "Données personnelles": "#F5F533"
        }

        self.Reduction_Risques: list = [
            "Aucune",
            "Formation",
            "Sensibilisation",
            "Plan de continuité d'activité",
            "Plan de reprise d'activité",
            "Mesure de réduction des risques",
            "Plan de gestion de crise testé"
        ]
        
        #ici on utilise les items comme des variations en % donc 50 implique hausse des risque de 50% par rapport à l'état initial
        self.Dict_Reduction_Risques: dict = {
            "Aucune": 100,
            "Formation": -20,
            "Sensibilisation": -10,
            "Plan de continuité d'activité": -10,
            "Plan de reprise d'activité": -10,
            "Mesure de réduction des risques": -10,
            "Plan de gestion de crise testé": -30
        }

        self.Impact_Inherent: list = [
            "Financier",
            "Reputationnel",
        ]

        self.Echelle: dict = {
            "min": Min_value,
            "max": Max_value,
        }
        
        self.Axes: dict = {
            "X": "Occurrence",
            "Y": "Real_Impact",
        }

        #self.Echelle_Criticite: dict = {
        #    "Faible": 0,
        #    "Faiblement modérée": 500,
        #   "Modérée": 1000,
        #    "Forte": 2000,
        #    "Très fort": 5000,
        #    "Extreme": 10000
        #}

        self.Echelle_Occurrence: dict = {
            "Rare": 1.0,
            "Peu probable": 2,
            "Probable": 3,
            "Certain": 4,
        }
        
        self.Formule_Risque_Inherent: str = "Financier + Reputationnel"