from DataStructure import Structure
from datetime import datetime
from math import log1p, exp

ENV_Structure = Structure()

class Menace_Structure:

    """
    Classe représentant une menace dans une structure de gestion des risques.
    \nAttributs:
    \n  Creation_Date (str): Date et heure de création de la menace.
    \n  Last_Modified (str): Date et heure de la dernière modification.
    \n  Name (str): Nom de la menace.
    \n  Type (str): Type de la menace, doit appartenir à la liste des types définis dans ENV_Structure.
    \n  Occurrence (float): Fréquence d'occurrence de la menace, comprise dans l'échelle définie.
    \n  Reduction_Risque (float): Facteur de réduction du risque (non initialisé directement).
    \n  Reduction_Risque_List (list): Liste des facteurs de réduction de risque appliqués.
    \n  Impact_Inherent (float): Impact inhérent de la menace (somme des impacts financiers et réputationnels).
    \n  Impact_Inherent_Dict (dict): Dictionnaire contenant les impacts financiers et réputationnels.
    \n  Real_Impact (float): Impact réel après prise en compte des réductions de risque.
    \n  Criticite (str): Niveau de criticité de la menace selon une échelle prédéfinie.
    \nMéthodes:
    \n  Update_Last_Modified():
    \n      Met à jour la date de dernière modification de la menace.
    \n  Update_Name(Name: str):
    \n      Met à jour le nom de la menace et la date de dernière modification.
    \n  Update_Type(Type: str):
    \n      Met à jour le type de la menace si celui-ci est valide, sinon lève une exception.
    \n  Wrapper_Update_Name_Type(Name: str, Type: str):
    \n      Met à jour le nom et le type de la menace.
    \n  Update_Occurrence(Occurrence: float):
    \n      Met à jour la fréquence d'occurrence de la menace si elle est dans l'échelle autorisée.
    \n  Compute_Impact_Inherent():
    \n      Calcule l'impact inhérent de la menace à partir des valeurs financières et réputationnelles.
    \n  Update_Impact_Inherent(Financier: float, Reputationnel: float):
    \n      Met à jour les valeurs d'impact inhérent et recalcule l'impact total.
    \n  Update_Reduction_Risque(Reduction_Risque: list):
    \n      Met à jour la liste des facteurs de réduction de risque et recalcule l'impact réel.
    \n  Update_Criticite():
    \n      Met à jour la criticité de la menace selon la formule définie et l'échelle de criticité.
    """

    def __init__(self): 

        """ Initialisation des attributs de la menace """

        self.Creation_Date: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.Last_Modified: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.Name: str
        self.Type: str
        self.Occurrence: float
        self.Reduction_Risque: float
        self.Reduction_Risque_List: list
        self.Impact_Inherent: float
        self.Impact_Inherent_Dict: dict
        self.Real_Impact: float
        self.Criticite_value: float
        self.Criticite: str
        self.Graph_Data: dict
        self.Couleur: str

    def Update_Last_Modified(self):

        """ Met à jour la date de dernière modification """

        self.Last_Modified = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def Update_Name(self, Name: str):

        """ Met à jour le nom de la menace """

        self.Name = Name
        self.Update_Last_Modified()

    def Update_Type(self, Type: str):

        """ Met à jour le type de la menace """

        if Type in ENV_Structure.TypesMenaces: # Vérification que le type est valide
            self.Type = Type
            self.Update_Couleur()  # Met à jour la couleur en fonction du type
            self.Update_Last_Modified()
        else:
            raise ValueError(f"Type '{Type}' is not a valid menace type. Valid types are: {ENV_Structure.TypesMenaces}")

    def Wrapper_Update_Name_Type(self, Name: str, Type: str):

        """ Wrapper pour mettre à jour le nom et le type de la menace """

        self.Update_Name(Name)
        self.Update_Type(Type)

    def Update_Occurrence(self, Occurrence: str):

        """ Met à jour l'occurrence de la menace """

        if Occurrence in ENV_Structure.Echelle_Occurrence.keys():
            self.Occurrence = ENV_Structure.Echelle_Occurrence[Occurrence]
            self.Update_Last_Modified()
        else:
            raise ValueError("Occurrence is not in keys.")

    def Compute_Impact_Inherent(self): 

        """ Calcule l'impact inhérent de la menace
        \nPossible de modifier la formule du calcul de l'impact inhérent """

        self.Impact_Inherent = self.Impact_Inherent_Dict["Financier"] + self.Impact_Inherent_Dict["Reputationnel"] 
        self.Impact_Inherent = round(self.Impact_Inherent, 2)
        self.Update_Last_Modified()

    def Update_Impact_Inherent(self, Financier:float, Reputationnel: float):

        """ Met à jour l'impact inhérent de la menace """
        
        if not (ENV_Structure.Echelle["min"] <= Financier <= ENV_Structure.Echelle["max"] and ENV_Structure.Echelle["min"] <= Reputationnel <= ENV_Structure.Echelle["max"]):
            raise ValueError(f"Impact values must be between {ENV_Structure.Echelle['min']} and {ENV_Structure.Echelle['max']}, with 0 being no impact and 5 being very high impact.")
        else:
            # Prise en compte des facteurs de l'impact inhérent
            self.Impact_Inherent_Dict = {
                "Financier": Financier,
                "Reputationnel": Reputationnel
            }
            self.Compute_Impact_Inherent()
            self.Update_Last_Modified()

    def Update_Reduction_Risque(self, Reduction_Risque: list):
        
        """ Met à jour la liste des facteur de réduction de risque """
        
        if all(item in ENV_Structure.Reduction_Risques for item in Reduction_Risque):
            self.Reduction_Risque_List = Reduction_Risque

            tmp = 0
            for item in Reduction_Risque:
                tmp += ENV_Structure.Dict_Reduction_Risques[item]
            
            self.Real_Impact = Structure.RealImpact_Sigmoide(self.Impact_Inherent * exp(tmp / 100))
            self.Real_Impact = round(self.Real_Impact, 2)
            self.Update_Last_Modified()
            
        else:
            raise ValueError(f"Reduction risks must be from the predefined list: {ENV_Structure.Reduction_Risques}")

    #def Update_Criticite(self):
    #    
    #    """ Met à jour la criticité de la menace selon la formule définie ci-dessous """
    #    
    #    tmp = exp(self.Real_Impact) * log1p(1 + self.Occurrence)
    #    tmp = round(tmp, 2)  # Arrondi à deux décimales pour la criticité
    #    self.Criticite_value = tmp
    #    if tmp < ENV_Structure.Echelle_Criticite["Faible"]:
    #        self.Criticite = "Faible"
    #    elif tmp < ENV_Structure.Echelle_Criticite["Faiblement modérée"]:
    #        self.Criticite = "Faiblement modérée"
    #    elif tmp < ENV_Structure.Echelle_Criticite["Modérée"]:
    #        self.Criticite = "Modérée"
    #    elif tmp < ENV_Structure.Echelle_Criticite["Forte"]:
    #        self.Criticite = "Forte"
    #    elif tmp < ENV_Structure.Echelle_Criticite["Très forte"]:
    #        self.Criticite = "Très forte"
    #    else:
    #        self.Criticite = "Extreme"
    #
    #    self.Update_Last_Modified()

    def Update_Couleur(self):

        """ Met à jour la couleur de la menace en fonction de son type """

        self.Couleur = ENV_Structure.TypesMenaces_Couleur[self.Type]
        self.Update_Last_Modified()

    def Get_Graph_Data(self):

        """ Retourne une structure utile pour la visualisation graphique de la menace """

        self.Graph_Data = {
            "Name": self.Name,
            "Type": self.Type,
            "Occurrence": self.Occurrence,
            "Real_Impact": self.Real_Impact,
            "Couleur": self.Couleur,
        }

        self.Update_Last_Modified()

        return self.Graph_Data

