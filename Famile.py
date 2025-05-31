import MenaceStructure

class Famile:

    """
    Classe Famile\n
    ----------------\n
    Cette classe permet de regrouper et de gérer un ensemble d'éléments de type Menace_Structure.\n
    Elle offre des méthodes pour ajouter des éléments, récupérer la liste des éléments,\n
    et préparer les données nécessaires à la génération de graphiques.\n
    Attributs:\n
        elements (list): Liste des éléments de la famille (instances de Menace_Structure).\n
        Data_Structure (dict): Dictionnaire structurant les données des éléments pour l'affichage graphique.\n
    Méthodes:\n
        __init__(): Initialise une nouvelle instance de la classe Famile.\n
        add_element(element): Ajoute un élément de type Menace_Structure à la famille.\n
        get_elements(): Retourne la liste des éléments de la famille.\n
        Pre_graphique(): Prépare et structure les données des éléments pour la visualisation graphique.\n
    """

    def __init__(self):

        """ Initialisation de la classe Famile """

        self.elements = []
        self.Data_Structure: dict

    def add_element(self, element: MenaceStructure.Menace_Structure):

        """ Ajoute un élément à la famille """

        self.elements.append(element)

    def get_elements(self):

        """ Retourne la liste des éléments de la famille """

        return self.elements

    def Pre_graphique(self):

        """ Prépare les données pour le graphique en regroupant les éléments de la famille """
        self.Data_Structure = {
            "Name": [],
            "Type": [],
            "Occurrence": [],
            "Real_Impact": [],
            "Couleur": [],
        }
        
        for element in self.elements:
            self.Data_Structure["Name"].append(element.Name)
            self.Data_Structure["Type"].append(element.Type)
            self.Data_Structure["Occurrence"].append(element.Occurrence)
            self.Data_Structure["Real_Impact"].append(element.Real_Impact)
            self.Data_Structure["Couleur"].append(element.Couleur)

    
        