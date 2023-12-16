from flask import Flask, render_template, request, session
import extra, json, difflib, re, string
from markupsafe import Markup


app = Flask(__name__)
app.secret_key = b'_5#y2Ldccd"dcdcF4Q8dcdcz\n\xec]zfrgb543/'

@app.route('/Amawal-n-Taweryaɣelt/')
def amawal_n_tawaryaɣelt():
    # defines variables to pass to the tempalte
    var = {
        'path': extra.generate_breadcrumb(path=request.path)
    }

    # deletes previous variables from session and assign the current one to the session
    if 'var' in session: session.pop('var', None)
    session['var'] = var

    return render_template('Amawal n Taweryaɣelt.html', var=var)

amawal_n_tawaryaɣelt_data = {}
@app.route('/Amawal-n-Taweryaɣelt/', methods=['POST'])
def amawal_n_tawaryaɣelt_post():
    global amawal_n_tawaryaɣelt_data
    # load previous variables passed to the template
    var = session.get('var')
    var['abbrevations'] = extra.abbreviations

    # loads dictionary if it hasn't already
    if len(amawal_n_tawaryaɣelt_data) == 0:
        with open('data/dictionaries/amawal_n_taweryaɣelt.json', 'r', encoding='utf8') as file:
            amawal_n_tawaryaɣelt_data = json.load(file)

    query = request.form['search'].lower()
    print(query)

    # var['related_results'] = [[key, amawal_n_tawaryaɣelt_data[key]] for key in amawal_n_tawaryaɣelt_data if query in key]
    # main_result = difflib.get_close_matches(query, [i[0].lower() for i in var['related_results']], n=1, cutoff=0.1)
    res_15 = difflib.get_close_matches(query, [i for i in amawal_n_tawaryaɣelt_data], n=15, cutoff=0.1)
    print(res_15)
    
    if len(res_15) == 0:
        main_result = []
    else:
        main_result = res_15[0]
        var['related_results'] = res_15[1:]

    if len(main_result) != 0:      
        var['main_result'] = [main_result, amawal_n_tawaryaɣelt_data[main_result]]
        var['main_result'][0] = [main_result.capitalize(), extra.to_tifinaɣ(main_result)]


        synonyms, rebuild = extra.get_abrv(definition=var['main_result'][1])
        var['main_result_syn'] = []

        for i in synonyms: var['main_result_syn'] += i
                    
        var['main_result'][1] = Markup(rebuild)
        var['translate'] = Markup(extra.translate(rebuild))

    return render_template('Amawal n Taweryaɣelt.html', var=var)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')





# to do
# Mod. to table
# Combine words
# extract voir
# fix search results
# abrevation list
# make results a table or grid

