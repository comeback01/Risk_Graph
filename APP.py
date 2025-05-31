import streamlit as st
import plotly.express as px
import numpy as np
from MenaceStructure import Menace_Structure as Menace
from Famile import Famile as Manager_of_Menaces
from DataStructure import Structure
from PIL import Image

# Constants and not Constances de Gstaad 
Structure = Structure()  # Initialize the structure to access types and reduction risks
Min_menace = 1
Max_menace = 50


# Streamlit UI for managing menaces

Manager = Manager_of_Menaces()

st.title("Gestion des risques")
num_menaces = st.number_input(f"Combien de risques : de {Min_menace} à {Max_menace} ", min_value=Min_menace, max_value=Max_menace, value=1)

for i in range(num_menaces):
    Menace_tmp = Menace()
    Manager.add_element(Menace_tmp)  # Add the menace to the manager
    st.subheader(f"Risque n°{i + 1}") # Displaying the risk number
    #st.markdown(Structure.TextPolice(f"Date dernière modification : {Menace_tmp.Last_Modified}",12),unsafe_allow_html=True) # Display last modified date
    
    Col1_1, Col1_2 = st.columns(2) # Create two columns for layout
    with Col1_1:
        Menace_tmp.Update_Name(st.text_input(f"Nom du risque Risque n°{i+1}", key=f"name_{i}")) # Display input for risk name
    with Col1_2:
        Menace_tmp.Update_Type(st.selectbox(f"Type de risque n°{i+1}", options=Structure.TypesMenaces, key=f"type_{i}")) # Display select box for risk type

    Col2_1, Col2_2 = st.columns([1,1], vertical_alignment='center') # Create two more columns for layout
    with Col2_1:
        st.write(f"****Definir le risque inhérent****")
    with Col2_2:
        HelpBouton_1 = st.button("❓", help=f"Formule du risque inhérent : {Structure.Formule_Risque_Inherent}", key=f"help_inherent_{i}")  # Help button for inherent risk formula

    Col3_1, Col3_2 = st.columns(2) # Create two more columns for layout
    with Col3_1:
        val2_1 = st.slider(f"Impact {Structure.Impact_Inherent[0]}", min_value=Structure.Echelle["min"], max_value=Structure.Echelle["max"], value=Structure.Echelle["min"], step=1, key=f"impact_inherent_{i}_1")
        val2_1 = round(val2_1, 2)  # Round the value 
    with Col3_2:
        val2_2 = st.slider(f"Impact {Structure.Impact_Inherent[1]}", min_value=Structure.Echelle["min"], max_value=Structure.Echelle["max"], value=Structure.Echelle["min"], step=1, key=f"impact_inherent_{i}_2")
        val2_2 = round(val2_2, 2)  # Round the value
    Menace_tmp.Update_Impact_Inherent(val2_1, val2_2)  # Update inherent impact values
    
    st.markdown(Structure.TextPolice(f"Valeur de l'Impact Inhérent : {Menace_tmp.Impact_Inherent}",12), unsafe_allow_html=True)  # Display inherent impact value

    Col3_1, Col3_2 = st.columns([1,1],vertical_alignment='center')  # Create two more columns for layout
    with Col3_1:
        st.write(f"****Définir l'occurrence du risque n°{i+1}****")
    with Col3_2:
        st.write(f"****Mesures face au risque n°{i+1}****")

    Col4_1, Col4_2 = st.columns([1,1],vertical_alignment='top')  # Create two more columns for layout
    with Col4_1:
        Occurrence = st.select_slider("Choisissez une option :", options=Structure.Echelle_Occurrence.keys(), key=f"select_occurence_{i}")  # Select slider for occurrence
        Menace_tmp.Update_Occurrence(Occurrence)  # Update occurrence value
    with Col4_2:
        Selection_Reduction_Risque = st.multiselect("Sélectionner les mesures de réduction des risques", options=Structure.Reduction_Risques, key=f"reduction_risque_{i}")  # Multi-select for risk reduction measures
        if "Aucune" in Selection_Reduction_Risque and len(Selection_Reduction_Risque) >  1:
            st.warning("Si vous sélectionnez 'Aucune', vous ne pouvez pas sélectionner d'autres mesures de réduction des risques.")
        else:
            Menace_tmp.Update_Reduction_Risque(Selection_Reduction_Risque)  # Update risk reduction measures
    
    #Menace_tmp.Update_Criticite()
    #st.markdown(Structure.TextPolice(f"Criticité : {Menace_tmp.Criticite} | value : {Menace_tmp.Criticite_value}", 20), unsafe_allow_html=True)  # Display real impact value

if st.toggle("Affichage graphique des risques",False, key=f'Display_Graph_1') == True:
    Manager.Pre_graphique()

    X = Manager.Data_Structure[Structure.Axes["X"]]
    Y = Manager.Data_Structure[Structure.Axes["Y"]]
    
    fig = px.scatter(x = X,
                     y = Y,
                     width = 800,
                     height = 800,
                     labels = {'x': Structure.Axes["X"], 'y': Structure.Axes["Y"]},
                     size=[10 for y in range(len(X))],  # Set a constant size for all points
                     color = Manager.Data_Structure["Type"],
                     color_discrete_map = Structure.TypesMenaces_Couleur,
             
                    custom_data=[Manager.Data_Structure["Name"], 
                                  Manager.Data_Structure["Type"], 
                                  Manager.Data_Structure["Occurrence"], 
                                  ]
                    )
    

    fig.update_traces(hovertemplate=
                    "<b>Nom :</b> %{customdata[0]}<br>" +
                    "<b>Type :</b> %{customdata[1]}<br>" +
                    "<b>Impact réel :</b> %{customdata[2]}<br>" +
                    "<extra></extra>"
                    )  # Customize hover template to show name, occurrence, and real impact

    fig.update_layout(title={'text': "Graphique des Risques", 'x':0.5})
    fig.update_xaxes(range=[0.5, 4+0.5], showticklabels=True, dtick = 1)
    fig.update_yaxes(range=[0.5, 4+0.5], showticklabels=True, dtick = 1)

    fig.add_layout_image(
        dict(
            source=Image.open("Fond.png"),
            xref = "x", yref = "y",
            x = Structure.Echelle["min"] - 0.5, y = Structure.Echelle["max"] + 0.5,
            sizex = Structure.Echelle["max"] - Structure.Echelle["min"] + 1,
            sizey = Structure.Echelle["max"] - Structure.Echelle["min"] + 1,
            sizing="stretch",
            opacity=0.2,
            layer="above",
        )
    )

    #col5_1 = st.columns(1)  # Create two columns for layout
    #with col5_1:
    st.plotly_chart(fig, use_container_width=False)  # Display the plotly chart in Streamlit, with the defined format
        


