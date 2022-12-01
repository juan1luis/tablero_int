from flask import render_template
from flask import Flask
import pandas as pd
import json
import plotly
import plotly_express as px
import pandas as pd
import math

app = Flask(__name__) 


info_carre = pd.read_csv('Programas_Int.csv')

@app.route('/')
def charts():

    no_opor = info_carre.groupby(["Op_Asig"], as_index=False)["Matricula"].count()
    opciones=[]
    for i in range(8):
        opciones.append(no_opor.iloc[i][1])
    
    Total = sum(opciones)
    No_selec = opciones[0]
    Selec = Total - No_selec
    P_selec = (Selec/Total)*100
    P_selec_op1 = math.floor((opciones[1]/Selec)*100)

    ty_opor = info_carre.groupby(["Tipo_Programa"], as_index=False)["Matricula"].count()
    AS = ty_opor.iloc[1][1] - No_selec
    INT = ty_opor.iloc[0][1] 
    P_AS = math.floor((AS/(AS+INT))*100)
    P_INT = math.floor((INT/(AS+INT))*100)

    
    #-----------------------------------------------------------------------------------------------------------#
    '''Grafico Alluvial'''

    allu = info_carre[['Escuela','Tipo_Programa','Pais_v','Pais_N']]
    alluvial = px.parallel_categories(allu,dimensions=['Escuela', 'Tipo_Programa', 'Pais_N'], color="Pais_v",
                                        title='Escuela vs Programa vs Pais A', 
    color_continuous_scale=px.colors.sequential.deep)
    g_alluvial = json.dumps(alluvial,cls = plotly.utils.PlotlyJSONEncoder)
    #-----------------------------------------------------------------------------------------------------------#
    '''Grafico Pie''' 

    pie_ = info_carre.groupby(["Op_Asig",'No._Opcion','Tipo_Programa'], as_index=False)["Matricula"].count()
    pie_ = pie_[pie_['Tipo_Programa'] == 'INT']
    pie = px.pie(pie_, values='Matricula', names='No._Opcion', color='Op_Asig', hole = .4,title='Opcion Asignada',
             color_discrete_map={1:'blue',
                                 7:'royalblue',
                                 3:'darkblue', 
                                 4:'cyan',
                                 2:'powderblue', 
                                 5:'lightcyan',
                                 6:'cornflowerblue',
                                 8:'skyblue'})
    g_pie = json.dumps(pie,cls = plotly.utils.PlotlyJSONEncoder)
    #-----------------------------------------------------------------------------------------------------------#
    '''Grafico Solar'''

    sun = info_carre[['Values','Nivel','Escuela','Carrera']]
    sunbur = px.sunburst(sun, path=['Nivel', 'Escuela', 'Carrera'], values='Values',title='Carreras y Derivados',color='Nivel',
                  color_discrete_map={'Profesional':'darkblue', 'Maestría':'skyblue', 'Preparatoria':'black', 'Doctorado':'skyblue',
       'Indefinido':'lightcyan', 'Especialidad':'blue'})
    g_sunbur = json.dumps(sunbur,cls = plotly.utils.PlotlyJSONEncoder)
    #-----------------------------------------------------------------------------------------------------------#
    '''Grafico Barras'''
    barra = info_carre.groupby(["Asignado", "Escuela"], as_index=False)["Matricula"].count()
    barras = px.bar(barra, y=["Escuela","Matricula"], x="Asignado", color="Escuela", title="Asignados vs Escuela")
    g_barras = json.dumps(barras,cls = plotly.utils.PlotlyJSONEncoder)
    #-----------------------------------------------------------------------------------------------------------#
    
    return render_template('index.html', g_alluvial=g_alluvial,g_pie=g_pie,g_sunbur=g_sunbur,g_barras=g_barras,
                                        P_selec_op1=P_selec_op1,P_AS=P_AS)

 
if __name__ == '__main__':
    app.run(debug=True)