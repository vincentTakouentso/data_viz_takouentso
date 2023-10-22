import streamlit as st
import  pandas as pd
import matplotlib.pyplot  as plt

import altair as alt
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool



st.title(' VISUALISATIONS CAS DE LA PRODUCTION ELECTRIQUE ')
st.title('TAKOUENTSO Guy vincent groupe BIA')

data = pd.read_csv("courbe-prod-elec.csv",delimiter=";")

if st.checkbox("Afficher un aperçu des données"):
    st.write(data)
if st.checkbox('Afficher les statistiques descriptives'):
    st.subheader('Statistiques descriptives')
    st.write(data.describe())

# colonne que vous voulez utiliser pour la visualisation basique
column_to_plot = st.selectbox("quelle colonne voulez vous visualiser ?", data.columns)

# visualisation basique
fig, ax = plt.subplots()
data[column_to_plot].hist(ax = ax)
ax.set_title(f'Histogramme pour la colonne {column_to_plot}')
ax.set_xlabel('Valeur')
ax.set_ylabel('Fréquence')
st.pyplot(fig)

st.title("visualisation internes")




#visualisations internes
#Évolution de la production totale d\'énergie au fil du temps
if st.checkbox("au cour du temps"):
    def get_hour(dt):
        return dt.hour

    data['date_heure'] = pd.to_datetime(data['date_heure'])

    data['hour'] = data['date_heure'].map(get_hour)

    plot_data = data.set_index('date_heure')[['production_totale_mw']]
    st.write('### 1- Évolution de la production totale d\'énergie au fil du temps', unsafe_allow_html=True)

    st.line_chart(plot_data)

#Production d\'électricité par territoire

production_par_territoire = data.groupby('territoire')['production_totale_mw'].sum()
fig, ax = plt.subplots()

ax.bar(production_par_territoire.index, production_par_territoire.values, color='skyblue', edgecolor='black')

ax.set_title('Production d\'électricité par territoire')
ax.set_xlabel('Territoire')
ax.set_ylabel('Production d\'électricité (MW)')

plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
plt.tight_layout()

st.pyplot(fig)

#cout moyen de production par territoire
cout_production_par_territoire = data.groupby('territoire')['cout_moyen_de_production_eur_mwh'].sum()
fig, ax = plt.subplots()

ax.bar(cout_production_par_territoire.index, cout_production_par_territoire.values, color='green', edgecolor='black')

ax.set_title('cout moyen Production d\'électricité par territoire')
ax.set_xlabel('Territoire')
ax.set_ylabel('cout moyen de la Production d\'électricité (MW)')

plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
plt.tight_layout()

st.pyplot(fig)


#production d'energie par source d'energie

sources_energie = ['thermique_mw', 'hydraulique_mw', 'micro_hydraulique_mw', 'photovoltaique_mw', 'eolien_mw', 'bioenergies_mw', 'geothermie_mw']

total_par_source = data[sources_energie].sum()

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(total_par_source, autopct='%1.1f%%', startangle=150, colors=plt.cm.Paired.colors, textprops=dict(color="w"))

ax.legend(wedges, sources_energie,
          title="Sources d'énergie",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=10,weight="bold")
ax.set_title("Répartition de la production d'énergie par source")

# Égaliser l'aspect ratio pour que le diagramme soit circulaire
ax.axis('equal')
st.pyplot(fig)


st.title('Visualisations externes\n')
#consomation en fonctio du territoire et de la composition
# Sélectionnez la date et l'heure spécifiques pour la visualisation
date_heure = '2016-01-01T00:00:00+01:00'

filtered_data = data[data['date_heure'] == date_heure]

columns = ['thermique_mw', 'hydraulique_mw', 'micro_hydraulique_mw', 'photovoltaique_mw', 'eolien_mw', 'bioenergies_mw', 'geothermie_mw']

stacked_data = filtered_data.melt(id_vars=['territoire'], value_vars=columns, var_name='source', value_name='production_mw')

# Créer le graphique à barres empilées
stacked_chart = alt.Chart(stacked_data).mark_bar().encode(
    x=alt.X('territoire:N', title='Territoire'),
    y=alt.Y('production_mw:Q', title='Production (MW)'),
    color=alt.Color('source:N', title='Source d\'énergie'),
    order=alt.Order('source:N'),
    tooltip=['territoire', 'production_mw', 'source']
).properties(
    width=800,  # Largeur du graphique
    height=600,
    title='Production d\'énergie par territoire')

stacked_chart


#representation de la production et le cout moyen

# Préparez les données (supposons que 'data' est votre DataFrame)
x = data['production_totale_mw']
y = data['cout_moyen_de_production_eur_mwh']

# Créez un nouvel outil de survol et ajoutez des informations de survol utiles
hover = HoverTool(
    tooltips=[
        ("Index", "$index"),
        ("Production (MW)", "@x"),
        ("Coût moyen (EUR/MWh)", "@y"),
    ]
)

# Créez une nouvelle figure avec les options souhaitées
p = figure(title="Coût moyen vs Production totale",
           x_axis_label='Production Totale (MW)',
           y_axis_label='Coût Moyen de Production (EUR/MWh)',
           width=700, height=400, tools=[hover, 'pan', 'wheel_zoom', 'box_zoom', 'reset'])

# Ajoutez un cercle glyph pour le tracé de dispersion
p.circle(x, y, size=7, color="navy", alpha=0.5)

# Affichez le résultat
output_file("scatter.html")
show(p)



#production par saison
data['date_heure'] = pd.to_datetime(data['date_heure'])
#determination de la saison
def get_saison(date):
    month = date.month
    if 3 <= month <= 5:
        return 'Printemps'
    elif 6 <= month <= 8:
        return 'Été'
    elif 9 <= month <= 11:
        return 'Automne'
    else:
        return 'Hiver'

data['saison'] = data['date_heure'].apply(get_saison)

if st.checkbox("visualiser de nouveau le dataset a jour"):
    st.write(data)

# Sélectionner les colonnes des sources d'énergie
sources_energie = ['thermique_mw', 'hydraulique_mw', 'micro_hydraulique_mw', 'photovoltaique_mw', 'eolien_mw', 'bioenergies_mw', 'geothermie_mw']

# Créer un graphique à barres empilées pour chaque saison
plt.figure(figsize=(9, 6))

seasons = data['saison'].unique()

for season in seasons:
    gaz_season = data[data['saison'] == season]
    total_production = [gaz_season[source].sum() for source in sources_energie]
    plt.bar(sources_energie, total_production, label=season)

# Personnalisation du graphique
plt.title('Comparaison de la production d\'énergie par saison')
plt.xlabel('Sources d\'énergie')
plt.ylabel('Production d\'énergie (MW)')
plt.xticks(rotation=45)
plt.legend(title='Saison', loc='upper right')
st.pyplot(plt)